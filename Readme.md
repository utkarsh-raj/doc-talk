# DocTalk - Your AI-Powered Document Chat Assistant

## Overview

DocTalk is a web application that allows you to upload document transcripts and then chat with an AI about the content of those documents. It's designed to help you quickly find information and get answers from your documents in a conversational manner.

## Features

* **Document Upload:** Upload new document transcripts to the application.
* **Chat Interface:** Chat with an AI assistant about the content of your uploaded documents.
* **AI-Powered Search:** The application uses AI to understand your questions and provide relevant answers from the documents.
* **Real-time Interaction:** Engage in a dynamic conversation with the AI.
* **FastAPI Backend:** The application is built using FastAPI, a modern, high-performance web framework.

## Technologies Used

DocTalk is built using a combination of powerful technologies:

* **Backend:**
    * [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python 3.7+
    * [Uvicorn](https://www.uvicorn.org/): An ASGI server for running the FastAPI application.
    * [Sentence Transformers](https://www.sbert.net/): A library used to generate sentence embeddings, which are numerical representations of text used for semantic search.
    * [Chroma](https://www.trychroma.com/): A vector database for storing and querying the sentence embeddings.
    * [OpenAI](https://openai.com/): The OpenAI API is used for generating chat responses.
    * [NLTK](https://www.nltk.org/): The Natural Language Toolkit is used for text processing, specifically for splitting the uploaded text into sentences.
    * [Python-dotenv](https://github.com/theskumar/python-dotenv): This library is used for managing environment variables.
* **Frontend**: React
    * [React](https://react.dev/): A JavaScript library for building user interfaces

## Installation

### Prerequisites

Before you begin, make sure you have the following installed:

* Python 3.7+
* pip (Python package installer)
* Node.js
* npm (Node.js package manager)

### Backend Setup

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd doctalk
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the backend dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    * Create a file named `.env` in the `app` directory.
    * Add your OpenAI API key to the `.env` file:

        ```
        OPENAI_API_KEY=your_openai_key
        CHROMA_PERSIST_DIR=your_path_to_db
        LLM_PROVIDER=openai (or ollama)
        OLLAMA_BASE_URL=base_url_ollame (if using ollama)
        OLLAMA_MODEL=llama_model (if using ollama)
        OPENAI_MODEL=gpt-4o-mini
        PORT=8000

        ```

        * The `LLM_PROVIDER` variable specifies which LLM provider to use. It defaults to `ollama`, but you can set it to `openai` if you prefer to use OpenAI.
        * `CHROMA_PERSIST_DIR` specifies the directory where Chroma will store the database files. The default is `chroma_db`.

5.  **Run the backend:**

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    This will start the FastAPI server. The `--reload` flag enables hot reloading, so the server will automatically restart when you make changes to the code.