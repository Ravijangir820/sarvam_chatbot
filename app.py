from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from sarvam_client import SarvamClient
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'flac'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB max file size

# Initialize Sarvam client
sarvam = SarvamClient()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main chatbot page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests
    Expects JSON: {"message": "user message", "language": "en"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        message = data.get('message', '').strip()
        language = data.get('language', 'en')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Log the request
        print(f"[Chat] Message: {message[:50]}... | Language: {language}")
        
        response = sarvam.get_response(message, language)
        
        if response:
            return jsonify({
                'success': True,
                'response': response,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to get response from Sarvam API. Please try again.'
            }), 500
            
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid request format'
        }), 400
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your message'
        }), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Handle audio transcription requests
    Expects multipart form data with audio file
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        language = request.form.get('language', 'en-IN')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Check file size
        if file.content_length and file.content_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'error': 'File size exceeds maximum limit'}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"[Transcribe] File: {filename} | Language: {language}")
        
        # Transcribe the audio
        transcript = sarvam.transcribe_audio(filepath, language)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        if transcript:
            return jsonify({
                'success': True,
                'transcript': transcript,
                'language': language
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to transcribe audio. Please try a different audio file or language.'
            }), 500
            
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred during transcription'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Sarvam Chatbot API'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
