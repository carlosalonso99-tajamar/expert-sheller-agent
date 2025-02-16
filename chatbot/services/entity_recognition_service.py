from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Crear el modelo de lenguaje
llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0.2,  # Baja temperatura para respuestas más precisas
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Lista de entidades a extraer
ENTITIES = ["precio", "modelo", "almacenamiento", "memoria", "gráfica", "procesador",
            "pantalla", "peso", "color", "audio"]

def identify_entities(text: str) -> dict:
    """
    Llama al modelo de lenguaje para detectar entidades en el texto.
    """
    prompt = f"""
    Extrae las siguientes entidades del texto proporcionado:
    - {", ".join(ENTITIES)}

    Devuelve los resultados en formato JSON. Si alguna entidad no está presente, omítela.

    Texto:
    {text}
    """

    response = llm.invoke(prompt)
    print(response.content)
    return response.content  # Devuelve la respuesta del modelo
