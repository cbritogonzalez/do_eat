from fastapi import FastAPI
from api import auth, events
import uvicorn

app = FastAPI()

app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(events.router, prefix='/calendar', tags=['Calendar Events'])

if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=8000)
