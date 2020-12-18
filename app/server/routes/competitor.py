from fastapi import APIRouter, Body

from app.server.database import retrieve_competitors
from app.server.models.competitor import (response_model)

router = APIRouter()


@router.get("/", response_description="Competitors retrieved")
async def get_competitors():
	competitors = await retrieve_competitors()
	if competitors:
		return response_model(competitors, "Competitors data retrieved successfully")
	return response_model(competitors, "Empty list returned")