# Document RAG API

A FastAPI-based Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions about their content.

## Overview

The application supports:

- PDF documents
- DOCX documents
- TXT documents

Uploaded documents are loaded, split into chunks, converted into embeddings using Gemini, and stored in Chroma.

Users can then ask questions about a specific document. The application retrieves relevant chunks and uses Gemini to generate an answer based only on the retrieved context.

## Architecture

```text
Document Upload
      |
      v
FastAPI
      |
      v
Document Service
      |
      +----> File Storage
      |
      v
Document Loader
      |
      v
Text Splitter
      |
      v
Gemini Embeddings
      |
      v
Chroma Vector Store
      |
      v
Document Metadata


Question
      |
      v
FastAPI /chat
      |
      v
Document Validation
      |
      v
Chroma Retrieval
      |
      v
Relevant Chunks
      |
      v
Gemini LLM
      |
      v
Answer + Sources