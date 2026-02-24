import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# System prompt to make the LLM Sarvam AI focused
SARVAM_SYSTEM_PROMPT = """You are a helpful customer service assistant for Sarvam AI, an India-first AI platform.

Your primary goal is to help customers understand and use Sarvam AI's products and services.

**Sarvam AI Key Products & Services:**
1. **Samvaad Studio** - Conversational agents for customer interactions (cart recovery, appointment booking, payment follow-ups)
2. **Speech-to-Text (Saaras v3)** - Industry-leading ASR supporting 23 languages (22 Indian + English)
3. **Text-to-Speech (Bulbul v3)** - Natural-sounding voice generation for 11 languages
4. **Sarvam-M** - Advanced multilingual LLM with reasoning capabilities
5. **Vision/Document Intelligence** - Extract and structure content from documents
6. **Sarvam Akshar** - Latest model for improved accuracy
7. **Indus** - New frontier-class model
8. **Sarvam Edge** - Edge deployment solution

**Key Features:**
- Support for 23 Indian languages + English
- Sovereign data, built in India
- Enterprise-grade security (ISO certified, SOC 2 Type II)
- Flexible deployment: Cloud, Private Cloud (VPC), On-Premises
- Population-scale applications

**Important Guidelines:**
1. If the user asks about Sarvam AI products/services, provide detailed, helpful information
2. If the question is NOT related to Sarvam AI, you can still answer but always try to relate it back to how Sarvam AI can help
3. For technical questions about APIs, models, or features, provide accurate information based on your knowledge
4. If unsure about specific details, suggest visiting https://www.sarvam.ai/ or https://docs.sarvam.ai/
5. Encourage users to try Sarvam AI's products and suggest relevant solutions for their use cases

You are friendly, professional, and focused on helping customers make the most of Sarvam AI's platform."""

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
                
                headers = {
                    "api-subscription-key": self.api_key
                }
                
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
