from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CompetitorSchema(BaseModel):
	excluded: str = Field(...)
	seller_url: str = Field(...)
	n_articles: int = Field(...)
	eans: list = []
	shop: str = Field(...)
	marketplace: str = Field(...)
	included: int = Field(...)
	seller_id: str = Field(...)
	user_email: EmailStr = Field(...)
	
	class Config:
		schema_extra = {
			"example": {
				"excluded": "0",
				"seller_url": "Miraherba",
				"n_articles": 1,
				"eans": ["4020943139359"],
				"shop": "1033",
				"marketplace": "1",
				"included": 1,
				"name": "Miraherba",
				"seller_id": "Miraherba-googleDE",
				"user_email": "weigert@vedes.com"
			}
		}


class UpdateCompetitorModel(BaseModel):
	excluded: str = Field(...)
	seller_url: str = Field(...)
	n_articles: int = Field(...)
	eans: list = []
	shop: str = Field(...)
	marketplace: str = Field(...)
	included: int = Field(...)
	seller_id: str = Field(...)
	user_email: EmailStr = Field(...)
	
	class Config:
		schema_extra = {
			"example": {
				"excluded": "0",
				"seller_url": "Miraherba",
				"n_articles": 1,
				"eans": ["4020943139359"],
				"shop": "1033",
				"marketplace": "5",
				"included": 1,
				"name": "Miraherba",
				"seller_id": "Miraherba-googleDE",
				"user_email": "123@babyland.de"
			}
		}


def response_model(data, message):
	return {
		"data": [data],
		"code": 200,
		"message": message,
	}


def error_response_model(error, code, message):
	return {"error": error, "code": code, "message": message}