import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend import api_router
from config import HOST
from frontend import fr_router

sentry_sdk.init(
    dsn='https://857a65a61d271a75c69f6934a0e9bf16@o4505749463105536.ingest.sentry.io/4505749549744128',
    traces_sample_rate=1.0,
)

app = FastAPI(title='ZXCTube')

app.include_router(api_router)
app.include_router(fr_router)


app.mount('/frontend/static', StaticFiles(directory='frontend/static'), name='static')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host=HOST)
