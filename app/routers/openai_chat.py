from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import re
from fastapi import APIRouter
from app.schemas.caterer import ChatRequest, ChatResponse, MatchedCaterer
from app.models.matcher import get_recommendations

router = APIRouter(prefix="/openai-chat", tags=["Chat"])
load_dotenv()

model = ChatOpenAI()

def query_llm(text: str) -> str:
    prompt = PromptTemplate(
        template = 'Please answer the following question in layman terms {user_query}',
        input_variables = ['user_query']
    )
    chain = prompt | model
    result = chain.invoke({'user_query': text})
    print(result)
    return result.content


@router.post("", response_model=ChatResponse)
async def chat_with_openai(request: ChatRequest) -> ChatResponse:
    """Process chat messages with OpenAI"""
    user_message = request.messages[-1].content if request.messages else ""
    response_text = query_llm(user_message)

    return ChatResponse(
        reply=response_text,
    )