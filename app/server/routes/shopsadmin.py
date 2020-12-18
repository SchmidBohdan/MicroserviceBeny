from fastapi import APIRouter, Body

from app.server.database import retrieve_competitors
from app.server.models.competitor import (
	response_model
)


router = APIRouter()


@router.get("/", response_description="Shopsadmin")
async def get_retrieve_competitors():
	shopsadmins = await retrieve_competitors()
	if shopsadmins:
		return response_model(shopsadmins, "Shopsadmin retrieved successfully")
	return response_model(shopsadmins, "Empty list returned")