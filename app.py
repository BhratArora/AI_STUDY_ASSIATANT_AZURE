import os
import tempfile

from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

FOUNDRY_PROJECT_ENDPOINT = os.getenv(
    "FOUNDRY_PROJECT_ENDPOINT"
)

FOUNDRY_AGENT_NAME = os.getenv(
    "FOUNDRY_AGENT_NAME"
)

if not FOUNDRY_PROJECT_ENDPOINT:
    raise ValueError(
        "FOUNDRY_PROJECT_ENDPOINT not found in .env"
    )

if not FOUNDRY_AGENT_NAME:
    raise ValueError(
        "FOUNDRY_AGENT_NAME not found in .env"
    )


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)

CORS(app)


# ============================================================
# CONNECT TO MICROSOFT FOUNDRY
# ============================================================

project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

openai = project.get_openai_client()


# ============================================================
# CURRENT STUDY SESSION
# ============================================================

current_vector_store_id = None
current_file_name = None
conversation = None


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "message": "AI Study Assistant backend is running."
    })


# ============================================================
# UPLOAD PDF
# ============================================================

@app.route("/upload", methods=["POST"])
def upload_pdf():

    global current_vector_store_id
    global current_file_name
    global conversation

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if "file" not in request.files:

        return jsonify({
            "error": "No PDF file was uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "error": "No file selected."
        }), 400

    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error": "Only PDF files are supported."
        }), 400

    try:

        print("\n========================================")
        print("NEW PDF UPLOAD")
        print("========================================")

        print("File:", file.filename)


        # ----------------------------------------------------
        # CREATE VECTOR STORE
        # ----------------------------------------------------

        print("\nCreating vector store...")

        vector_store = openai.vector_stores.create(
            name="StudentStudyMaterial"
        )

        print(
            "Vector store:",
            vector_store.id
        )


        # ----------------------------------------------------
        # TEMPORARILY SAVE PDF
        # ----------------------------------------------------

        print("\nPreparing PDF for upload...")

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_path = temp_file.name

                file.save(temp_path)


            # ------------------------------------------------
            # UPLOAD PDF TO FOUNDRY
            # ------------------------------------------------

            print(
                "Uploading PDF to Foundry..."
            )

            with open(
                temp_path,
                "rb"
            ) as pdf_file:

                vector_store_file = (
                    openai.vector_stores.files.upload_and_poll(
                        vector_store_id=vector_store.id,
                        file=pdf_file
                    )
                )

        finally:

            # ------------------------------------------------
            # DELETE TEMPORARY LOCAL COPY
            # ------------------------------------------------

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                os.remove(temp_path)


        # ----------------------------------------------------
        # UPLOAD SUCCESSFUL
        # ----------------------------------------------------

        print(
            "\nPDF indexed successfully."
        )

        print(
            "File ID:",
            vector_store_file.id
        )


        # ----------------------------------------------------
        # SAVE CURRENT SESSION
        # ----------------------------------------------------

        current_vector_store_id = vector_store.id

        current_file_name = file.filename


        # ----------------------------------------------------
        # CREATE NEW CONVERSATION
        # ----------------------------------------------------

        conversation = (
            openai.conversations.create()
        )


        print(
            "\nStudy session ready."
        )


        return jsonify({

            "success": True,

            "message":
                "PDF uploaded and indexed successfully.",

            "file_name":
                current_file_name,

            "vector_store_id":
                current_vector_store_id

        })


    except Exception as e:

        print("\nUPLOAD ERROR:")

        print(str(e))

        return jsonify({

            "error":
                str(e)

        }), 500


# ============================================================
# ASK QUESTION
# ============================================================

@app.route("/ask", methods=["POST"])
def ask_question():

    global current_vector_store_id
    global conversation


    # --------------------------------------------------------
    # CHECK WHETHER A PDF HAS BEEN UPLOADED
    # --------------------------------------------------------

    if current_vector_store_id is None:

        return jsonify({

            "error":
                "Please upload a PDF first."

        }), 400


    # --------------------------------------------------------
    # READ REQUEST
    # --------------------------------------------------------

    data = request.get_json()

    if (
        not data
        or "question" not in data
    ):

        return jsonify({

            "error":
                "Question is required."

        }), 400


    question = data["question"].strip()


    if not question:

        return jsonify({

            "error":
                "Question cannot be empty."

        }), 400


    try:

        print("\n========================================")
        print("STUDENT QUESTION")
        print("========================================")

        print(question)


        # ----------------------------------------------------
        # SEND QUESTION TO FOUNDRY AGENT
        # ----------------------------------------------------

        response = openai.responses.create(

            conversation=conversation.id,

            input=question,

            extra_body={

                "agent_reference": {

                    "type":
                        "agent_reference",

                    "name":
                        FOUNDRY_AGENT_NAME

                },

                "structured_inputs": {

                    "vector_store_id":
                        current_vector_store_id

                }

            }

        )


        # ----------------------------------------------------
        # GET ANSWER
        # ----------------------------------------------------

        answer = response.output_text


        print("\n========================================")
        print("AI STUDY ASSISTANT")
        print("========================================")

        print(answer)


        # ----------------------------------------------------
        # SEND ANSWER TO FRONTEND
        # ----------------------------------------------------

        return jsonify({

            "success":
                True,

            "answer":
                answer

        })


    except Exception as e:

        print("\nQUESTION ERROR:")

        print(str(e))

        return jsonify({

            "error":
                str(e)

        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("       AI STUDY ASSISTANT SERVER")
    print("========================================")

    print("\nServer running at:")

    print(
        "http://127.0.0.1:5000"
    )

    print(
        "\nWaiting for requests..."
    )


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )