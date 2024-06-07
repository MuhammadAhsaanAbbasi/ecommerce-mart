# from fastapi import FastAPI
# from starlette.middleware.sessions import SessionMiddleware
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from .web.route  import router
# from .core.db import create_db_and_tables
# from .model.models import Users


# @asynccontextmanager
# async def life_span(app: FastAPI):
#     print("Hello World..!!!")
#     create_db_and_tables()
#     yield

# app = FastAPI(
#     title="University GPT",
#     description="A GPT University or Program that will help to create whole university program with GPT and also help to create a Quizz for Students!",
#     version="1.0.0",
#     terms_of_service="https://caxgpt.vercel.app/terms/",
#     lifespan=life_span,
#     contact={
#         "name": "Muhammad Ahsaan Abbasi",
#         "url": "http://localhost:8000/contact/",
#         "email": "mahsaanabbasi@gmail.com",
#     },
#     license_info={
#         "name": "Apache 2.0",
#         "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
#     },
#     servers=[
#         {
#             "url": "http://localhost:8000",
#             "description": "Local server"
#         },
#     ],
#     docs_url="/docs"
# )

# # SessionMiddleware must be installed to access request.session
# app.add_middleware(
#     SessionMiddleware, secret_key="!secret")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "DELETE", "PUT"],
#     allow_headers=["*"],
# )

# app.router.include_router(router, tags=["OAuth2 Authentication"])

# @app.get("/")
# def get_root():
#     return {"message": "welcome to login System"}