#http://127.0.0.1:8000/hello

from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello(name: str = "World"):
    return {"message": f"Hello {name}"}
