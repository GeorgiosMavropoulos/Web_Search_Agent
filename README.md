# AI Web Research & Translation Pipeline

An AI-powered research tool built with Python and LangChain Expression Language (LCEL). It searches the web for relevant information, extracts text from web pages, summarizes the collected content, translates the final summary and then another LLM judges the whole workflow.

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

### 6. Streamlit Visualization
Implemented a simple Streamlit WebPage with a chatbox to enable users interact with the agent.

### 7. LLM as a judge
Final another LLM is being called to judge the quality of the workflow.

 
 
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
    |
    v
Judgement

```

### Step 1: User Input

The user provides two inputs:

- **Research question:** The topic or question to investigate.

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

The previous research summary is passed to a translation chain along with the target language.

The language model produces the translated result.

### Step 6: LLM as a Judge

Another LLM is being called to judge the results. The LLM receives the initial question, the scraped text, the summary, the report and the translation.

## Technologies

The project uses the following technologies and libraries.
```
| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | Framework for building language model applications |
| LCEL | Composing and connecting runnable components |
| Language model API | Generating summaries and translations |
| DuckDuckGo Search | Finding relevant web pages |
| Beautiful Soup | Extracting readable content from web pages |
| python-dotenv | Loading environment variables from a `.env` file |
| streamlit | GUI visualization
```

## Project Structure

### File Responsibilities
```
- app.py: Entry point that launches the Streamlit GUI to display all results.
- inference.py: Main backend entry point implementing the inference class that runs the complete workflow.
- llm/: Contains the LLM setup and safety checks.
- prompts/: Stores the prompt templates used across the workflows.
- llm_as_a_judge_chain/: Defines the LLM-as-a-judge evaluation chain.
- scrapper_chain/: Defines the chain logic for scraping content.
- summary_chain/: Defines the summarization chain.
- translation_chain/: Defines the translation chain.
- websearch_chain/: Defines the search-related chain logic.
- web_scrap/: Contains the web page extraction functionality.
-  web_search/: Contains the web search functionality.
- utilities/: Contains helper modules, such as the parser to convert JSON objects to Python dictionaries.
• pyproject.toml & requirements.txt: List the project configuration and Python dependencies.
• .python-version: Specifies the Python version for the environment.
• .gitignore: Specifies intentionally untracked files to ignore in Git.
• README.md: Documents the project..

```
## Installation

### Prerequisites

Before running the project, make sure you have:

- Python 3.10 or a compatible version supported by your chosen dependencies.
- pip installed.
- Access to a supported language model API, if your selected model requires one.
- An internet connection for web search and page retrieval.

### 1. Clone the Repository

```bash
git clone https://github.com/GeorgiosMavropoulos/Web_Search_Agent
cd Web_Search_Agent
```


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



```bash
pip install -r requirements.txt
```



### 4. Configure Environment Variables

Create a `.env` file in the project root.

I used GEMINI:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL= gemini-3.8-flash-lite

```

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


## Usage
From the main root:
```streamlit run app.py```

1. Start the application.
2. Enter a research question.
3. Allow the search component to retrieve relevant URLs.
4. Extract and summarize the content.
5. Translate the final summary.
6. Read the generated result.

For example, a completed run might look like this:

```text
Research question:
What are the best places to visit in Astorga, Spain?

Output:
A Greek/Italian/French language summary
historical sites, and activities in Astorga.
```


## LCEL Concepts

One of the main purposes of this project is to practice LangChain Expression Language.



## Future Improvements

- **Source citations:** Include links to the pages used to generate the summary.
- **Add Langgraph to connect nodes and edges:** Add Langgraph to replace LCEL with nodes and edges.
- **Improved summarization:** Combine individual page summaries into a coherent research report.
- **Language selection:** Support more target languages.
- **Better error handling:** Handle inaccessible URLs, empty pages, and failed model requests.
- **Token management:** Control input length and model usage costs.
- **Structured output:** Return the title, summary, key points, and source URLs in a consistent format.
- **Caching:** Avoid repeating expensive requests for previously processed content.
- **User interface:** Add a simple command-line interface or web application.
- **Evaluation:** Compare summaries and translations against the original source material.


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

This project was released under the MIT licence.
---



Built to explore LangChain Expression Language through a practical AI research workflow.
