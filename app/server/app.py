from fastapi import FastAPI

from app.server.routes.competitor import router as CompetiorRouter
from app.server.routes.crawl import router as CrawlRouter
from app.server.routes.shopsadmin import router as ShopsadminRouter

app = FastAPI()

app.include_router(CompetiorRouter, tags=["Competitor"], prefix="/competitor")
app.include_router(CrawlRouter, tags=["Crawl"], prefix="/crawl")
app.include_router(ShopsadminRouter, tags=["Shopsadmin"], prefix="/shopsadmin")


@app.get("/", tags=["Root"])
async def read_root():
	return {"message": "Welcome to Beny Microcervise!"}