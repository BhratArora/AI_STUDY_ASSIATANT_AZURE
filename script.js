// ============================================================
// DOM ELEMENTS
// ============================================================

const pdfInput =
    document.getElementById("pdfInput");

const uploadButton =
    document.getElementById("uploadButton");

const uploadStatus =
    document.getElementById("uploadStatus");

const selectedFileName =
    document.getElementById(
        "selectedFileName"
    );

const documentName =
    document.getElementById(
        "documentName"
    );

const chatBox =
    document.getElementById(
        "chatBox"
    );

const questionInput =
    document.getElementById(
        "questionInput"
    );

const askButton =
    document.getElementById(
        "askButton"
    );


// ============================================================
// FILE SELECTION
// ============================================================

pdfInput.addEventListener(
    "change",
    function () {

        const file =
            pdfInput.files[0];

        if (!file) {

            selectedFileName.textContent =
                "No file selected";

            selectedFileName.classList.remove(
                "file-selected"
            );

            return;
        }


        if (
            !file.name
                .toLowerCase()
                .endsWith(".pdf")
        ) {

            selectedFileName.textContent =
                "Please select a PDF file.";

            selectedFileName.classList.remove(
                "file-selected"
            );

            pdfInput.value = "";

            return;
        }


        selectedFileName.textContent =
            file.name;

        selectedFileName.classList.add(
            "file-selected"
        );


        uploadStatus.textContent =
            "";

    }
);


// ============================================================
// UPLOAD PDF
// ============================================================

uploadButton.addEventListener(
    "click",
    uploadPDF
);


async function uploadPDF() {

    const file =
        pdfInput.files[0];


    // No file

    if (!file) {

        uploadStatus.textContent =
            "Please select a PDF first.";

        return;
    }


    // Validate PDF

    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        uploadStatus.textContent =
            "Please select a PDF file.";

        return;
    }


    // Disable controls

    uploadButton.disabled =
        true;

    pdfInput.disabled =
        true;


    // Uploading state

    uploadButton.innerHTML =
        `
        <span class="button-spinner"></span>
        Uploading...
        `;


    uploadStatus.textContent =
        "Uploading and indexing your PDF...";


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Upload failed."
            );

        }


        // Successful upload

        uploadStatus.innerHTML =
            `
            <span class="success-icon">
                ✓
            </span>

            PDF uploaded and indexed successfully.
            `;


        documentName.textContent =
            data.file_name;


        // Reset chat

        chatBox.innerHTML =
            `
            <div class="welcome-message">

                <div class="welcome-icon">
                    ✦
                </div>

                <h3>
                    Document ready
                </h3>

                <p>
                    Your study material has been indexed.
                    Ask a question to begin.
                </p>

                <div class="suggestion-row">

                    <span>
                        Explain a concept
                    </span>

                    <span>
                        Summarize a topic
                    </span>

                    <span>
                        Generate questions
                    </span>

                </div>

            </div>
            `;


        // Focus question box

        questionInput.focus();


    } catch (error) {

        console.error(
            "Upload error:",
            error
        );


        uploadStatus.innerHTML =
            `
            <span style="color:#f87171;">
                Upload failed:
            </span>

            ${escapeHTML(error.message)}
            `;

    } finally {

        // Re-enable controls

        uploadButton.disabled =
            false;

        pdfInput.disabled =
            false;


        uploadButton.innerHTML =
            `
            Upload & Analyze
            <span>→</span>
            `;

    }

}


// ============================================================
// ASK QUESTION
// ============================================================

askButton.addEventListener(
    "click",
    askQuestion
);


// Enter = Send
// Shift + Enter = New line

questionInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askQuestion();

        }

    }
);


async function askQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {

        return;

    }


    // Display user message

    addMessage(
        question,
        "user"
    );


    // Clear input

    questionInput.value =
        "";


    // Disable Ask button

    askButton.disabled =
        true;


    // Show thinking state

    const loadingMessage =
        addMessage(
            "Thinking...",
            "ai"
        );


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question:
                            question
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );

        }


        // Remove thinking message

        loadingMessage.remove();


        // Display AI response

        addMessage(
            data.answer,
            "ai"
        );


    } catch (error) {

        console.error(
            "Question error:",
            error
        );


        loadingMessage.remove();


        addMessage(
            "Error: " +
            error.message,
            "ai"
        );

    } finally {

        // Re-enable Ask button

        askButton.disabled =
            false;


        questionInput.focus();

    }

}


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(
    message,
    type
) {

    const messageDiv =
        document.createElement(
            "div"
        );


    messageDiv.classList.add(
        "message"
    );


    if (type === "user") {

        messageDiv.classList.add(
            "user-message"
        );

    } else {

        messageDiv.classList.add(
            "ai-message"
        );

    }


    const content =
        document.createElement(
            "div"
        );


    content.classList.add(
        "message-content"
    );


    if (type === "ai") {

        // Render Markdown

        if (
            typeof marked !==
            "undefined"
        ) {

            content.innerHTML =
                marked.parse(
                    message
                );

        } else {

            content.textContent =
                message;

        }

    } else {

        // User messages are
        // inserted as plain text

        content.textContent =
            message;

    }


    messageDiv.appendChild(
        content
    );


    chatBox.appendChild(
        messageDiv
    );


    // Scroll to newest message

    chatBox.scrollTop =
        chatBox.scrollHeight;


    return messageDiv;

}


// ============================================================
// HTML ESCAPE HELPER
// ============================================================

function escapeHTML(
    text
) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}