from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from src.tools import make_rag_tools
from langchain.schema import Document


def build_agent(docs: list[Document], model_name: str = "gpt-4o-mini", k: int = 3):
    llm = ChatOpenAI(model=model_name, temperature=0)
    tools = make_rag_tools(docs, model_name=model_name, k=k)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent