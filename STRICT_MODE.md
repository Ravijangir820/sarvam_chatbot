# Sarvam AI Chatbot - Strict Mode Configuration

This document explains the strict Sarvam AI-only mode implemented in the chatbot.

## 🎯 What Changed

The chatbot now operates in **STRICT MODE**, meaning it:

✅ **WILL answer questions about:**
- Sarvam AI products and services
- How to use Sarvam AI APIs
- Features and capabilities of Sarvam models
- Pricing and deployment options
- Technical implementation details
- Use cases and customer success stories

❌ **WILL NOT answer questions about:**
- General knowledge (capitals, geography, math, etc.)
- Other companies or products
- Personal advice
- Entertainment or trivia
- Any topic unrelated to Sarvam AI

## 🔄 Behavior Examples

### ✓ Good: Sarvam AI Topic
**User:** "How do I use Saaras v3 for speech-to-text?"
**Assistant:** [Detailed answer about Saaras v3, APIs, implementation]

### ✗ Off-Topic: General Knowledge
**User:** "What is the capital of India?"
**Assistant:** "I'm specifically designed to help with Sarvam AI. I can't answer general knowledge questions. But I'd be happy to help you with Sarvam AI's products! For example, our Saaras v3 STT supports Hindi and can process audio in 23 languages. What would you like to know about Sarvam AI?"

### ✗ Off-Topic: Other Company
**User:** "How is Google's AI different from Sarvam?"
**Assistant:** "I'm here to help with Sarvam AI questions only! I can explain Sarvam AI's unique strengths like sovereign data, support for 23 Indian languages, and enterprise-grade security. Would you like to know more about Sarvam?"

## 💡 Key Features of Strict Mode

### 1. Polite Redirection
- Declines off-topic questions gracefully
- Always offers to help with Sarvam AI topics
- Maintains friendly, professional tone

### 2. Product Knowledge
The chatbot knows about:
- **Samvaad Studio** - Conversational AI platform
- **Saaras v3** - Speech-to-Text (23 languages)
- **Bulbul v3** - Text-to-Speech (11 languages)
- **Sarvam-M** - Multilingual LLM
- **Vision** - Document Intelligence
- **Indus** - Latest frontier model
- **Sarvam Akshar** - Enhanced model
- **Sarvam Edge** - Edge deployment

### 3. Helpful Redirects
When declining a question, the chatbot:
- Explains it's Sarvam AI specific
- Suggests a related Sarvam AI topic
- Provides website/docs links

## 🧪 Testing Strict Mode

Run the test suite to verify:

```bash
python test_strict_mode.py
```

Expected behavior:
- Sarvam AI queries: Detailed, helpful answers
- General queries: Polite decline with redirect
- Off-topic queries: "Let's talk about Sarvam AI instead"

## 📝 System Prompt Details

The strict mode is enforced through the system prompt in `sarvam_client.py`:

```python
SARVAM_SYSTEM_PROMPT = """
You are a specialized customer support assistant for Sarvam AI.
YOUR PRIMARY ROLE: Help customers understand Sarvam AI ONLY.
For ANY question that is NOT about Sarvam AI, you MUST politely decline.
"""
```

## 🎯 Use Cases Supported

The chatbot is perfect for:

1. **Customer Support**
   - Answering product questions
   - Helping with API integration
   - Troubleshooting common issues

2. **Sales & Onboarding**
   - Explaining Sarvam AI benefits
   - Guiding new users
   - Showcasing use cases

3. **Technical Documentation**
   - API details and endpoints
   - Code examples
   - Integration patterns

4. **Language Support**
   - Explaining 23-language support
   - Use cases for Indian languages
   - Regional customization

## ⚙️ Configuration

To adjust the strict mode behavior, edit `sarvam_client.py`:

```python
# Lines 5-80: Modify SARVAM_SYSTEM_PROMPT
# Make it more/less strict as needed
```

### Examples of modifications:

**More Permissive:** Allow tangential topics
- Remove "ONLY" and "MUST"
- Add "but you can also discuss..."

**Even Stricter:** Very brief, only Sarvam Q&A
- Add: "Keep responses to Sarvam AI only"
- Remove: Examples of off-topic behaviors

## 🔄 Testing Different Queries

### Sarvam AI Topics (should get detailed answers):
- "What is Sarvam-M?"
- "How do I integrate Saaras v3?"
- "Tell me about Bulbul TTS"
- "What languages does Sarvam support?"
- "How is Sarvam's approach sovereign?"

### Off-Topic (should get declined):
- "What is 2+2?"
- "Tell me a joke"
- "How to learn Python?"
- "What's the weather?"
- "Compare Google and OpenAI"

## 📊 Usage Analytics

Monitor in Flask logs:
```
[Chat] Message: <user_query> | Language: <lang>
Response: <assistant_response>
```

### Metrics to track:
- % Sarvam AI questions answered
- % Off-topic questions declined
- Average response quality
- User satisfaction

## 🚀 Production Deployment

For production:

1. **Monitor Off-Topic Queries**
   - Track which topics users ask about
   - Consider adding to knowledge base if relevant

2. **Update Regularly**
   - New Sarvam products → update system prompt
   - Customer feedback → refine responses

3. **Analytics Integration**
   - Log all queries and responses
   - Monitor deflection rate
   - Track user satisfaction

## 📚 Related Files

- `sarvam_client.py` - Contains system prompt
- `test_strict_mode.py` - Test suite
- `README.md` - Full documentation
- `SECURITY.md` - Security guidelines

---

**Summary:** This strict mode ensures the chatbot stays focused on its purpose: helping customers understand and use Sarvam AI. It politely declines off-topic questions while maintaining a helpful, professional tone.
