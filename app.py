import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Cloudhaven Agent")


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str


def cloudhaven_agent(query: str, api_key: str) -> str:
    """Simple agent that answers questions about capital cities."""
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0)

    system_prompt = """You are a helpful assistant that knows the capital cities of countries around the world.
When asked about a country's capital, provide the accurate capital city name."""

    messages = [
        ("system", system_prompt),
        ("human", query),
    ]

    response = llm.invoke(messages)
    return response.content


@app.get("/health", status_code=200)
def health():
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse, status_code=200)
def query(request: QueryRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    answer = cloudhaven_agent(request.query, api_key)
    return QueryResponse(answer=answer)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
