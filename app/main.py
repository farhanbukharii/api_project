from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import users, generate
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
import os
from app.routers import users


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")

app = FastAPI(
    title="My API",
    description="API with OAuth2PasswordBearer",
    version="1.0.0"
)
@app.get("/")
def read_root():
    return {"message": "API is working. Visit /frontend for UI."}

# Serve static files (HTML frontend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/frontend", StaticFiles(directory=static_path, html=True), name="static")



# Include routers
app.include_router(users.router)
app.include_router(generate.router)
app.include_router(users.router)