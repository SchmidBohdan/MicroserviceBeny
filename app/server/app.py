from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.server.routes.competitor import router as CompetiorRouter
from app.server.routes.crawl import router as CrawlRouter
from app.server.routes.shopsadmin import router as ShopsadminRouter
from app.server.routes.tasks import router as Tasks

app = FastAPI()

app.include_router(CompetiorRouter, tags=["Competitor"], prefix="/competitor")
app.include_router(CrawlRouter, tags=["Crawl"], prefix="/crawl")
app.include_router(ShopsadminRouter, tags=["Shopsadmin"], prefix="/shopsadmin")
app.include_router(Tasks, tags=["Tasks"], prefix="")


@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root():
	html_content = """
    <html>
        <body>
            <a href="http://0.0.0.0:8000/docs">Go to Swagger</a>
        </body>
    </html>
    """
	return HTMLResponse(content=html_content, status_code=200)