from pydantic import BaseModel, parse_raw_as
from typing import List, Optional

from pydantic import BaseModel, parse_raw_as

from memory.redis_manager import upload_to_redis


class Conversation(BaseModel):
    question: str
    answer: str
    agents: List[str]
    reason: str


class ConversationBuffer:
    def __init__(self):
        self.buffer = []

    def get_memory_from_buffer(self, index: int) -> Optional[str]:
        conversation = self.get_conversation_from_buffer(index)

        if conversation:
            return f"Previous Q: {conversation.question}, Previous A: {conversation.answer}"
        return None

    def add_conversation(self, response_json_str: str):
        # Deserialize JSON string to Conversation object
        conversation = parse_raw_as(Conversation, response_json_str)

        self.buffer.append(conversation)
        if len(self.buffer) >= 5:
            self.process_buffer()

    def process_buffer(self):
        # Summarize conversations
        summary = self.summarize_conversations()
        memory = self.get_memory_from_buffer(-1)

        # Upload to Redis
        upload_to_redis(self.buffer, memory)

        # Clear the buffer
        self.buffer.clear()

    def get_conversation_from_buffer(self, index: int) -> Optional[Conversation]:
        try:
            return self.buffer[index]
        except IndexError:
            return None

    def summarize_conversations(self):
        # Your logic to summarize conversations
        # post LLM integration
        return "Summary"
