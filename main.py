import uvicorn
from fastapi import FastAPI

# from db import db, engine
from routers import router

app = FastAPI()

# app.state.database = db
#
#
# @app.on_event('startup')
# async def startup():
#     db_ = app.state.database
#     if not db_.is_connected:
#         await db_.connect()
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     db_ = app.state.database
#     if db_.is_connected:
#         await db_.disconnect()

app.include_router(router, prefix='/video', tags=['Video'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8001)
