import uvicorn
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from backend import api_router
from config import HOST
from frontend import fr_router

app = FastAPI(title='ZXCTube')

#app.add_middleware(
#    TrustedHostMiddleware, allowed_hosts=["zxctube.ru"]
#)

#@app.middleware("http")
#async def force_https(request: Request, call_next):
#    scheme = request.headers.get("X-Forwarded-Proto", "http")
#    print(scheme)
#    if scheme == "http":
#        url = str(request.url)
#        url = url.replace(scheme, "https")
#        response = RedirectResponse(url, status_code=301)
#        return response
#    return await call_next(request)

app.include_router(api_router)
app.include_router(fr_router)

app.mount('/frontend/static', StaticFiles(directory='frontend/static'), name='static')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host=HOST)
