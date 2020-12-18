from fastapi import APIRouter, Body

from app.server.database import retrieve_crawls
from app.server.models.competitor import (
	error_response_model,
	response_model,
)


router = APIRouter()


@router.get("/", response_description="Crawls retrieved")
async def get_crawl():
	crawls = await retrieve_crawls()
	if crawls:
		return response_model(crawls, "Crawls data retrieved successfully")
	return response_model(crawls, "Empty list returned")