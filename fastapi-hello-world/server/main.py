# Visit: http://127.0.0.1:8000/hello

# FastAPI is a Python web framework that makes it easy to build APIs.
# We import FastAPI to create the application and define routes.
from fastapi import FastAPI

# FastAPI() creates the application instance — this is the central object that
# holds all routes, middleware, and configuration. Everything gets registered on it.
app = FastAPI()

# @app.get("/hello") is a route decorator. It tells FastAPI:
#   - Listen for HTTP GET requests on the path /hello
#   - When a request comes in, call the function below
# FastAPI registers this at startup so it's ready immediately when a request arrives.
@app.get("/hello")
def say_hello(name: str = "World"):
    # "name" is a query parameter — FastAPI reads it from the URL automatically.
    # If the URL is /hello?name=Walid, then name="Walid".
    # The default value "World" means if no ?name= is provided, name="World".
    # FastAPI does this without any extra parsing code — the type annotation (str)
    # tells FastAPI what type to expect and how to validate it.

    # Returning a Python dict is all you need — FastAPI automatically converts it
    # to a JSON response with the correct Content-Type header. No json.dumps() needed.
    return {"message": f"Hello {name}"}
