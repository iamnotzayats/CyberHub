from fastapi import FastAPI

from routers import news, parameters

app = FastAPI()

app.include_router(news.v1_news_router)
app.include_router(parameters.v1_settings_router)


