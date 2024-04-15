import os
import openai
from pydantic import BaseModel, Field


class OpenAIQuery(BaseModel):
    user_message: str = Field(..., description="Message from the user")
    assistant_message: str = Field(..., description="Previous message from the assistant")

    def query_openai_gpt(self):
        # Set API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")

        # Construct messages
        messages = [
            {
                "role": "user",
                "content": self.user_message
            },
            {
                "role": "assistant",
                "content": self.assistant_message
            }
        ]

        # Make API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract and return the assistant's reply as a string
        assistant_reply = response['choices'][0]['message']['content']
        return assistant_reply
