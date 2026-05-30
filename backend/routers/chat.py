import json
import asyncio
import traceback
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models.chat_models import ChatRequest
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from services.vectorstore import get_vectorstore
from chains.memory import get_session_memory

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    async def stream_generator():
        try:
            # 1. Setup LLM and Retriever
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
            vectorstore = get_vectorstore()
            retriever = vectorstore.as_retriever(
                search_type="mmr", 
                search_kwargs={
                    'k': 5, 
                    'fetch_k': 15,
                    'filter': {'session_id': request.session_id}
                }
            )
            
            # 2. Get Memory & Chat History
            memory = get_session_memory(request.session_id)
            memory_vars = memory.load_memory_variables({})
            chat_messages = memory_vars.get("chat_history", [])
            chat_history_str = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_messages])
            
            # 3. Retrieve Documents
            docs = await retriever.ainvoke(request.message)
            context_chunks = []
            for d in docs:
                meta = d.metadata
                chunk_str = f"[Video {meta.get('video_id', 'Unknown')}] "
                chunk_str += f"Title: {meta.get('title', 'Unknown')} | "
                chunk_str += f"Creator: {meta.get('creator', 'Unknown')} ({meta.get('follower_count', 0)} followers) | "
                chunk_str += f"Stats: {meta.get('views', 0)} views, {meta.get('likes', 0)} likes, {meta.get('engagement_rate', 0)}% engagement\n"
                chunk_str += f"Content: {d.page_content}"
                context_chunks.append(chunk_str)
            
            context = "\n\n".join(context_chunks)
            
            # 4. Stream the Response
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert AI video analyst. Use the provided context (which contains video metadata, stats, and transcript snippets) and chat history to answer the user's question accurately.\n\nContext:\n{context}\n\nHistory:\n{chat_history}"),
                ("user", "{question}")
            ])
            
            chain = prompt | llm
            
            response_text = ""
            async for chunk in chain.astream({"context": context, "chat_history": chat_history_str, "question": request.message}):
                if chunk.content:
                    response_text += chunk.content
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk.content})}\n\n"
            
            # 5. Send Citations
            for doc in docs:
                yield f"data: {json.dumps({'type': 'citation', 'video_id': doc.metadata.get('video_id', 'Unknown'), 'chunk': doc.page_content[:100] + '...', 'chunk_index': doc.metadata.get('chunk_index', 0)})}\n\n"
                
            # 6. Update Memory
            memory.save_context({"input": request.message}, {"answer": response_text})
            
        except Exception as e:
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)  # Log to backend
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        finally:
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
