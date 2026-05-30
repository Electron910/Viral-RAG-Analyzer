import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import ConversationalRetrievalChain
from services.vectorstore import get_vectorstore
from chains.memory import get_session_memory

def get_rag_chain(session_id: str, callbacks=None):
    # Non-streaming LLM for condensing the question
    condense_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.0
    )
    
    # Streaming LLM for generating the final answer
    streaming_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.2, 
        streaming=True,
        callbacks=callbacks
    )
    
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'fetch_k': 15}
    )
    memory = get_session_memory(session_id)
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=streaming_llm,
        condense_question_llm=condense_llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False
    )
    return chain
