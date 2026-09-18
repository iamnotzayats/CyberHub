from fastapi import FastAPI

from routers import news_router, parameters_router

app = FastAPI()

app.include_router(news_router.v1_news_router)
app.include_router(parameters_router.v1_settings_router)


