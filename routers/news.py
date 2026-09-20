from fastapi import APIRouter, Depends, status,HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.models import News
from fastapi import Query

from slugify import slugify

from sqlalchemy import select


v1_news_router = APIRouter(prefix="/v1")


@v1_news_router.post("/new/create", status_code=201)
async def create_news(
    title: str = Query(..., min_length=1, max_length=255),
    content: str = Query(..., min_length=1),
    is_published: bool = Query(False),
    session: AsyncSession = Depends(get_session),
):
    slug = slugify(title)
    news = News(title=title, content=content, is_published=is_published, slug=slug)
    session.add(news)
    await session.commit()
    await session.refresh(news)
    return news

@v1_news_router.get(
    "/news/get/all",
    tags=["news"],
)
async def get_list_news(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200, description="Сколько записей вернуть"),
    offset: int = Query(0, ge=0, description="Сколько пропустить"),
    only_published: bool = Query(False, description="Только опубликованные"),
):
    stmt = select(News).order_by(News.created_at.desc())
    if only_published:
        stmt = stmt.where(News.is_published.is_(True))
    stmt = stmt.limit(limit).offset(offset)

    result = await session.execute(stmt)
    return result.scalars().all()

@v1_news_router.get("/news/{slug}", tags=["news"])
async def get_news_by_slug(
    slug: str = Path(..., min_length=1),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(News).where(News.slug == slug))
    news = result.scalar_one_or_none()

    if news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    return news

@v1_news_router.patch("/news/update/{slug}", tags=["news"])
async def update_news(
    slug: str = Path(..., min_length=1),
    title: str | None = Query(None, min_length=1, max_length=255),
    content: str | None = Query(None, min_length=1),
    is_published: bool | None = Query(None),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(News).where(News.slug == slug))
    news = result.scalar_one_or_none()
    if news is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    if title is not None:
        news.title = title
    if content is not None:
        news.content = content
    if is_published is not None:
        news.is_published = is_published

    await session.commit()
    await session.refresh(news)
    return news 