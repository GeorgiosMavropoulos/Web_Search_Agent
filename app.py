
import logging
import streamlit as st

from langchain_core.output_parsers import StrOutputParser

from llm.llm_instance import LLM
from prompts.prompt_templates import Prompt_Temps
from websearch_chain.web_search_chain import WebSearchChain
from scrapper_chain.scrap_chain import WebScrapChain


# ============================================================
# Configuration and logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI Research & Translation",
    page_icon="🌐",
    layout="wide"
)


# ============================================================
# Initialize dependencies safely
# ============================================================

@st.cache_resource
def initialize_dependencies():
    """Initialize reusable application dependencies."""
    llm = LLM()
    prompts = Prompt_Temps()
    return llm, prompts


try:
    llm_client, prompt_template = initialize_dependencies()
except Exception:
    logger.exception("Application initialization failed")
    st.error(
        "The application could not initialize its AI components. "
        "Check your configuration, API credentials, and terminal logs."
    )
    st.stop()


# ============================================================
# Error handling helpers
# ============================================================

class PipelineError(Exception):
    """An error associated with a specific pipeline stage."""

    def __init__(self, stage: str, message: str):
        super().__init__(message)
        self.stage = stage
        self.message = message


def run_stage(stage, operation, validator=None):
    """Execute one stage and provide consistent error handling."""
    try:
        result = operation()

        if validator is not None and not validator(result):
            raise ValueError(
                "The stage returned an empty or invalid result."
            )

        logger.info("Stage completed: %s", stage)
        return result

    except Exception as exc:
        logger.exception("Stage failed: %s", stage)

        raise PipelineError(
            stage=stage,
            message=str(exc)
        ) from exc


def is_nonempty_list(value):
    return isinstance(value, list) and len(value) > 0


def is_nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def display_stage_error(error):
    """Show a safe, user-friendly error in the GUI."""

    messages = {
        "Web Search": (
            "The web search failed. Check your search provider, "
            "network connection, and API configuration."
        ),
        "Web Scraping": (
            "The search completed, but the pages could not be "
            "retrieved. Some websites block automated requests."
        ),
        "Summary": (
            "The summary could not be generated. Check your LLM "
            "provider, model availability, and prompt configuration."
        ),
        "Translation": (
            "The translations could not be generated. Check the "
            "translation prompt and LLM configuration."
        ),
        "Evaluation": (
            "The translations were generated, but their evaluation "
            "failed. Check the judge prompt and LLM configuration."
        ),
    }

    st.error(f"❌ {error.stage} failed")
    st.write(messages.get(
        error.stage,
        "An unexpected error occurred during processing."
    ))

    with st.expander("Technical details"):
        st.code(error.message)

    st.info(
        "Correct the underlying issue and try again. "
        "If the error persists, check the application terminal logs."
    )


# ============================================================
# User interface
# ============================================================

st.title("🌐 AI Research & Translation")
st.caption(
    "Web Search → Web Scraping → Summary → Translation → Evaluation"
)

with st.form("research_form"):
    user_question = st.text_area(
        "Enter your question",
        placeholder="e.g. Who is M.J. Jackson?",
        height=100,
        max_chars=5000
    )

    submitted = st.form_submit_button(
        "Start Research",
        type="primary",
        use_container_width=True
    )


# ============================================================
# Execute pipeline
# ============================================================

