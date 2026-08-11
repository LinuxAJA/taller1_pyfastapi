from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class TraineeSchema(BaseModel):
    tipo_doc: str = Field(..., description="Tipo de documentos del aprendiz (CC, TI, CE)", pattern="^(CC|TI|CE)$", example="CC")
    documento: str = Field(..., description="Número de documento del aprendiz", min_length=6, max_length=10, pattern="^[0-9]+$", example="123456789")
    nombre: str = Field(..., description="Nombre del aprendiz", min_length=2, max_length=50, example="Juan")
    ficha: str = Field(..., description="Número de ficha del aprendiz", min_length=6, max_length=10, pattern="^[0-9]+$", example="123456")
    programa: str = Field(..., description="Programa de formación del aprendiz", min_length=2, max_length=100, example="ADSO")
    email: EmailStr = Field(..., description="Correo electrónico del aprendiz", example="juan@sena.edu.co")    

class TraineeCreate(TraineeSchema):
    pass

class TraineeUpdate(BaseModel):
    tipo_doc: Optional[str] = Field(None, description="Tipo de documentos del aprendiz (CC, TI, CE)", pattern="^(CC|TI|CE)$", example="CC")
    
    nombre: Optional[str] = Field(None, description="Nombre del aprendiz", min_length=2, max_length=50, example="Juan")
    ficha: Optional[str] = Field(None, description="Número de ficha del aprendiz", min_length=6, max_length=10, pattern="^[0-9]+$", example="123456")
    programa: Optional[str] = Field(None, description="Programa de formación del aprendiz", min_length=2, max_length=100, example="ADSO")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico del aprendiz", example="juan@sena.edu.co")    

class TraineeResponse(TraineeSchema):
    data: Optional[List[TraineeSchema]] = None # Datos consumidos de la API