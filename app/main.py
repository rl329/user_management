from builtins import Exception
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware  # Import the CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
from app.utils.translation import load_translations  # Import the load_translations function
import logging
from dotenv import load_dotenv
import os

load_dotenv()

print("SMTP_SERVER:", os.getenv("smtp_server"))
print("SMTP_PORT:", os.getenv("smtp_port"))
print("SMTP_USERNAME:", os.getenv("smtp_username"))
print("SMTP_PASSWORD:", os.getenv("smtp_password"))

logging.basicConfig(level=logging.INFO)

# Load translations into memory
load_translations()

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
# CORS middleware configuration
# This middleware will enable CORS and allow requests from any origin
# It can be configured to allow specific methods, headers, and origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed to access the server, ["*"] allows all
    allow_credentials=True,  # Support credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed HTTP headers
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)
    load_translations()  # Load translation files at application startup

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

app.include_router(user_routes.router)


