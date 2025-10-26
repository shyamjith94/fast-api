from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core import settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.depends import Database
# route
from app.api import routes



# app events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Simple DB connection check
    try:
        Database(check_connection=True)
    except Exception as e:
        print("Database connection failed:", e)
        raise e

    # Run the app
    yield

    # Shutdown logic


    

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_TAG}/openapi.json",
    docs_url="/docs",
    readoc_url="/readdoc",
    lifespan=lifespan,  # modern startup/shutdown handler
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)



app.include_router(router=routes.product_router, prefix=f"{settings.API_TAG}/v1", tags=["product"])
app.include_router(router=routes.category_router, prefix=f"{settings.API_TAG}/v1", tags=["category"])



@app.get("/")
def home():
    return {"message": "Hello, FastAPI with VS Code!"}