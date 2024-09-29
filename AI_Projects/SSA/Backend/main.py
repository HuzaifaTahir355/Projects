import routers
from fastapi import FastAPI
# import uvicorn

app = FastAPI()

app.include_router(routers.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)