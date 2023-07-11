from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import Settings
from routes.users import user_router
from routes.events import event_router
import uvicorn

app = FastAPI()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

settings = Settings()

@app.on_event("startup")
async def init_db():
    await settings.init_database()

'''
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")
'''

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)