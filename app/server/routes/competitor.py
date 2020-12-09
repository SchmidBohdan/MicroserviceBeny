from fastapi import APIRouter, Body

from app.server.database import retrieve_competitors
from app.server.models.competitor import (ResponseModel)

router = APIRouter()


@router.get("/", response_description="Competitors retrieved")
async def get_competitors():
	competitors = await retrieve_competitors()
	if competitors:
		return ResponseModel(competitors, "Competitors data retrieved successfully")
	return ResponseModel(competitors, "Empty list returned")