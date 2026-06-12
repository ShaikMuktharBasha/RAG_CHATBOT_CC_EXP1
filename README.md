# Employee Handbook Assistant

A professional ChatGPT-style web application built with Streamlit and Python that acts as an intelligent assistant for your company's Employee Handbook. It uses Retrieval-Augmented Generation (RAG) to answer questions based on the uploaded PDF document.

## Features

- **Professional UI**: Clean, corporate-styled dashboard with a sidebar and main chat area.
- **RAG Architecture**: Uses LangChain, FAISS, MiniLM embeddings, and DistilBERT for accurate question answering.
- **PDF Processing**: Upload and process your employee handbook PDF directly in the app.
- **Chat History**: Maintains conversation history during the session.
- **Transparency**: Shows confidence scores and the exact context retrieved from the handbook for every answer.
- **Responsive**: Modern dark-mode compatible design with custom CSS.

## Setup Instructions

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    cd employee_handbook_assistant
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

1.  Open the application in your browser (usually http://localhost:8501).
2.  In the sidebar, upload your Employee Handbook PDF.
3.  Click "Process Document". The assistant will split the text and create a vector index.
4.  Once the system status shows "🟢 System Ready", start asking questions in the main chat area!
