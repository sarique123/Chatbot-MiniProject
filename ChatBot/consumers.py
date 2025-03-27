import json
import google.generativeai as genai
from channels.generic.websocket import AsyncWebsocketConsumer

# Initialize Gemini API
GENAI_API_KEY = "your_gemini_api_key"
genai.configure(api_key=GENAI_API_KEY)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Handle disconnects if needed

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get("message", "")

        # Get response from Gemini API
        response_text = await self.get_gemini_response(user_message)

        # Send the response back to the client
        await self.send(text_data=json.dumps({"response": response_text}))

    async def get_gemini_response(self, message):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
