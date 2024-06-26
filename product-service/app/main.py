from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .web.route import router
from .web.csg_route import csg_router
from .core.db import create_db_and_tables


@asynccontextmanager 
async def life_span(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Product Service",
    description="This is a product service",
    version="1.0.0",
    terms_of_service="https://caxgpt.vercel.app/terms/",
    lifespan=life_span,
    contact={
        "name": "Muhammad Ahsaan Abbasi",
        "phone": "+92 349-204-7381",
        "email": "mahsaanabbasi@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    root_path="/product-service",
    root_path_in_servers=True,
    docs_url="/docs"
)

# SessionMiddleware must be installed to access request.session
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.router.include_router(router=router, tags=["Product Service"])
app.router.include_router(router=csg_router, tags=["Category, Size & Gender Service"])

@app.get("/")
def get_root():
    return {"message": "welcome to Product Service, Create Product, Product Detail, Specific Product Detail, Search Product, Delete Product"}
