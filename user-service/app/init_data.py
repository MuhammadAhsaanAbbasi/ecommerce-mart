# import asyncio
# import datetime
# from typing import Annotated
# from fastapi import Depends
# from university_gpt.core.config import logger_config
# from university_gpt.core.db import Session, get_session, engine
# from sqlmodel import select
# from university_gpt.model.models import (
#     University,
#     Program,
#     Course,
#     Users,
#     Admin,
# )
# from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

# max_tries = 3
# wait_seconds = 1

# university_name = "ʌɓɓʌşï GPT-Tech"

# # Extract the data outside of the function
# logger = logger_config(__name__)
# logger.info("Seeding database")

# #admin
# admin = Admin(
#     username="ʌɓɓʌşï",
#     email="abbasi@gmail.com",
#     hashed_password="abbasi@123",
#     is_verified=True,
#     otp="123456"
# )

# # University
# university = University(
#     university_name=university_name,
#     university_desc="The University of ʌɓɓʌşï GPT-Tech is a leading educational institution of Technology",
#     admins=admin
# )

# async def init_db_seed(session: Annotated[Session, Depends(get_session)]):
#     logger = logger_config(__name__)
#     logger.info("Seeding database")
    
#     #admin
#     admin_seed = admin
    
#     # University
#     university_seed = university
    
#     session.add_all([admin_seed, university_seed])
#     session.commit()


# @retry(
#     stop=stop_after_attempt(max_tries),
#     wait=wait_fixed(wait_seconds),
#     before=before_log(logger, 200),
#     after=after_log(logger, 300),
# )
# async def init_db():
#     try:
#         logger.info("init_db Up")
#         with Session(engine) as session:
#             logger.info("Checking if Database is already seeded")
#             university_req = session.exec(
#                 select(University).where(University.university_name == university_name)
#             )
#             university = university_req.one_or_none()
#             print("\n\nuniversity\n\n", university, "\n\n")
#             if university is None:
#                 logger.info("Database not seeded. Seeding Database")
#                 await init_db_seed(session=session)
#             else:
#                 logger.info("Database already seeded")
#                 return {"message": "Database already seeded"}
#     except Exception as e:
#         logger.error(e)
#         raise e


# if __name__ == "__main__":
#     logger.info("In Initial Data Seeding Script")
#     asyncio.run(init_db())
#     logger.info("Database Seeding Completed!")
#     logger.info("Database is Working!")
#     logger.info("Backend Database Initial Data Seeding Completed!")