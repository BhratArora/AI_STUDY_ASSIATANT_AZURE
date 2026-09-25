🎓 StudyAI — AI Study Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Microsoft-Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Microsoft Azure">
  <img src="https://img.shields.io/badge/Azure%20AI-Foundry-0078D4?style=for-the-badge" alt="Azure AI Foundry">
  <img src="https://img.shields.io/badge/Model-GPT--4.1--mini-412991?style=for-the-badge" alt="GPT-4.1-mini">
</p>

<p align="center">
  <strong>Study smarter. Understand deeper.</strong>
</p>

<p align="center">
  An AI-powered study assistant that turns your own study material into an interactive, document-grounded tutor.
</p>

📌 Overview

StudyAI is an AI-powered academic tutor built with Microsoft Azure AI Foundry.

Students can upload their study material as a PDF and interact with it through an AI tutor. The system uses Retrieval-Augmented Generation (RAG), Vector Stores, and File Search to retrieve relevant information from the uploaded material before generating a response.

The goal is to make studying more interactive, focused, and aligned with the student's actual study material.

Core Architecture

Student
   │
   ▼
Web Frontend
HTML / CSS / JavaScript
   │
   ▼
Flask REST API
   │
   ▼
Azure AI Foundry
   │
   ├── Vector Store
   │       │
   │       └── Uploaded PDF
   │
   ├── File Search
   │
   └── AI Study Assistant Agent
              │
              ▼
         GPT-4.1-mini
              │
              ▼
       Grounded Response

🎯 Problem Statement

Students often have to switch between PDFs, notes, search engines, videos, and general-purpose AI tools while preparing for exams.

This creates three major problems:

Large amounts of study material are difficult to revise.

Generic AI answers may go beyond the student's actual study material.

Creating topic-specific practice questions manually takes time.

StudyAI addresses these problems by connecting an AI tutor directly to the student's uploaded study material.

💡 Solution

StudyAI provides a single learning workflow:

📄 Upload Study Material
          ↓
🔎 Index the Document
          ↓
🤖 Ask the AI Tutor
          ↓
📚 Retrieve Relevant Content
          ↓
🧠 Generate a Grounded Explanation
          ↓
📝 Practice with MCQs
          ↓
🎯 Revise and Learn

For document-specific questions, the uploaded study material is treated as the primary source of information.

✨ Key Features

📄 1. PDF Study Material Upload

Students can upload their study material in PDF format.

The backend:

Receives the PDF.

Creates a vector store.

Uploads the document.

Indexes the document.

Creates a study session.

Connects the material to the AI agent through File Search.

The uploaded PDF is processed for retrieval rather than being manually copied into every conversation.

🔎 2. Retrieval-Augmented Generation (RAG)

StudyAI uses a RAG-based architecture.

Instead of asking the model to answer purely from its general knowledge, the system first retrieves relevant information from the student's uploaded document.

Student Question
       ↓
Azure AI Foundry Agent
       ↓
File Search
       ↓
Relevant Document Content
       ↓
GPT-4.1-mini
       ↓
Grounded Answer

This helps keep document-specific responses relevant to the material the student is actually studying.

🤖 3. Azure AI Foundry Agent

The project uses an AI agent configured through Azure AI Foundry.

The agent uses:

AIProjectClient

DefaultAzureCredential

PromptAgentDefinition

FileSearchTool

GPT-4.1-mini

Custom academic-tutor instructions

The agent configuration is handled by:

setup_agent.py

🧠 4. Document-Grounded Learning

The assistant is instructed to use the uploaded study material when answering document-specific questions.

If the requested information cannot be found in the uploaded material, the assistant can indicate that it was not found instead of presenting unsupported information as if it came from the document.

This provides a more controlled learning experience than an unrestricted chatbot.

📝 5. MCQ Generation

Students can ask StudyAI to generate exam-oriented multiple-choice questions from their study material.

Generated questions can include:

Question

Four options

Topic

Difficulty

Correct answer

Explanation

Example:

Create 5 important MCQs from this topic.

This allows students to move from learning to active practice without leaving the application.

📚 6. Concept Explanations

Students can ask the tutor to explain concepts from their study material.

The assistant can organize explanations using:

Definition

Core concept

Explanation

Example

Key points

Takeaway

This is intended to make technical topics easier to understand and revise.

📋 7. Summaries

Students can request concise summaries of topics from their study material.

This is useful for:

Quick revision

Exam preparation

Reviewing lengthy notes

Identifying important concepts

⚖️ 8. Concept Comparison

StudyAI can compare concepts and present the differences in a structured format.

For example:

Aspect

Concept A

Concept B

Definition

...

...

Working

...

...

Advantages

...

...

Limitations

...

...

💬 9. Conversation Context

The application creates a study conversation so that follow-up questions can maintain context during the active study session.

For example:

Student: Explain TCP congestion control.

AI: [Explanation]

Student: What are its main phases?

AI: [Context-aware follow-up]

🛡️ 10. AI Guardrails

The agent contains explicit instructions to control its behavior.

Topic Constraint

The requested topic should remain the focus of retrieval and response generation.

Document Grounding

Document-specific answers should be based on the uploaded study material.

Out-of-Scope Handling

If information is not available in the uploaded study material, the assistant should not pretend that it found it there.

Quiz Behavior

The assistant can generate quizzes and keep answers available for evaluation when requested.

🏗️ System Architecture

flowchart TD
    A[Student] --> B[Web Frontend]
    B --> C[Flask REST API]

    C -->|Upload PDF| D[Azure AI Foundry]
    D --> E[Vector Store]
    E --> F[File Search]

    B -->|Ask Question| C
    C --> G[AI Study Assistant Agent]

    G --> F
    F --> H[Relevant Study Material]
    H --> G

    G --> I[GPT-4.1-mini]
    I --> C
    C --> B
    B --> A

