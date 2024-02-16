import openai
from openai import OpenAI

class ChatGPT:
    def __init__(self):
        self.client = OpenAI()
        self.chat_history = []
    
    def prompt(self, user_prompt):
        # Combine the conversation history with the new user prompt
        full_prompt = self._build_full_prompt(user_prompt)

        response = self.client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": full_prompt}
        ])
        #print(response.choices[0].message.content.strip())
        response_text = response.choices[0].message.content.strip()  # Clean up leading/trailing spaces
        self._update_chat_history(user_prompt, response_text)  # Update the conversation history
        return response_text
    
    def _build_full_prompt(self, user_prompt):
        # Combine the chat history and the new user prompt into a single string
        return "\n".join(self.chat_history + [f"User: {user_prompt}", "AI:"])

    def _update_chat_history(self, user_prompt, ai_response):
        # Update the conversation history with the latest exchange
        self.chat_history.extend([f"User: {user_prompt}", f"AI: {ai_response}"])

    def restart_chat(self):
        # Reset the conversation history to start a new chat session
        self.chat_history = []