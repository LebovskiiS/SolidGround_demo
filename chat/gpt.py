from DjangoProject.settings import GPT_API, PROMPT, GPT_WELCOME_MESSAGE
from openai import OpenAI


class GPT:
    API_KEY = GPT_API

    def __init__(self, user_id, model="gpt-4.1"):
        self.client = OpenAI(api_key=self.API_KEY)
        self.user_id = user_id
        self.model = model
        self.messages = []

        if PROMPT:
            self.messages.append({"role": "system", "content": PROMPT})

    def get_response(self, message_to_chat, role="user"):
        self.messages.append({"role": role, "content": message_to_chat})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )

        try:
            ai_response = response.choices[0].message.content
        except (IndexError, AttributeError) as e:
            print(f"Error processing response: {e}")
            return "Failed to get a valid response from the model."

        self.messages.append({"role": "assistant", "content": ai_response})

        return ai_response
