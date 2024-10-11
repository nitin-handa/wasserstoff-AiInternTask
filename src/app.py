# Import necessary libraries
import os
import uuid
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import datetime
from document_processor import DocumentProcessor
from summarizer import Summarizer
from keyword_extractor import KeywordExtractor
from db_manager import DBManager
from utils import determine_length
from logger import logger
from flask import send_from_directory, jsonify

# Load environment variables
load_dotenv()

# Configuring application
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}  
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # Maximum file size set to 50MB

# Flask app initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Component initialization
db_manager = DBManager(uri=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
summarizer = Summarizer()
keyword_extractor = KeywordExtractor()
processor = DocumentProcessor(UPLOAD_FOLDER)  # Initialize DocumentProcessor

# Setup ThreadPoolExecutor for concurrent execution
executor = ThreadPoolExecutor(max_workers=5)

# Function to verify if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process a document
def process_document(doc_path, num_pages):
    logger.info(f"Processing file: {doc_path}")
    
    """
    Handle text extraction, summarization, keyword extraction, and save the metadata to the database.
    """
    try:
        logger.info(f"Starting file processing for {doc_path}")
        
        # Normalize path
        normalized_path = os.path.normpath(doc_path)
        logger.info(f"Normalized file path: {normalized_path}")
        
        # Extract text
        text = processor.extract_text(normalized_path)
        
        if text:
            logger.info(f"Text extracted from {normalized_path}: {text[:500]}...")  # Log first 500 characters
        else:
            logger.error(f"Failed to extract text from {normalized_path}.")
            return

        # Determine document length
        doc_length = determine_length(num_pages)
        logger.info(f"Document length calculated: {doc_length} pages.")

        # Summarize text
        summary = summarizer.summarize(text, num_pages)
        if summary:
            logger.info(f"Summary generated for {normalized_path}.")
        else:
            logger.warning(f"Failed to generate summary for {normalized_path}.")
        
        # Extract keywords
        keywords = keyword_extractor.extract_keywords(text)
        if keywords:
            logger.info(f"Keywords extracted for {normalized_path}: {keywords}")
        else:
            logger.warning(f"Failed to extract keywords from {normalized_path}.")

        # Record metadata in the database
        metadata = {
            'document_name': os.path.basename(normalized_path),
            'path': normalized_path.replace('\\', '/'),
            'size': os.path.getsize(normalized_path),
            'num_pages': num_pages,
            'summary': summary,
            'keywords': keywords,
            'status': 'Completed' if summary and keywords else 'Failed',
            'processing_time': 0 
        }
        
        # Save metadata
        doc_id = db_manager.insert_metadata(metadata)
        if doc_id:
            logger.info(f"Document processed successfully: {doc_id}")
        else:
            logger.error(f"Failed to insert document metadata for {normalized_path}")

    except Exception as e:
        logger.error(f"Error processing file {doc_path}: {e}")
        db_manager.insert_metadata({
            'document_name': os.path.basename(doc_path),
            'path': doc_path.replace('\\', '/'),
            'size': os.path.getsize(doc_path),
            'num_pages': num_pages,
            'status': 'Failed'
        })

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file uploaded.')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            flash('No file selected.')
            return redirect(request.url)
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                uploaded_files.append(file_path)
                logger.info(f"File uploaded to: {file_path}")
            else:
                flash(f"File type for {file.filename} is not supported.")

        if uploaded_files:
            for doc_path in uploaded_files:
                try:
                    num_pages = processor.get_num_pages(doc_path)
                    logger.info(f"File has {num_pages} pages.")
                except Exception as e:
                    logger.error(f"Error determining page count for {doc_path}: {e}")
                    num_pages = 1

                executor.submit(process_document, doc_path, num_pages)
            
            flash('Your documents have been successfully uploaded and are being processed. If the results are not immediately visible, please refresh the page.', 'success')
            flash('Recent Uploaded document(s) at bottom  ', 'success')
            return redirect(url_for('view_results'))

    return render_template('upload.html')

# Route for viewing results
@app.route('/results')
def view_results():
    status_filter = request.args.get('status', 'all')
    sort_by = request.args.get('sort_by', 'uploaded_at')
    sort_order = request.args.get('sort_order', 'desc')

    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'  # Default to descending if invalid

    documents = db_manager.get_all_documents(status_filter=status_filter, sort_by=sort_by, sort_order=sort_order)
    logger.info(f"{len(documents)} documents retrieved with filter '{status_filter}' sorted by '{sort_by}'.")

    return render_template('results.html', documents=documents)

# Route for downloading files
@app.route('/download/<document_id>')
def download_file(document_id):
    document = db_manager.get_document_by_id(document_id)
    
    if document:
        file_path = os.path.normpath(document['path'])
        if os.path.exists(file_path):
            directory, filename = os.path.split(file_path)
            return send_from_directory(directory, filename, as_attachment=True)
        else:
            flash('File not found.')
            return redirect(url_for('view_results'))
    else:
        flash('Document not found.')
        return redirect(url_for('view_results'))

# Route to export documents as JSON
@app.route('/export')
def export_data():
    import json
    documents = db_manager.get_all_documents()
    for doc in documents:
        doc['_id'] = str(doc['_id'])
    
    return app.response_class(
        response=json.dumps(documents, indent=4),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=documents.json'}
    )

# API route for retrieving documents
@app.route('/api/documents')
def get_documents_api():
    status_filter = request.args.get('status', 'all')
    sort_by = request.args.get('sort_by', 'document_name')

    documents = db_manager.get_all_documents(status_filter=status_filter, sort_by=sort_by)
    for doc in documents:
        doc['_id'] = str(doc['_id'])

    return jsonify(documents)

# Error handler for oversized files
@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File exceeds the maximum allowed size of 50MB.')
    return redirect(request.url), 413

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