🔄 End-to-End Workflow

Step 1 — Upload

The student selects a PDF from the web interface.

Student → Frontend → Flask

Step 2 — Document Processing

The backend uploads the document and creates a vector store for retrieval.

PDF
 ↓
Vector Store
 ↓
Indexed Study Material

Step 3 — File Search

When a question is asked, the agent uses File Search to retrieve relevant information.

Question
 ↓
File Search
 ↓
Relevant Content

Step 4 — AI Generation

The retrieved information is supplied to the AI agent and GPT-4.1-mini generates the response.

Step 5 — Response

The Flask backend returns the response to the frontend, where it is rendered for the student.

🖥️ Application

The frontend is built using:

HTML5

CSS3

JavaScript

Markdown rendering

The interface provides:

PDF upload

Chat-based interaction

AI responses

Grounding status

Structured Markdown responses

🔌 API

GET /

Health check endpoint used to verify that the Flask backend is running.

POST /upload

Uploads and processes a study PDF.

Flow

PDF
 ↓
Flask
 ↓
Vector Store
 ↓
File Search
 ↓
Study Session

POST /ask

Sends a student question to the AI Study Assistant.

Example Request

{
  "question": "Explain TCP congestion control."
}

Flow

Question
 ↓
Flask
 ↓
Azure AI Foundry Agent
 ↓
File Search
 ↓
GPT-4.1-mini
 ↓
Answer

🧰 Technology Stack

Layer

Technology

Frontend

HTML5, CSS3, JavaScript

Backend

Python, Flask

API

Flask REST API

CORS

Flask-CORS

Configuration

python-dotenv

Cloud Platform

Microsoft Azure

AI Platform

Azure AI Foundry

Agent SDK

Azure AI Projects SDK

AI Model

GPT-4.1-mini

Retrieval

RAG + File Search

Document Indexing

Vector Store

Authentication

DefaultAzureCredential

📁 Project Structure

AI_STUDY_ASSIATANT_AZURE/
│
├── app.py
│   └── Flask backend
│       ├── PDF upload
│       ├── Vector store creation
│       ├── Document indexing
│       ├── Study session management
│       └── Question answering
│
├── setup_agent.py
│   └── Azure AI Foundry agent setup
│       ├── Agent configuration
│       ├── Agent instructions
│       ├── File Search configuration
│       └── Agent version creation
│
├── frontend files
│   ├── HTML
│   ├── CSS
│   └── JavaScript
│
├── README.md
├── LICENSE
└── .gitignore

⚙️ Setup

Prerequisites

Python 3.x

Git

Azure subscription

Azure AI Foundry project

GPT-4.1-mini deployment

Azure CLI

1. Clone the Repository

git clone https://github.com/BhratArora/AI_STUDY_ASSIATANT_AZURE.git

cd AI_STUDY_ASSIATANT_AZURE

2. Create a Virtual Environment

Windows

python -m venv .venv

.venv\Scripts\activate

macOS / Linux

python3 -m venv .venv

source .venv/bin/activate

3. Install Dependencies

pip install flask flask-cors python-dotenv azure-identity azure-ai-projects

🔐 Azure Authentication

The project uses Azure's credential chain through:

DefaultAzureCredential()

For local development:

az login

Make sure your Azure account has access to the required Azure AI Foundry project.

🔑 Environment Variables

Create a .env file in the project root.

Example:

FOUNDRY_PROJECT_ENDPOINT=your_foundry_project_endpoint
FOUNDRY_AGENT_NAME=your_agent_name

⚠️ Never commit secrets

Do not upload:

.env
API keys
Access tokens
Azure credentials
Passwords

Make sure .env is included in .gitignore.

🤖 Agent Setup

Run the agent setup script:

python setup_agent.py

This configures the AI Study Assistant agent in Azure AI Foundry with its instructions and File Search capability.

▶️ Run the Backend

Start the Flask application:

python app.py

The backend will be available at:

http://127.0.0.1:5000

Open the frontend in your browser to start a study session.

🧪 Example Session

Upload

Computer_Networks.pdf

Ask

Explain CSMA/CD.

Practice

Create 5 important MCQs from this topic.

Revise

Summarize this topic for my exam.

The assistant retrieves relevant information from the uploaded material before generating its response.

🚀 Current Implementation

PDF upload

Vector store creation

Document indexing

File Search

Azure AI Foundry agent

GPT-4.1-mini

Document-grounded question answering

Concept explanations

MCQ generation

Summaries

Concept comparisons

Conversation context

Markdown responses

Topic constraints

Out-of-scope handling

Azure authentication through DefaultAzureCredential

🛣️ Future Scope

Planned improvements include:

Multiple PDFs per user

Persistent user study sessions

Page-level citations

Interactive quiz scoring

Personalized learning analytics

Progress tracking

Improved session management

Production deployment

Azure App Service deployment

🔮 Vision

StudyAI aims to turn static study material into an interactive learning environment.

📄 Study Material
       ↓
🔎 Retrieve
       ↓
🤖 Understand
       ↓
💬 Ask
       ↓
📝 Practice
       ↓
🎯 Revise

The long-term vision is a study assistant that can understand a student's material, explain difficult concepts, generate targeted practice, and support the complete learning cycle.

👥 Team Project

StudyAI — AI Study Assistant

Built using:

Microsoft Azure • Azure AI Foundry • Python • Flask • JavaScript • RAG • AI Agents

📜 License

This project is licensed under the MIT License.

See the LICENSE file for details.

<p align="center">
  <strong>🎓 StudyAI</strong><br>
  Study smarter. Understand deeper.
</p>
