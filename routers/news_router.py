from fastapi import APIRouter

v1_news_router = APIRouter(prefix="/v1")

@v1_news_router.get("/news")
def get_news():
    return {"message": "Здесь будут новости"}