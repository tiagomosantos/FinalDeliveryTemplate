# FinalDeliveryTemplate

This repository serves as a **template** for the final project, providing a pre-structured framework to streamline development. The structure includes placeholders for key modules, assets, and utilities required for a fully functional chatbot integrated with Streamlit and LangChain.  

## Purpose  
- Offer a **starting point** for building custom chatbot applications.  
- Include reusable components for **retrieval-augmented generation (RAG)**, intent routing, and database interactions.  
- Facilitate modular design for **scalability** and **ease of customization**.  

Feel free to adapt this template to meet your specific project requirements by replacing placeholder content (e.g., `company_name/`) and adding new functionality where needed.  

## Repository Structure
```plaintext
root/
├── app.py                # Main Streamlit application script.
├── dev.py                # Development script for testing chatbot.                   
├── requirements.txt      # Python dependencies.
├── .gitignore            # Standard .gitignore file.
├── README.md             # Comprehensive project documentation.
├── company_name/         # Replace "company_name" with your company name.
│   ├──  __init__.py      # Package initialization, expose bot and dev_bot.
│   ├── chatbot/          # Chatbot modules and assets.
│   │   ├── bot.py        # Core chatbot logic.
│   │   ├── dev_bot.py    # Development chatbot for testing.
│   │   ├── memory.py     # Chatbot memory.
│   │   ├── chains/       # Custom LangChain chains.
│   │   │   └── *.py      # Chain modules.
│   │   ├── tools/        # Custom LangChain tools.
│   │   │   └── *.py      # Tool modules.
│   │   ├── agents/       # Custom LangChain Agents.
│   │   │   └── *.py      # Agent modules.
│   │   ├── rag/          # RAG-related modules for retrieval-augmented generation.
│   │   │   └── *.py      # Scripts for retrieval, embedding, ranking, QA pipelines, and utilities.
│   │   ├── router/       # Intent router.
│   │   │   └── *.py      # Intent router developement. 
│   │   │   └── *.ipynb   # Intent routing training and evaluation. And to create synthetic data.
│   ├── pages/            # Streamlit app pages.
│   │   └── *.py          # Page modules.
│   ├── data/             # Data and scripts.
│   │   │── loader.py     # Functions to load data.
│   │   ├── database/     # Database files/scripts.
│   │   │   ├── *.db      # SQLite databases.
│   │   │   ├── *.ipynb   # Scripts for database creation.
│   │   ├── pdfs/         # PDFs and embedding scripts.
│   │   │   ├── *.pdf     # PDF files.
│   │   │   └── *.ipynb   # PDF processing scripts.
```

## Directory and File Details

#### Root Directory
- **`app.py`**: Main Streamlit application script that handles the frontend interface and user interactions.
- **`dev.py`**: Script for testing and debugging the chatbot independently from the app.
- **`requirements.txt`**: List of Python dependencies.
- **`.gitignore`**: Specifies files and directories to be excluded from version control.
- **`README.md`**: Documentation explaining the project, setup, and usage.

#### `company_name/` (Replace with your company name)
- **`__init__.py`**: Package initialization file that exposes the chatbot and development chatbot for external use.

- **`chatbot/`**: Contains chatbot backend functionalities:
  - **`bot.py`**: Core chatbot logic.
  - **`dev_bot.py`**: Standalone chatbot testing script.
  - **`memory.py`**: Implements chatbot memory for retaining context.
  - **`chains/`**: Custom LangChain chains:
    - **`*.py`**: Pipelines for querying databases, processing PDFs, or RAG.
  - **`tools/`**:Custom LangChain tools:
    - **`*.py`**: Helpers for implementation of tools.
  - **`agents/`**: Custom LangChain agents for specialized workflows:
    - **`*.py`**: Modules for tasks like database CRUD.
  - **`rag/`**: Modules for Retrieval-Augmented Generation (RAG):
    - **`*.py`**: Scripts for embedding, ranking, and integrating context.
  - **`router/`**: Handles user intent routing:
    - **`*.py`**: Intent detection and routing scripts.
    - **`*.ipynb`**: Training and evaluating intent routing models.

- **`pages/`**: Streamlit app pages:
  - **`*.py`**: Modules representing different pages (e.g., chatbot interface, home page).

- **`data/`**: Manages project data:
  - **`loader.py`**: Functions for loading data.
  - **`database/`**: Database files and scripts:
    - **`*.db`**: SQLite databases for structured data storage.
    - **`*.ipynb`**: Jupyter notebooks for database creation and management.
  - **`pdfs/`**: PDF documents and processing scripts:
    - **`*.pdf`**: Source PDFs.
    - **`*.ipynb`**: Scripts for extracting text, embeddings, and integration.