FROM python:3.13-slim AS build
WORKDIR /build
RUN pip3 install poetry && poetry self add poetry-plugin-export
COPY . /build
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.13-slim
WORKDIR /app
COPY --from=build /build/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
RUN pip3 install .
ENTRYPOINT [ "python3", "/app/feedzgerald/app.py"]
