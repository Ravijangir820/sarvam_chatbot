# Sarvam Chatbot API - cURL Examples

This file contains examples of how to test the Sarvam Chatbot API using cURL commands.

## Prerequisites

- Ensure the Flask server is running: `python app.py`
- Server should be accessible at `http://localhost:5000`

## 1. Health Check

Check if the API is running:

```bash
curl -X GET http://localhost:5000/api/health
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "Sarvam Chatbot API"
}
```

## 2. Chat Request - English

Send a text message to the chatbot:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of India?",
    "language": "en"
  }'
```

## 3. Chat Request - Hindi

Send a message in Hindi:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "भारत की राजधानी क्या है?",
    "language": "hi"
  }'
```

## 4. Chat Request - Tamil

Send a message in Tamil:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "இந்தியாவின் தலைநகரம் என்ன?",
    "language": "ta"
  }'
```

## 5. Chat Request - Telugu

Send a message in Telugu:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ఇండియా యొక్క రాజధాని ఏది?",
    "language": "te"
  }'
```

## 6. Chat Request - Multiple Languages

Other supported languages:
- `kn` - Kannada
- `ml` - Malayalam
- `mr` - Marathi
- `gu` - Gujarati
- `bn` - Bengali
- `pa` - Punjabi

Example with Kannada:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ಭಾರತದ ರಾಜಧಾನಿ ಯಾವುದು?",
    "language": "kn"
  }'
```

## 7. Audio Transcription Request

Upload an audio file for transcription:

### Using WAV file (English):
```bash
curl -X POST http://localhost:5000/api/transcribe \
  -F "audio=@path/to/your/audio.wav" \
  -F "language=en-IN"
```

### Using MP3 file (Hindi):
```bash
curl -X POST http://localhost:5000/api/transcribe \
  -F "audio=@path/to/your/audio.mp3" \
  -F "language=hi-IN"
```

### Supported Audio Formats and Languages:
- **Formats**: .wav, .mp3, .ogg, .m4a, .flac
- **Languages**: en-IN, hi-IN, ta-IN, te-IN, kn-IN, ml-IN, mr-IN, gu-IN, bn-IN, pa-IN, etc.

Example Response:
```json
{
  "success": true,
  "transcript": "What is the capital of India",
  "language": "en-IN"
}
```

## 8. Combined Workflow Example

1. **Record and transcribe audio**:
```bash
curl -X POST http://localhost:5000/api/transcribe \
  -F "audio=@recording.wav" \
  -F "language=en-IN"
```

2. **Send transcribed text to chat**:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of India",
    "language": "en"
  }'
```

## Error Handling

### Error Response Examples:

**No message provided:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

Response:
```json
{
  "error": "Message is required"
}
```

**Invalid audio file format:**
```bash
curl -X POST http://localhost:5000/api/transcribe \
  -F "audio=@file.txt" \
  -F "language=en-IN"
```

Response:
```json
{
  "error": "File type not allowed. Allowed: wav, mp3, ogg, m4a, flac"
}
```

**No audio file provided:**
```bash
curl -X POST http://localhost:5000/api/transcribe \
  -F "language=en-IN"
```

Response:
```json
{
  "error": "No audio file provided"
}
```

## Using PowerShell (Windows)

If you're on Windows and prefer PowerShell:

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method Get

# Chat request
$body = @{
    message = "What is the capital of India?"
    language = "en"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## Useful Tools

- **Postman**: Great GUI for testing APIs
  - Download: https://www.postman.com/downloads/
  - Create requests visually and save collections

- **Insomnia**: Lightweight REST client
  - Download: https://insomnia.rest/

- **VS Code REST Client**: Extension for VS Code
  - Create `.rest` files with request examples

## Testing with Python

```python
import requests
import json

# Chat
response = requests.post(
    'http://localhost:5000/api/chat',
    json={
        'message': 'Hello, how can I help?',
        'language': 'en'
    }
)
print(json.dumps(response.json(), indent=2))

# Transcribe
with open('audio.wav', 'rb') as f:
    files = {'audio': f}
    data = {'language': 'en-IN'}
    response = requests.post(
        'http://localhost:5000/api/transcribe',
        files=files,
        data=data
    )
print(json.dumps(response.json(), indent=2))
```

## Testing with JavaScript/Node.js

```javascript
// Chat
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello, how can I help?',
    language: 'en'
  })
})
.then(resp => resp.json())
.then(data => console.log(data));

// Transcribe
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.wav');
formData.append('language', 'en-IN');

fetch('http://localhost:5000/api/transcribe', {
  method: 'POST',
  body: formData
})
.then(resp => resp.json())
.then(data => console.log(data));
```

## Rate Limiting & Best Practices

- Respect Sarvam API rate limits
- Add appropriate delays between requests in production
- Implement retry logic with exponential backoff
- Cache responses when applicable
- Use compression for audio files
- Log all requests for debugging

## Troubleshooting

### Issue: "Connection refused" error
- Ensure Flask server is running: `python app.py`
- Check if port 5000 is available
- Try accessing http://localhost:5000 in your browser

### Issue: "API Key invalid" error
- Verify API key in `.env` file
- Check for extra spaces in the key
- Ensure the API key has required permissions

### Issue: Audio transcription returns empty
- Check audio file quality
- Verify the language code matches the audio language
- Try a different audio format

### Issue: Chat responses are slow
- Check internet connection
- Monitor Sarvam API status
- Check system resources (CPU, memory)

---

For more information, visit:
- [Sarvam AI Documentation](https://docs.sarvam.ai/)
- [API Reference](https://docs.sarvam.ai/api-reference-docs/)
