from routers import product_description
from routers import files_mgmt
from routers import settings
from fastapi import FastAPI
# import uvicorn


app = FastAPI()

app.include_router(files_mgmt.router)
app.include_router(product_description.router)
app.include_router(settings.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)