# app/main.py
from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from uuid import UUID
from app import crud, schemas
from app.auth import verify_supabase_token

app = FastAPI(title="News API (Supabase + FastAPI)", version="1.0")

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}

@app.get("/news", response_model=List[schemas.NewsOut], tags=["news"])
async def list_news(limit: int = 100, offset: int = 0, auth=Depends(verify_supabase_token)):
    try:
        data = await crud.list_news(limit=limit, offset=offset, auth=auth)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/{news_id}", response_model=schemas.NewsOut, tags=["news"])
async def get_news(news_id: UUID, auth=Depends(verify_supabase_token)):
    try:
        item = await crud.get_news(news_id, auth=auth)
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/news", response_model=schemas.NewsOut, status_code=status.HTTP_201_CREATED, tags=["news"])
async def create_news(payload: schemas.NewsCreate, auth=Depends(verify_supabase_token)):
    try:
        item = await crud.create_news(payload.dict(exclude_none=True), auth=auth)
        # PostgREST may return list; handle
        if isinstance(item, list):
            item = item[0] if item else item
        return item
    except httpx.HTTPStatusError as ex:
        raise HTTPException(status_code=ex.response.status_code, detail=ex.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/news/{news_id}", response_model=schemas.NewsOut, tags=["news"])
async def patch_news(news_id: UUID, payload: schemas.NewsUpdate, auth=Depends(verify_supabase_token)):
    try:
        updated = await crud.update_news(news_id, payload.dict(exclude_none=True), auth=auth)
        # PostgREST returns number or empty; re-fetch
        item = await crud.get_news(news_id, auth=auth)
        if not item:
            raise HTTPException(status_code=404, detail="Not found after update")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/news/{news_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["news"])
async def delete_news(news_id: UUID, auth=Depends(verify_supabase_token)):
    try:
        exists = await crud.get_news(news_id, auth=auth)
        if not exists:
            raise HTTPException(status_code=404, detail="Not found")
        await crud.delete_news(news_id, auth=auth)
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
