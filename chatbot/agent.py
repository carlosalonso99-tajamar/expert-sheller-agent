from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import StdOutCallbackHandler
from chatbot.tools import ocr_tool, entity_tool, translation_tool, db_query_tool
from dotenv import load_dotenv
import os

load_dotenv()

# 🔹 Crear el modelo de lenguaje
llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# 🔹 Definir herramientas del agente
tools = [
    ocr_tool,
    entity_tool,
    db_query_tool,
    translation_tool
]

# 🔹 Instrucciones para el comportamiento del agente
instructions = """
Eres un asistente inteligente que ayuda con el procesamiento de texto. 

- Si el usuario envia **PDFs** o **documentos**, usa la herramienta OCR para extraer el texto.
- Si el usuario pregunta por informacion, tiene intencion de compra o da caracteristicas detalladas, usa la herramienta de **Entidades** para extraer informacion estructurada.
- Una vez usada la herramienta de **Entidades**, usa la herramienta de **Consulta_BD** para buscar productos en la base de datos.
- Si el usuario solicita **traducir** texto, usa la herramienta de **Traduccion**, si no aporta un mensaje usa tuultima respuesta.
- No preguntes si quieres usar una herramienta, simplemente ejecútala cuando sea necesario.
- Si el usuario no solicita nada relacionado con estas herramientas, responde como un chatbot normal con información relevante.
"""

# 🔹 Inicializar el agente con instrucciones personalizadas
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # Agente basado en razonamiento con funciones
    verbose=True,
    agent_kwargs={"system_message": instructions},  # 📌 Se añaden las instrucciones
    # memory=memory,
    # callbacks=[StdOutCallbackHandler()]
)
