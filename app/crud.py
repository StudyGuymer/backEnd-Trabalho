# app/crud.py
from .config import POSTGREST_URL, TABLE_NEWS, SUPABASE_ANON_KEY
import httpx
from typing import Dict, Any, Optional
from uuid import UUID

def postgrest_headers(auth):
    # auth can be a dict result from verify_supabase_token or None
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    # If the client passed a "provider token" we might want to forward Authorization to PostgREST
    if isinstance(auth, dict) and "access_token" in auth:
        headers["Authorization"] = f"Bearer {auth['access_token']}"
    return headers

async def list_news(limit:int=100, offset:int=0, auth=None):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{POSTGREST_URL}/{TABLE_NEWS}", headers=postgrest_headers(auth), params={"select":"*","order":"created_at.desc","limit":limit,"offset":offset})
    r.raise_for_status()
    return r.json()

async def get_news(news_id: UUID, auth=None) -> Optional[Dict[str,Any]]:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{POSTGREST_URL}/{TABLE_NEWS}", headers=postgrest_headers(auth), params={"id":f"eq.{news_id}","select":"*"})
    if r.status_code == 404 or r.json() == []:
        return None
    r.raise_for_status()
    data = r.json()
    return data[0] if isinstance(data, list) and data else data

async def create_news(payload: Dict[str,Any], auth=None):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{POSTGREST_URL}/{TABLE_NEWS}", headers=postgrest_headers(auth), json=payload)
    r.raise_for_status()
    # PostgREST returns created object when return=representation
    return r.json()

async def update_news(news_id: UUID, payload: Dict[str,Any], auth=None):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.patch(f"{POSTGREST_URL}/{TABLE_NEWS}", headers=postgrest_headers(auth), params={"id":f"eq.{news_id}"}, json=payload)
    r.raise_for_status()
    return r.json()

async def delete_news(news_id: UUID, auth=None):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.delete(f"{POSTGREST_URL}/{TABLE_NEWS}", headers=postgrest_headers(auth), params={"id":f"eq.{news_id}"})
    r.raise_for_status()
    return True
