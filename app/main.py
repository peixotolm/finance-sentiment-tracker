from api.v1.endpoints.products import product_router
from fastapi import FastAPI

app = FastAPI()  # Define the app at the module level

app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
