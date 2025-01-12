from fastapi import FastAPI
from api import auth, events, nutrition
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(events.router, prefix='/calendar', tags=['Calendar Events'])
app.include_router(nutrition.router, prefix='/nutrition', tags=['Nutrition'])

if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=8000)
