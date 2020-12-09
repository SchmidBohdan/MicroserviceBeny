from fastapi import APIRouter, Body

from app.server.database import retrieve_competitors
from app.server.models.competitor import (
	ResponseModel
)


router = APIRouter()


@router.get("/", response_description="Shopsadmin")
async def get_retrieve_competitors():
	shopsadmins = await retrieve_competitors()
	if shopsadmins:
		return ResponseModel(shopsadmins, "Shopsadmin is successfully")
	return ResponseModel(shopsadmins, "Empty list returned")