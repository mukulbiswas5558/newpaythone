from fastapi import FastAPI
from app.database import db
from app.routers.users import router as user_router

app = FastAPI(
    title="ERP API",  # Change the title of the API
    description="ERP for API.",  # Add or change the description
    version="1.0.0",  # Update the version if needed
    openapi_url="/dx/openapi.json",  # Change the OpenAPI schema URL
    docs_url="/dx/",  # Change the Swagger UI documentation URL
    redoc_url="/dc/",  # Change the ReDoc documentation URL
)


# Startup and Shutdown events
@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
