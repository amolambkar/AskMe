"""
Purpose: Functionalities related to Question and Answer.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from services.process import create_context


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that provide me crisp answer from context : {context}",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm


def get_response(question: str) -> str:
    """
    Get response from llm
    """
    context = create_context(question)

    if len(context) < 10:
        return "Sorry unable to answer."
    res = chain.invoke(
        {
            "context": context,
            "input": question,
        }
    )
    return res.content
