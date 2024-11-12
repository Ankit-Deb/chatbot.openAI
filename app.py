from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId
"""
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
"""
from openai import OpenAI  # Correct usage here

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
  
# Added for session tracking
app.secret_key = os.getenv("SECRET_KEY", "my_secret_key")

# MongoDB connection string (from .env)
mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
db = mongo_client['ChatbotDB']
collection = db['conversations']

# OpenAI API Key (from .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


"""
# Configure file upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_document_content(file_path):
    content = ""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        for para in doc.paragraphs:
            content += para.text + "\n"
    return content
"""

# Route for the homepage

@app.route('/')
def home():
    return render_template('index.html')


# Route for handling the chatbot's response
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message')

    # Use session-based conversation tracking
    if 'conversation_id' not in session:
        session['conversation_id'] = str(ObjectId())  # Create a new conversation ID if not already in session
    
    conversation_id = session['conversation_id']
    conversation = collection.find_one({"_id": ObjectId(conversation_id)})

    if not conversation:
        # Create a new conversation document if one doesn't exist
        conversation = {"_id": ObjectId(conversation_id), "messages": [{"sender": "user", "text": user_message}]}
        collection.insert_one(conversation)
    else:
        # Append user message to the existing conversation
        collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$push": {"messages": {"sender": "user", "text": user_message}}}
        )

    # Generate OpenAI response using the chat model
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150
        )
        bot_message = response.choices[0].message.content.strip()  # Updated access method

        # Append bot response to the conversation document
        collection.update_one(
            {"_id": ObjectId(conversation_id)},  # Convert conversation_id to ObjectId here
            {"$push": {"messages": {"sender": "bot", "text": bot_message}}}
        )

        return jsonify({'message': bot_message})
    except Exception as e:
        if 'insufficient_quota' in str(e):
            return jsonify({'message': 'Error: You have exceeded your API quota. Please try again later.'})
        else:
            return jsonify({'message': 'Error: ' + str(e)})

"""
# Route for handling document uploads
@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract content from the uploaded document
        document_content = extract_document_content(file_path)

        # Store document content in MongoDB
        collection.insert_one({"document_content": document_content})

        return jsonify({'message': f'Document uploaded and processed: {filename}'})
    else:
        return jsonify({'message': 'Invalid file type. Only PDF and DOCX files are allowed.'})
"""

if __name__ == '__main__':
    """
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    """

    app.run(debug=True)
