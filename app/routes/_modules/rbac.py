# from fastapi import FastAPI, Request, HTTPException, Depends
# import httpx
# from httpx import AsyncClient, HTTPStatusError
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from starlette.responses import JSONResponse
# from dotenv import load_dotenv
# import os
# import routes._path.ms_paths as MS
# from routes._path.api_paths import LOGIN_WITH_MS, AUTH_CALLBACK


# class TokenVerifyMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
#         if request.url.path == LOGIN_WITH_MS or request.url.path == AUTH_CALLBACK:
#             return await call_next(request)
#         access_token = request.cookies.get("access_token")
#         if not access_token:
#             return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
#         async with AsyncClient() as client:
#             headers={"Authorization": f"Bearer {access_token}"}
#             try:
#                 user_response = await client.get(
#                     MS.MS_USER_INFO_URL,
#                     headers=headers
#                 )
#                 user_response.raise_for_status()
#             except HTTPStatusError as e:
#                 return JSONResponse({"error": "Unauthorized"}, status_code=401)
            
#         return await call_next(request)