if submitted:

    if not user_question.strip():
        st.warning("Please enter a question before starting.")
        st.stop()

    # Keep the current run's partial results, even if a later
    # stage fails.
    results = {
        "question": user_question.strip(),
        "urls": None,
        "texts": None,
        "summary": None,
        "translations": None,
        "evaluation": None,
        "failed_stage": None,
    }

    progress = st.progress(0)
    status = st.empty()

    try:
        # ----------------------------------------------------
        # 1. Web Search
        # ----------------------------------------------------
        status.info("🔎 Searching the web...")

        urls = run_stage(
            "Web Search",
            lambda: WebSearchChain.search(user_question.strip()),
            validator=is_nonempty_list
        )

        results["urls"] = urls
        progress.progress(20)

        # ----------------------------------------------------
        # 2. Web Scraping
        # ----------------------------------------------------
        status.info("📄 Retrieving webpage content...")

        texts = run_stage(
            "Web Scraping",
            lambda: WebScrapChain.scrape_urls(urls),
            validator=is_nonempty_list
        )

        results["texts"] = texts
        progress.progress(40)

        # ----------------------------------------------------
        # 3. Summary
        # ----------------------------------------------------
        status.info("📝 Generating summary...")

        summary_chain = (
            prompt_template.TEXT_SUMMARY_TEMPLATE
            | llm_client.get_llm()
            | StrOutputParser()
        )

        summary = run_stage(
            "Summary",
            lambda: summary_chain.invoke({
                "search_result_text": "\n\n".join(texts)
            }),
            validator=is_nonempty_text
        )

        results["summary"] = summary
        progress.progress(60)

        # ----------------------------------------------------
        # 4. Translation
        # ----------------------------------------------------
        status.info("🌍 Translating summary...")

        translation_chain = (
            prompt_template.TEXT_TRANSLATE_TEMPLATE
            | llm_client.get_llm()
            | StrOutputParser()
        )

        translations = run_stage(
            "Translation",
            lambda: translation_chain.invoke({
                "summarized_content": summary
            }),
            validator=is_nonempty_text
        )

        results["translations"] = translations
        progress.progress(80)

        # ----------------------------------------------------
        # 5. Evaluation
        # ----------------------------------------------------
        status.info("⚖️ Evaluating translations...")

        judge_chain = (
            prompt_template.JUDGE_TEMPLATE
            | llm_client.get_llm()
            | StrOutputParser()
        )

        evaluation = run_stage(
            "Evaluation",
            lambda: judge_chain.invoke({
                "summarized_content": summary,
                "translated_texts": translations
            }),
            validator=is_nonempty_text
        )

        results["evaluation"] = evaluation
        progress.progress(100)

        status.success("Research completed successfully!")
        st.session_state["research_results"] = results

    except PipelineError as exc:
        results["failed_stage"] = exc.stage

        # Save partial results so successful stages remain visible.
        st.session_state["research_results"] = results

        status.error(f"Stopped at: {exc.stage}")
        display_stage_error(exc)

    except Exception as exc:
        # Defensive fallback for errors outside run_stage().
        logger.exception("Unexpected pipeline failure")

        results["failed_stage"] = "Unexpected error"
        st.session_state["research_results"] = results

        status.error("The research pipeline stopped unexpectedly.")

        st.error(
            "An unexpected application error occurred. "
            "Your completed results, if any, are preserved below."
        )

        with st.expander("Technical details"):
            st.code(str(exc))


# ============================================================
# Display results, including partial results
# ============================================================

if "research_results" in st.session_state:

    results = st.session_state["research_results"]

    st.divider()
    st.subheader("Research Results")
    st.write("**Question:**", results["question"])

    if results["failed_stage"]:
        st.warning(
            f"Partial results: the pipeline stopped at "
            f"{results['failed_stage']}."
        )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔎 Web Search",
        "📄 Scraped Text",
        "📝 Summary",
        "🌍 Translations",
        "⚖️ Judge"
    ])

    with tab1:
        st.subheader("Retrieved URLs")
        urls = results["urls"]

        if urls:
            for i, url in enumerate(urls, start=1):
                st.markdown(f"{i}. [{url}]({url})")
        else:
            st.info("No search results are available.")

    with tab2:
        st.subheader("Scraped Content")
        texts = results["texts"]

        if texts:
            for i, text in enumerate(texts, start=1):
                with st.expander(f"Document {i}"):
                    st.text(text)
        else:
            st.info("No scraped content is available.")

    with tab3:
        st.subheader("Generated Summary")
        summary = results["summary"]

        if summary:
            st.markdown(summary)
            st.download_button(
                "Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain",
                key="download_summary"
            )
        else:
            st.info("The summary has not been generated.")

    with tab4:
        st.subheader("Translated Texts")
        translations = results["translations"]

        if translations:
            st.markdown(translations)
            st.download_button(
                "Download Translations",
                data=translations,
                file_name="translations.txt",
                mime="text/plain",
                key="download_translations"
            )
        else:
            st.info("Translations are not available.")

    with tab5:
        st.subheader("Translation Evaluation")
        evaluation = results["evaluation"]

        if evaluation:
            st.markdown(evaluation)
            st.download_button(
                "Download Evaluation",
                data=evaluation,
                file_name="evaluation.txt",
                mime="text/plain",
                key="download_evaluation"
            )
        else:
            st.info("The evaluation is not available.")
