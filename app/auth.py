# app/auth.py
from fastapi import Header, HTTPException, Depends, status
import httpx
from .config import SUPABASE_URL, SUPABASE_ANON_KEY

async def verify_supabase_token(authorization: str = Header(...)):
    """
    Espera header Authorization: Bearer <token>
    Verifica o token chamando o endpoint /rest/v1? uma abordagem simples: checar /auth/v1/user
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed authorization header")
    token = authorization.split(" ", 1)[1]
    # Chamar endpoint do Supabase para verificar token: /auth/v1/user
    url = f"{SUPABASE_URL}/auth/v1/user"
    headers = {"Authorization": f"Bearer {token}", "apiKey": SUPABASE_ANON_KEY}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return r.json()
