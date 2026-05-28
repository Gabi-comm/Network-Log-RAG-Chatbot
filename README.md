# Network-Log-RAG-Chatbot
An intelligent log analysis system that uses embeddings to index network logs into a vector database (ChromaDB), allowing a local Language Model chatbot (Ollama) to query, analyze, and detect security anomalies.

# Embedded Network Log Model with LLM Chatbot

An intelligent, privacy-first network log analysis system. This project implements a Retrieval-Augmented Generation (RAG) pipeline that embeds raw network security logs, stores them in a vector database, and pairs them with a local Large Language Model (LLM) chatbot for interactive, natural-language security analysis.

## Features
* **Log Embedding & Ingestion:** Uses Hugging Face embedding models to transform unstructured network logs into dense vector representations.
* **Vector Storage (ChromaDB):** Stores embedded log data locally for rapid, semantic similarity search.
* **Local LLM Integration (Ollama):** Queries the embedded logs using an open-source, local language model to ensure data privacy and security.
* **Interactive Chat Interface:** Allows security analysts to query complex network behavior, trace anomalies, and generate incident summaries using natural language.

## Tech Stack
* **Language:** Python 3.14+
* **Framework:** LangChain
* **Embeddings:** Hugging Face (`langchain-huggingface`)
* **Vector DB:** ChromaDB
* **Local LLM Engine:** Ollama

## Project Structure

The project is organized into modular scripts representing distinct phases of a Retrieval-Augmented Generation (RAG) pipeline:

* **`HR_Policies.txt`**: The raw text dataset containing simulated policy information and hidden PII.
* **`redact.py`**: Pre-processing script used to scan the raw text, detect sensitive information (like SSNs or emails), and clean it.
* **`embed.py`**: Loads the sanitized data, splits it into digestible text chunks, generates vector embeddings, and stores them in ChromaDB.
* **`retriever.py`**: Handles semantic search logic-taking a user query and fetching the most relevant document chunks from the vector database.
* **`chatbot.py`**: The final execution script that wraps the retriever and links it to Ollama, providing an interactive natural language chat interface.
