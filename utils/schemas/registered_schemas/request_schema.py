from pydantic import BaseModel, Field


class RegisteredRequestSchema(BaseModel):
    client_name: str = Field(..., alias="clientName") 
    client_email: str = Field(..., alias="clientEmail") 