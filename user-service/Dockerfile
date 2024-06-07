FROM python:3.12

WORKDIR /user_workspace

RUN pip install poetry

COPY ./pyproject.toml /user_workspace/

RUN potry install

COPY . /user_workspace/

EXPOSE 8000

RUN ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
