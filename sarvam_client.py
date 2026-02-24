import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# System prompt to make the LLM Sarvam AI focused - STRICT VERSION
SARVAM_SYSTEM_PROMPT = """You are a specialized customer support assistant for Sarvam AI, an India-first AI platform.

YOUR PRIMARY ROLE: Help customers understand and use Sarvam AI's products and services ONLY.

**IMPORTANT**: You MUST ONLY answer questions related to Sarvam AI and its ecosystem. 
For ANY question that is NOT about Sarvam AI, you MUST politely decline and redirect to Sarvam AI topics.

**Sarvam AI Products & Services:**
1. **Samvaad Studio** - Enterprise conversational agents for customer interactions
   - Use cases: Cart recovery, appointment booking, payment follow-ups, customer service
   - Features: Multi-language support, enterprise security

2. **Speech-to-Text (Saaras v3)** - State-of-the-art ASR
   - Supports 23 languages (22 Indian + English)
   - Features: Transcription, translation, transliteration, code-mixing
   - Use cases: Voice assistants, call center analytics, accessibility

3. **Text-to-Speech (Bulbul v3)** - Natural voice generation
   - 11 languages (10 Indian + English)
   - Features: Customizable pitch, pace, speaker options
   - Use cases: IVR systems, accessibility, content localization

4. **Sarvam-M** - Advanced multilingual LLM
   - Supports Indian languages with deep cultural understanding
   - Use cases: Chat, reasoning, content generation

5. **Vision/Document Intelligence** - Content extraction
   - 23 language support for OCR
   - Use cases: Document digitization, form processing, data extraction

6. **Latest Models:**
   - **Indus** - Frontier-class model
   - **Sarvam Akshar** - Enhanced accuracy model
   - **Sarvam Edge** - Edge deployment solution

7. **Samvaad** - Conversational AI platform
   - Pre-built agents for common use cases
   - Enterprise-grade security (ISO certified, SOC 2 Type II)

**Key Differentiators:**
- Sovereign AI built in India
- Support for all 23 Indian languages
- Population-scale applications
- Enterprise security and compliance
- Flexible deployment: Cloud, Private Cloud (VPC), On-Premises

**STRICT INSTRUCTIONS:**
1. ONLY answer questions about Sarvam AI, its products, features, APIs, and pricing
2. If user asks about something unrelated (general knowledge, other companies, personal advice, etc.):
   - Politely say you can only help with Sarvam AI topics
   - Offer to answer Sarvam AI related questions instead
3. For technical API questions, provide accurate, helpful information
4. For pricing/billing, direct to https://www.sarvam.ai/api-pricing
5. For account issues, direct to https://dashboard.sarvam.ai/
6. For documentation, share https://docs.sarvam.ai/

**Example Responses:**

User: "What is the capital of India?"
You: "I'm specifically designed to help with Sarvam AI. I can't answer general knowledge questions. But I'd be happy to help you with Sarvam AI's products! For example, our Saaras v3 STT supports Hindi and can process audio in 23 languages. What would you like to know about Sarvam AI?"

User: "How do I use your speech-to-text API?"
You: [Provide detailed, helpful information about Saaras v3 STT]

User: "Tell me a joke"
You: "I'm here to help with Sarvam AI questions only! Would you like to learn about our conversational AI products (Samvaad) or any other Sarvam AI service?"

**Your Tone:**
- Professional but friendly
- Helpful and solution-oriented
- Focused on Sarvam AI value proposition
- Patient with redirecting off-topic questions"""

class SarvamClient:
    def __init__(self):
        self.api_key = os.getenv("SARVAM_API_KEY")
        self.api_base_url = os.getenv("SARVAM_API_BASE_URL", "https://api.sarvam.ai")
        self.headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def transcribe_audio(self, audio_file_path, language="en-IN"):
        """
        Convert speech to text using Saaras v3 STT model
        
        Args:
            audio_file_path: Path to audio file (MP3, WAV, etc.)
            language: Language code (e.g., 'en-IN', 'hi-IN')
        
        Returns:
            Transcribed text
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {
                    'file': (audio_file_path.split('\\')[-1], audio_file, 'audio/wav'),
                }
                
                data = {
                    'language_code': language,
                    'model': 'saaras:v3'
                }
                
                # For file uploads, don't include Content-Type header
                # requests will automatically set it to multipart/form-data
                headers = {
                    "api-subscription-key": self.api_key
                }
                
                print(f"[DEBUG] Transcribing with key: {self.api_key[:20]}... | Language: {language}")
                
                response = requests.post(
                    f"{self.api_base_url}/speech-to-text",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                # Check response format
                if 'transcript' in result:
                    return result['transcript']
                else:
                    print(f"Unexpected response format: {result}")
                    return str(result)
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    pass
                print(f"Error in transcription (Status {response.status_code}): {error_msg}")
                return None
        except FileNotFoundError:
            print(f"Audio file not found: {audio_file_path}")
            return None
        except requests.exceptions.Timeout:
            print("Transcription request timed out")
            return None
        except Exception as e:
            print(f"Exception in transcribe_audio: {str(e)}")
            return None
    
    def chat(self, message, language="en"):
        """
        Send a message to the Sarvam-M LLM model for chat
        
        Args:
            message: User message
            language: Language code
        
        Returns:
            Chat response from the model
        """
        try:
            # Build conversation messages with system context
            messages = [
                {
                    "role": "system",
                    "content": SARVAM_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            payload = {
                "model": "sarvam-m",
                "messages": messages,
                "temperature": 0.2,
                "top_p": 1.0,
                "max_tokens": 1024
            }
            
            response = requests.post(
                f"{self.api_base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract response from the model
                if 'choices' in result and len(result['choices']) > 0:
                    choice = result['choices'][0]
                    if 'message' in choice:
                        return choice['message'].get('content', '')
                
                # Fallback: return entire result as string
                print(f"Unexpected response format: {result}")
                return str(result)
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    pass
                print(f"Error in chat (Status {response.status_code}): {error_msg}")
                return f"Sorry, I encountered an error: {error_msg}"
        except requests.exceptions.Timeout:
            print("Chat request timed out")
            return "Sorry, the request timed out. Please try again."
        except Exception as e:
            print(f"Exception in chat: {str(e)}")
            return f"Sorry, an error occurred: {str(e)}"
    
    def get_response(self, user_input, language="en"):
        """
        Get a response from the chatbot for user input
        
        Args:
            user_input: User message or question
            language: Language code
        
        Returns:
            Response from the chatbot
        """
        return self.chat(user_input, language)


if __name__ == "__main__":
    client = SarvamClient()
    response = client.get_response("What is the capital of India?")
    print(response)
