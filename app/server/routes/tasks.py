from fastapi import APIRouter, Body

from app.server.database import (
	populate_competitors,
	disable_users
)
from app.server.models.competitor import (
	ResponseModel
)


router = APIRouter()


@router.get("/populate_competitors", response_description="Populate competitors")
async def get_populate_competitors():
	pop_comp = await populate_competitors()
	if pop_comp:
		return ResponseModel(pop_comp, "Population competitors - done.")
	

@router.get("/disable_users", response_description="Disable users with expired shops")
async def get_disable_users_with_expired_shops():
	dis_users = await disable_users()
	if dis_users:
		return ResponseModel(dis_users, "Disable users with expired shops - done.")
