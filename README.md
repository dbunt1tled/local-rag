# Local RAG Application

A Streamlit-based Retrieval-Augmented Generation (RAG) application that allows you to interact with your documents using natural language queries. The application uses local language models and vector databases for private, offline document processing and question-answering.

## Local RAG
- LLM Models: **llama3.2**
- LLM Embedding Model: **nomic-embed-text**
## Features

- **Document Processing**: Upload and process various document formats
- **Vector Database**: Local vector storage for efficient document retrieval
- **Natural Language Queries**: Ask questions in natural language about your documents
- **Offline-First**: All processing happens locally on your machine
- **Web Interface**: User-friendly Streamlit interface for easy interaction

## Prerequisites

- Python 3.13+
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd local-rag
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file and update it with your configuration:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your preferred settings.

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run Home.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload your documents and start querying!

## Project Structure

```
.
├── app/                    # Main application package
│   ├── message/            # Message handling components
│   └── ...                 # Other application modules
├── internal/               # Internal application code
├── migration/              # Database migration scripts
├── .env                    # Environment variables
├── .gitignore             # Git ignore file
├── alembic.ini            # Alembic configuration
├── app.py                 # Main application entry point
├── pyproject.toml         # Python project configuration
├── README.md              # This file
└── requirements.txt       # Project dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the repository.

---

*This project was built with ❤️ using Streamlit, Langchain and other amazing open-source tools.*
