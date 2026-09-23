# 🎓 AI Study Assistant — Azure AI Foundry

> An intelligent, document-grounded AI study assistant that helps students learn from their own study material using Azure AI Foundry, AI Agents, File Search, and GPT-4.1-mini.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Microsoft-Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Microsoft Azure">
  <img src="https://img.shields.io/badge/Azure%20AI-Foundry-0078D4?style=for-the-badge" alt="Azure AI Foundry">
  <img src="https://img.shields.io/badge/Model-GPT--4.1--mini-412991?style=for-the-badge" alt="GPT-4.1-mini">
</p>

---

## 📌 Overview

**AI Study Assistant** is an AI-powered academic tutor designed to help students learn directly from their uploaded study material.

Instead of relying on unrestricted general-purpose answers, the system uses **document grounding** to retrieve relevant information from the student's uploaded material before generating a response.

This makes the assistant particularly useful for:

- 📚 Understanding lecture notes
- 📄 Asking questions about PDFs
- 🧠 Learning concepts from study material
- 📝 Generating quizzes and MCQs
- 📋 Summarizing academic material
- 🔢 Solving numerical and formula-based questions
- 🔍 Comparing concepts
- 🎯 Preparing for examinations

The core design principle is simple:

> **The student's study material is the source of truth for document-specific questions.**

---

# ✨ Key Features

## 📄 1. PDF Study Material Upload

Students can upload their study material as a PDF.

The backend:

1. Receives the PDF.
2. Creates a vector store.
3. Uploads the document.
4. Indexes the document for retrieval.
5. Creates a study session.
6. Makes the material available to the AI agent through File Search.

This allows the assistant to answer questions based on the student's actual material.

---

## 🤖 2. Azure AI Foundry Agent

The project uses an AI agent created through **Azure AI Foundry**.

The agent is configured using:

- Azure AI Projects SDK
- `AIProjectClient`
- `DefaultAzureCredential`
- `PromptAgentDefinition`
- `FileSearchTool`
- Structured inputs
- GPT-4.1-mini

The agent is created through:

```text
Setup_agent.py
