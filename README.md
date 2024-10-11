# wasserstoff-AiInternTask
A Flask-based application for PDF summarization and keyword extraction using MongoDB


## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)

## Project Overview
This project is part of an AI internship task. It includes a document analysis web application where users can upload documents, analyze them, and extract key information such as summaries and keywords. The app features a real-time document status filter and search function.

## Features
- Upload and analyze documents.
- View document summaries and keywords.
- Filter documents by status (Completed, Processing, Failed).
- Search documents by name.
- Real-time updates with status filtering and sorting.
- Export results in Json formats.

## Installation
### Prerequisites
- Python 3.8 or higher
- Flask
- Bootstrap 5
- JavaScript libraries (included in the repository)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/nitin-handa/wasserstoff-AiInternTask.git
   
2. Navigate to the project directory:
    ```bash
    cd wasserstoff-AiInternTask
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   
4. Start the Flask server
   ```bash
   python src/app.py     

# Usage
1. Open your browser and navigate to http://127.0.0.1:5000/.
2. Upload a document for analysis.
3. View the document summary, keywords, and other metadata.
4. If results aren't visible, refresh the page after the upload is complete.
   
# File Structure
   ```bash
    project-root/
    ├── src/
    │   ├── app.py
    │   ├── db_manager.py
    │   ├── document_processor.py
    │   ├── summarizer.py
    │   ├── keyword_extractor.py
    │   ├── logger.py
    │   └── utils.py
    │
    ├── static/
    │   └── uploads/
    │
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── upload.html
    │   └── results.html
    │
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── .env
    ├── .gitignore
    └── README.md
    
    
       
