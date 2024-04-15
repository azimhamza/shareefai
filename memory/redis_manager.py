import redis
from pydantic import BaseModel
from typing import List, Optional


class RedisManager(BaseModel):
    """
    Pydantic model for Conversation
    """

    question: str
    answer: str
    agents: List[str]
    reason: str
    pre_context: Optional[str]

    # Connect to a single, secured Redis instance as a function
    # of the environment variables.

    def connect_redis(self: str, port: int, db: int, password: str):
        """
        Connect to Redis
        :param self:
        :param port:
        :param db:
        :param password:
        :return:
        """
        return redis.Redis(host=self, port=port, db=0, password=password)


def upload_to_redis(r, conversations: List[RedisManager], pre_context: Optional[str]):
    """
    Upload a list of conversations to Redis
    :param r:
    :param conversations:
    :param pre_context:
    :return:
    """
    for i, conv in enumerate(conversations):
        r.hmset(
            f"conversation:{i}",
            {
                "question": conv.question,
                "answer": conv.answer,
                "agents": ",".join(conv.agents),
                "reason": conv.reason,
                "pre_context": pre_context,
            },
        )


def upload_to_other_db():
    """
    @TODO: Implement this function to upload to other DBs
    :return:
    """
    return None


def fetch_from_redis(r, conversation_id: str) -> Optional[RedisManager]:
    """
    Fetch a conversation from Redis
    :param r:
    :param conversation_id:
    :return:
    """
    data = r.hgetall(f"conversation:{conversation_id}")
    if not data:
        return RedisManager(
            question=data.get("question").decode(),
            answer=data.get("answer").decode(),
            agents=data.get("agents").decode().split(","),
            reason=data.get("reason").decode(),
            pre_context=data.get("pre_context").decode(),  # Retrieve the pre_context
        )
