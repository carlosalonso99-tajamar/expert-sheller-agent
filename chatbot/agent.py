from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from chatbot.tools import extract_text_from_pdf  # OCR tool
from dotenv import load_dotenv
import os
load_dotenv()
# Crear el modelo de lenguaje
llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0.7,
    openai_api_key= os.getenv("OPENAI_API_KEY")
)

# Definir herramientas del agente
tools = [
    Tool(
        name="OCR",
        func=extract_text_from_pdf,
        description="Extrae texto de un PDF usando OCR"
    )
]

# Inicializar el agente
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # Agente basado en razonamiento
    verbose=True,
    
)
