from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
	retrieve_crawls
)
from app.server.models.competitor import (
	ErrorResponseModel,
	ResponseModel,
)


router = APIRouter()


@router.get("/", response_description="Crawls retrieved")
async def get_crawl():
	crawls = await retrieve_crawls()
	if crawls:
		return ResponseModel(crawls, "Crawls data retrieved successfully")
	return ResponseModel(crawls, "Empty list returned")