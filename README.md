<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Bot README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        pre {
            background-color: #eaeaea;
            padding: 10px;
            overflow-x: auto;
        }
        code {
            background-color: #eaeaea;
            padding: 2px 4px;
            border-radius: 4px;
        }
        a {
            color: #2980b9;
        }
        ul {
            margin-top: 0;
        }
        hr {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Medical Bot</h1>
    <p>A medical document AI assistant built with <strong>Streamlit</strong> (frontend) and <strong>FastAPI</strong> (backend). The app allows users to upload PDFs and ask medical questions. The AI retrieves relevant information and provides responses.</p>

    <hr>

    <h2>Table of Contents</h2>
    <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running-the-application">Running the Application</a></li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
        <li><a href="#notes">Notes</a></li>
    </ul>

    <hr>

    <h2 id="installation">Installation</h2>

    <h3>Option 1: Using Python</h3>
    <p>Upgrade pip:</p>
    <pre><code>pip install --upgrade pip</code></pre>

    <p>Install all dependencies:</p>
    <pre><code>pip install streamlit faiss-cpu langchain langchain_community fpdf pypdf sentence-transformers fastapi pydantic uvicorn</code></pre>

    <h3>Option 2: Using Docker</h3>
    <p>Ensure Docker and Docker Compose are installed.</p>
    <p>Build and run the containers:</p>
    <pre><code>docker-compose up --build</code></pre>

    <hr>

    <h2 id="running-the-application">Running the Application</h2>

    <h3>Streamlit Frontend</h3>
    <pre><code>streamlit run frontend/main.py</code></pre>

    <h3>FastAPI Backend</h3>
    <pre><code>uvicorn backend.main:app --host 0.0.0.0 --port 8000</code></pre>

    <hr>

    <h2 id="usage">Usage</h2>
    <ul>
        <li>Open the Streamlit app in your browser: <a href="http://localhost:8501">http://localhost:8501</a></li>
        <li>Upload PDFs or documents to the app.</li>
        <li>Enter medical queries in the chat interface.</li>
        <li>The AI agent will retrieve relevant information and provide responses.</li>
    </ul>

    <hr>

    <h2 id="project-structure">Project Structure</h2>
    <pre><code>medical_bot/
│
├── backend/
│   ├── main.py
│   └── ...
│
├── frontend/
│   ├── main.py
│   └── ...
│
├── data/
│   └── documents/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.html</code></pre>

    <hr>

    <h2 id="notes">Notes</h2>
    <ul>
        <li>Ensure all dependencies are installed before running the application.</li>
        <li>For Docker, make sure the ports 8501 (Streamlit) and 8000 (FastAPI) are available.</li>
        <li>The project is designed for educational and prototype purposes. For production, secure API keys and handle data carefully.</li>
    </ul>

</body>
</html>


