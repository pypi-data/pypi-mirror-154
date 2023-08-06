from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apiautomata.routes import echo, home, missing, proxy

app = FastAPI()

app.include_router(home.router)
app.include_router(echo.router)
app.include_router(proxy.router)
app.include_router(missing.router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup_event():
    print('Starting...')


@app.on_event('shutdown')
async def shutdown_event():
    print('Stopping...')
