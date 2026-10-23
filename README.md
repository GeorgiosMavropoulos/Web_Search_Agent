# AI Web Research & Translation Pipeline

An AI-powered research tool built with Python and LangChain Expression Language (LCEL). It searches the web for relevant information, extracts text from web pages, summarizes the collected content, and translates the final summary into a language of your choice.

This project is designed as a hands-on learning project for understanding how to build modular AI workflows with LangChain and LCEL.

## Table of Contents

- [Overview](#overview)
- [Project Goals](#project-goals)
- [Features](#features)
- [How It Works](#how-it-works)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [LCEL Concepts](#lcel-concepts)
- [Error Handling and Limitations](#error-handling-and-limitations)
- [Future Improvements](#future-improvements)
- [Learning Objectives](#learning-objectives)
- [License](#license)

## Overview

Finding useful information online often requires visiting multiple websites, reading long articles, extracting relevant details, and translating information into another language.

The AI Web Research & Translation Pipeline aims to simplify this process by combining web search, web scraping, text summarization, and machine translation into a single workflow.

The user provides a research question and a target language. The application searches for relevant web pages, extracts their content, generates a summary, and translates the result.

The workflow is built using small, independent components that can be connected and reused through LCEL.

## Project Goals

The main goals of this project are to:

- Automate basic web research.
- Extract readable text from web pages.
- Summarize information using a language model.
- Translate summaries into a user-selected language.
- Build a modular pipeline using LangChain Expression Language.
- Practice connecting Python functions and LangChain components.
- Understand how data flows between different stages of an AI application.

## Features

### 1. Web Search

Search the web using a user-provided research question.

The search component returns a list of relevant URLs that can be processed by the following stages.

### 2. Web Scraping

Retrieve the content of selected web pages and extract readable text.

The goal is to focus on the main content rather than unnecessary HTML elements, such as navigation menus and scripts.

### 3. Text Summarization

Pass the extracted text to a language model to generate a concise summary.

The summary can focus on the most relevant information related to the original research question.

### 4. Translation

Translate the generated summary into a target language specified by the user.

For example, the application could research a topic using English-language sources and return a summary in Greek.

### 5. LCEL Pipeline

Connect the individual components into a single workflow using LangChain Expression Language.

Each stage has a specific responsibility, making the application easier to understand, test, and extend.

## How It Works

The application follows a sequential research pipeline.

```text
User Input
    |
    v
Web Search
    |
    v
List of URLs
    |
    v
Web Scraping
    |
    v
Extracted Text
    |
    v
Text Summarization
    |
    v
Generated Summary
    |
    v
Translation
    |
    v
Final Translated Summary
```

### Step 1: User Input

The user provides two inputs:

- **Research question:** The topic or question to investigate.
- **Target language:** The language in which the final summary should be returned.

Example:

```text
Research question:
What are the main benefits of renewable energy?

Target language:
Greek
```

### Step 2: Web Search

The search component uses the research question to find relevant web pages.

The output is a list of URLs.

### Step 3: Web Scraping

The scraper visits the selected URLs and extracts their readable text.

Each page can be processed independently, allowing the workflow to handle multiple sources.

### Step 4: Summarization

The extracted content is passed to a summarization chain.

The language model generates a shorter version of the source material while preserving its main ideas.

For multiple sources, their summaries can be combined into a single research summary.

### Step 5: Translation

The final research summary is passed to a translation chain along with the target language.

The language model produces the translated result.

### Step 6: Final Output

The application returns the translated summary to the user.

The intended result is a concise overview of the research topic without requiring the user to read every source in full.

## Technologies

The project uses the following technologies and libraries.

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | Framework for building language model applications |
| LCEL | Composing and connecting runnable components |
| Language model API | Generating summaries and translations |
| DuckDuckGo Search | Finding relevant web pages |
| Trafilatura or Beautiful Soup | Extracting readable content from web pages |
| python-dotenv | Loading environment variables from a `.env` file |

The exact libraries and model provider may vary depending on the implementation.

## Project Structure

A possible project structure is:

```text
ai-web-research/
│
├── main.py
│
├── chains/
│   ├── search_chain.py
│   ├── summarization_chain.py
│   └── translation_chain.py
│
├── tools/
│   ├── web_search.py
│   └── scraper.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### File Responsibilities

- `main.py`: Entry point that runs the complete workflow.
- `chains/search_chain.py`: Defines the search-related chain logic.
- `chains/summarization_chain.py`: Defines the summarization prompt and chain.
- `chains/translation_chain.py`: Defines the translation prompt and chain.
- `tools/web_search.py`: Contains the web search functionality.
- `tools/scraper.py`: Contains the web page extraction functionality.
- `.env`: Stores API credentials and configuration values.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: Documents the project.

This structure is a suggested starting point and can be adjusted as the project evolves.

## Installation

### Prerequisites

Before running the project, make sure you have:

- Python 3.10 or a compatible version supported by your chosen dependencies.
- pip installed.
- Access to a supported language model API, if your selected model requires one.
- An internet connection for web search and page retrieval.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-web-research.git
cd ai-web-research
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository name if necessary.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

If you have already created a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by your implementation. For example:

```bash
pip install langchain langchain-core langchain-community
pip install langchain-openai python-dotenv trafilatura
pip install duckduckgo-search
```

Package requirements can differ depending on the search integration, scraper, and model provider you choose. Use the current package documentation to verify the appropriate dependencies.

### 4. Configure Environment Variables

Create a `.env` file in the project root.

For example, if you use an OpenAI-compatible LangChain integration:

```env
OPENAI_API_KEY=your_api_key_here
```

Add other configuration variables if your implementation requires them.

**Important:** Never commit API keys or other secrets to GitHub.

## Configuration

The application can be configured to control the research process.

Possible configuration options include:

| Setting | Description |
|---|---|
| Research question | The topic to investigate |
| Maximum search results | The maximum number of URLs to retrieve |
| Target language | The language used for the final translation |
| Summary length | The desired level of detail in the summary |
| Model | The language model used for summarization and translation |

For an initial version, keep the configuration simple. Additional settings can be introduced when the core pipeline works reliably.

## Usage

The exact usage depends on how the entry point is implemented.

Once the application is configured, the intended workflow is:

1. Start the application.
2. Enter a research question.
3. Specify the target language.
4. Allow the search component to retrieve relevant URLs.
5. Extract and summarize the content.
6. Translate the final summary.
7. Read the generated result.

For example, a completed run might look like this:

```text
Research question:
What are the best places to visit in Astorga, Spain?

Target language:
Greek

Output:
A Greek-language summary of the main attractions,
historical sites, and activities in Astorga.
```

This is an example of the intended interaction, not a claim about an already implemented command-line interface.

## LCEL Concepts

One of the main purposes of this project is to practice LangChain Expression Language.

### Runnable Composition

The pipe operator (`|`) connects components so that the output of one component becomes the input of the next.

Conceptually:

```python
chain = component_a | component_b | component_c
```

This makes it possible to organize the workflow into smaller, reusable stages.

### RunnableLambda

`RunnableLambda` allows ordinary Python functions to be used as part of an LCEL pipeline.

It is useful for operations such as processing search results, extracting values from dictionaries, or formatting data between chains.

### RunnablePassthrough

`RunnablePassthrough` passes its input through without changing it.

It can be useful when the original research question or other input data must remain available to later stages.

### RunnableParallel

`RunnableParallel` runs multiple runnable components using the same input and collects their results into a dictionary.

For example, it could be used to generate a summary and extract key points independently from the same source text.

### Runnable `.map()`

The `.map()` method applies a runnable to each item in a list of inputs.

In this project, it can be useful for processing multiple URLs or summarizing several extracted documents.

### StrOutputParser

`StrOutputParser` converts a language model's message output into a plain string.

This is useful when one chain needs to pass its generated text to another chain.

### Invoke and Stream

The project can use `.invoke()` to execute a chain and retrieve its result.

The `.stream()` method can be explored later to process output incrementally when the selected runnable and model support streaming.

## Error Handling and Limitations

Web research pipelines depend on external services and websites, so some failures are expected.

### Web Search Failures

Search services may return no results, encounter rate limits, or change their response formats.

The application should handle empty results gracefully.

### Scraping Failures

Some websites may block automated requests, require authentication, or load their content dynamically using JavaScript.

Not every URL will produce usable text.

### Long Documents

Large web pages may exceed the model's context limits.

Possible improvements include truncating content, splitting documents into smaller chunks, or summarizing chunks before combining them.

### Inconsistent Outputs

Different LCEL components may return strings, message objects, dictionaries, or lists.

Each stage should have a clearly defined input and output format to prevent errors when connecting components.

### Summary Accuracy

Language models may omit details or generate inaccurate statements. Summaries should be treated as an aid to research rather than a substitute for the original sources.

### Translation Quality

Translations may not preserve every nuance of the original text, especially for technical terminology or culturally specific expressions.

### Source Reliability

Search results are not necessarily authoritative. Important findings should be checked against the original sources.

## Future Improvements

Once the basic pipeline is working, several improvements could be added.

- **Source citations:** Include links to the pages used to generate the summary.
- **Parallel processing:** Process multiple URLs concurrently where appropriate.
- **Improved summarization:** Combine individual page summaries into a coherent research report.
- **Language selection:** Support more target languages.
- **Better error handling:** Handle inaccessible URLs, empty pages, and failed model requests.
- **Token management:** Control input length and model usage costs.
- **Structured output:** Return the title, summary, key points, and source URLs in a consistent format.
- **Caching:** Avoid repeating expensive requests for previously processed content.
- **User interface:** Add a simple command-line interface or web application.
- **Evaluation:** Compare summaries and translations against the original source material.

These improvements are optional and should be implemented incrementally.

## Learning Objectives

By building this project, I aim to improve my understanding of:

- Python application structure.
- LangChain and LCEL.
- Runnable composition and data flow.
- Prompt templates and output parsers.
- Integrating Python functions into LCEL chains.
- Web search and text extraction.
- Summarization and translation workflows.
- Handling multiple inputs and outputs.
- Debugging chain execution and inconsistent data structures.

The focus is on understanding how the individual components work together rather than building a complex application immediately.

## License

This project can be released under the MIT License. If you choose this license, add a `LICENSE` file containing the appropriate MIT License text.

---

**Status:** Learning project — under development.

Built to explore LangChain Expression Language through a practical AI research workflow.
