from pydantic import BaseModel, Field

class DBQueryInputSchema(BaseModel):
    entities: dict = Field(description="Diccionario de entidades extraídas del texto del usuario.")