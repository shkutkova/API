from pydantic import BaseModel, Field

class TokenResponseSchema(BaseModel):
    access_token: str = Field(..., alias="accessToken")