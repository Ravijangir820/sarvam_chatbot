# Sarvam AI Chatbot

A web-based chatbot application powered by Sarvam AI's Speech-to-Text (STT) and Large Language Model (LLM) services. The chatbot supports multiple Indian languages and can handle both text and voice input.

## Features

✨ **Key Features:**
- 🎤 Speech-to-Text (STT) using Saaras v3 model
- 💬 AI-powered chat using Sarvam-M language model
- 🌐 Support for 23 languages (22 Indian languages + English)
- 🎙️ Voice recording and transcription
- 🌙 Dark mode support
- 📱 Responsive mobile-friendly design
- ⚡ Real-time chat responses

## Supported Languages

- English (en)
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
- Malayalam (ml)
- Marathi (mr)
- Gujarati (gu)
- Bengali (bn)
- Punjabi (pa)

And many more...

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser with microphone access (for voice features)

## Installation

### 1. Clone or Download the Repository

```bash
cd c:\Users\ravi_jangir\Desktop\sarvam_chatbot
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

The `.env` file already contains your API key:
```
SARVAM_API_KEY=sk_n8ou9kh3_LLjokiDcynMaVM7F2R8Pk2Es
SARVAM_API_URL=https://api.sarvam.ai/api/v1
```

## Running the Application

### Start the Flask Server

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### Access the Chatbot

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Text-Based Chat
1. Type your message in the input field
2. Click "Send" or press Enter
3. The chatbot will respond with an AI-generated answer

### Voice Input
1. Click the "🎤 Record" button
2. Speak your question or message
3. Click "⏹️ Stop" when done
4. The speech will be transcribed and sent as a message
5. The chatbot will respond

### Language Selection
1. Select your preferred language from the "Select Language" dropdown
2. The chatbot will respond in the selected language

### Settings
- **Auto-play responses**: Enable/disable text-to-speech for bot responses
- **Dark Mode**: Toggle dark theme for better visibility in low-light environments

## API Endpoints

### 1. Chat Endpoint
```
POST /api/chat
Content-Type: application/json

Request:
{
    "message": "What is the capital of India?",
    "language": "en"
}

Response:
{
    "success": true,
    "response": "The capital of India is New Delhi.",
    "message": "What is the capital of India?"
}
```

### 2. Transcription Endpoint
```
POST /api/transcribe
Content-Type: multipart/form-data

FormData:
- audio: <audio file>
- language: "en-IN"

Response:
{
    "success": true,
    "transcript": "What is the capital of India",
    "language": "en-IN"
}
```

### 3. Health Check
```
GET /api/health

Response:
{
    "status": "healthy",
    "service": "Sarvam Chatbot API"
}
```

## Architecture

```
sarvam_chatbot/
├── app.py                 # Flask backend application
├── sarvam_client.py       # Sarvam API client
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API key)
├── README.md             # This file
├── templates/
│   └── index.html        # HTML interface
└── static/
    ├── styles.css        # CSS styling
    └── script.js         # Frontend JavaScript
```

## File Descriptions

### Backend Files

- **app.py**: Main Flask application that serves the web interface and API endpoints
  - `/` - Serves the chatbot UI
  - `/api/chat` - Handles text chat requests
  - `/api/transcribe` - Handles audio transcription requests
  - `/api/health` - Health check endpoint

- **sarvam_client.py**: Wrapper client for Sarvam AI APIs
  - `transcribe_audio()` - Converts speech to text using Saaras v3
  - `chat()` - Sends messages to Sarvam-M LLM model
  - `get_response()` - High-level method for getting responses

### Frontend Files

- **templates/index.html**: HTML structure with language selector, message area, and input controls
- **static/styles.css**: Modern, responsive CSS with dark mode support
- **static/script.js**: Client-side JavaScript for:
  - Audio recording and transcription
  - Chat message handling
  - UI interactions
  - Speech synthesis (optional)

## Configuration

### Environment Variables

Edit `.env` to customize:
```
SARVAM_API_KEY=your_api_key_here
SARVAM_API_URL=https://api.sarvam.ai/api/v1
```

### Flask Settings

In `app.py`, you can modify:
- `DEBUG=True/False` - Enable/disable debug mode
- `MAX_CONTENT_LENGTH` - Maximum file upload size (currently 25MB)
- `UPLOAD_FOLDER` - Temporary audio file storage

## Sarvam AI Models Used

### Saaras v3 (Speech-to-Text)
- **Endpoint**: `/api/v1/speech/asr`
- **Features**: Supports 23 languages, multiple output modes
- **Use Case**: Converting user speech to text

### Sarvam-M (LLM/Chat)
- **Endpoint**: `/api/v1/chat/completions`
- **Features**: Multilingual chat with reasoning capabilities
- **Use Case**: Generating intelligent responses to user queries

## Troubleshooting

### Issue: "API Key Invalid" Error
- Verify the API key in `.env` file
- Ensure there are no extra spaces or quotes around the key

### Issue: Microphone Not Working
- Check browser permissions for microphone access
- Ensure your browser supports the Web Audio API
- Try a different browser (Chrome, Edge, Safari)

### Issue: Speech Transcription Fails
- Verify audio quality and microphone volume
- Check that the audio file is in supported format (WAV, MP3, OGG)
- Ensure the language code matches your speech language

### Issue: Connection Refused
- Ensure Flask server is running on port 5000
- Check firewall settings
- Try accessing http://localhost:5000 instead of a different address

### Issue: Slow Responses
- Check your internet connection
- Monitor Sarvam API status
- Reduce request frequency if rate-limited

## Development Notes

### Adding New Languages
1. Update the `languageSelect` dropdown in `templates/index.html`
2. Add language mapping in `getLanguageCode()` function in `static/script.js`
3. Update the `language` parameter in API calls

### Customizing the UI
- Modify `static/styles.css` for styling changes
- Update `templates/index.html` for layout changes
- Edit `static/script.js` for behavior changes

### Extending Functionality
- Add new endpoints in `app.py`
- Create new API methods in `sarvam_client.py`
- Update frontend to call new endpoints from `static/script.js`

## API Documentation Reference

For detailed API documentation, visit:
- **Sarvam AI Docs**: https://docs.sarvam.ai/
- **Sarvam AI Cookbook**: https://github.com/sarvamai/sarvam-ai-cookbook

## Security Notes

⚠️ **Important**:
- Never commit `.env` with your API key to public repositories
- Keep your API key confidential
- Use HTTPS in production
- Add authentication if deploying to production
- Implement rate limiting for public access

## Performance Tips

- Use HTTP/2 for faster connections
- Implement caching for common responses
- Optimize audio file sizes before transcription
- Use CDN for static files in production
- Monitor API usage and quotas

## Deployment

For production deployment:

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t sarvam-chatbot .
docker run -p 5000:5000 -e SARVAM_API_KEY=your_key sarvam-chatbot
```

## License

This project uses the Sarvam AI API. Refer to their documentation for usage terms.

## Support

For issues or questions:
- Check the [Sarvam AI Documentation](https://docs.sarvam.ai/)
- Join the [Sarvam AI Discord Community](https://discord.com/invite/5rAsykttcs)
- Review the [Sarvam AI Cookbook](https://github.com/sarvamai/sarvam-ai-cookbook)

## Changelog

### v1.0.0 (Initial Release)
- Basic chat functionality
- Speech-to-text support
- Multiple language support
- Dark mode
- Responsive design

---

**Built with ❤️ using Sarvam AI services**
