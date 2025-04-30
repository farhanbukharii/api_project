from fastapi import FastAPI
from app.routers import users, generate
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuth2 as OAuth2Model
from fastapi.security import OAuth2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, API is working!"}

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

app.include_router(users.router)
app.include_router(generate.router)