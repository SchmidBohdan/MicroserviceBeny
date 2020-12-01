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


@router.get("/", response_description="Competitors retrieved")
async def get_competitors():
	competitors = await retrieve_competitors()
	if competitors:
		return ResponseModel(competitors, "Competitors data retrieved successfully")
	return ResponseModel(competitors, "Empty list returned")

@router.get("/populate_competitors", response_description="Populate competitors")
async def get_populate_competitors():
	shopsadmins = await populate_competitors()
	if shopsadmins:
		return ResponseModel(shopsadmins, "Population competitors is successfully")
	return ResponseModel(shopsadmins, "Empty list returned")