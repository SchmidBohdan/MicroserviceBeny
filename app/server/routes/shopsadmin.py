from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
	retrieve_competitors,
	populate_competitors
)
from app.server.models.competitor import (
	ErrorResponseModel,
	ResponseModel
)


router = APIRouter()


@router.get("/", response_description="Shopsadmin")
async def get_retrieve_competitors():
	shopsadmins = await retrieve_competitors()
	if shopsadmins:
		return ResponseModel(shopsadmins, "Shopsadmin is successfully")
	return ResponseModel(shopsadmins, "Empty list returned")