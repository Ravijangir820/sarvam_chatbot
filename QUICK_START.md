# Quick Start Guide - Sarvam AI Chatbot

Get your chatbot running in 5 minutes!

## Prerequisites

- Python 3.8+
- Modern web browser with microphone support
- Internet connection

## Installation & Setup

### Step 1: Navigate to the project folder

```bash
cd c:\Users\ravi_jangir\Desktop\sarvam_chatbot
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

**Windows Users**: You can also run the batch file:
```bash
run_chatbot.bat
```

This will automatically create a virtual environment and install dependencies.

### Step 3: Start the server

```bash
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### Step 4: Open the chatbot

Open your browser and go to:
```
http://localhost:5000
```

## 🎉 Done! Your chatbot is ready!

## First Steps

1. **Try text chat**: Type a question and click Send
2. **Try voice input**: Click the 🎤 Record button, speak, then Stop
3. **Change language**: Select a different language from the dropdown
4. **Explore settings**: Click the ⚙️ Settings gear for more options

## Common Features

### Text Chat
- Type your message
- Click Send or press Enter
- The AI will respond

### Voice Chat
- Click "🎤 Record" button
- Speak clearly into your microphone
- Click "⏹️ Stop" when done
- The audio will be transcribed and sent automatically

### Language Support
- English, Hindi, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Bengali, Punjabi, and more
- The chatbot will respond in your selected language

### Settings
- **Auto-play responses**: Enable text-to-speech for bot replies
- **Dark Mode**: Toggle dark theme for comfortable viewing

## Testing the API

### Test with Python script:

```bash
python test_api.py
```

This will run automatic tests to verify your setup.

### Test with cURL:

```bash
# Health check
curl http://localhost:5000/api/health

# Send a message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello!\", \"language\": \"en\"}"
```

See `curl_examples.md` for more examples.

## Troubleshooting

### "Connection refused" error
- Make sure the Flask server is running
- Try `http://localhost:5000` in your browser
- Check if port 5000 is available

### "API Key invalid" error
- Check your `.env` file
- Ensure API key is correct

### Microphone not working
- Check browser microphone permissions
- Try a different browser (Chrome, Edge, Safari)
- Ensure you granted microphone access when prompted

### Slow responses
- Check your internet connection
- Wait a moment and try again
- Check Sarvam API status

## Project Structure

```
sarvam_chatbot/
├── app.py              ← Main Flask server
├── sarvam_client.py    ← Sarvam API wrapper
├── requirements.txt    ← Python dependencies
├── .env               ← API configuration
├── README.md          ← Full documentation
├── templates/
│   └── index.html     ← Chatbot webpage
└── static/
    ├── script.js      ← Frontend logic
    └── styles.css     ← Styling
```

## Next Steps

1. **Customize the UI**: Edit `templates/index.html` and `static/styles.css`
2. **Change behavior**: Modify `static/script.js` for frontend logic
3. **Extend features**: Add new endpoints in `app.py` and `sarvam_client.py`
4. **Deploy**: See README.md for production deployment options

## Key Commands

```bash
# Start the chatbot
python app.py

# Run tests
python test_api.py

# Install dependencies
pip install -r requirements.txt

# Stop the server
Ctrl+C (in the terminal)
```

## Getting Help

- 📖 [Full Documentation](README.md)
- 🔧 [API Examples](curl_examples.md)
- 🌐 [Sarvam AI Docs](https://docs.sarvam.ai/)
- 💬 [Sarvam AI Discord](https://discord.com/invite/5rAsykttcs)
- 📚 [Sarvam AI Cookbook](https://github.com/sarvamai/sarvam-ai-cookbook)

## API Key Information

Your API key is already configured in `.env`:
```
SARVAM_API_KEY=sk_n8ou9kh3_LLjokiDcynMaVM7F2R8Pk2Es
```

⚠️ **Never share your API key publicly!**

---

**Enjoy your Sarvam AI Chatbot! 🚀**
