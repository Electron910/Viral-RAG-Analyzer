from langchain_classic.memory import ConversationBufferMemory
from utils.session import get_session

def get_session_memory(session_id: str) -> ConversationBufferMemory:
    session_data = get_session(session_id)
    if "memory" not in session_data:
        session_data["memory"] = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True,
            output_key="answer"
        )
    return session_data["memory"]
