# Flask Toolkits
[![Downloads](https://static.pepy.tech/personalized-badge/flask-toolkits?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/flask-toolkits)

## Repository
- [GITHUB](https://github.com/Danangjoyoo/flask-toolkits)

## Installation
```
pip install flask-toolkits
```

## Description
Flask toolkits implements and provides several features from `FastAPI` like:
- Automatic API documentation (define the function and we'll generate the `swagger`/`openapi` spec for you)
- Passing parameters through `view`/`router` function which is unable in `Flask` before
- Easy Middleware setup
- Parameters and schema validation using `Pydantic`
- Response classes that could return any type of data without worried to get error
- much more..


## Changelogs
- v0.0
    - First Upload
- v0.1
    - Integration with [flask-http-middleware](https://pypi.org/project/flask-http-middleware)
    - [pydantic](https://pypi.org/project/pydantic) support for JSON arguments and validation
    - Multiple response type generator
    - Added `JSONResponse` class to replace `jsonify` roles in send dictionary data with encoding improvements.
- v0.2
    - Supported enumeration API documentation
    - Added support for type hint from `typing`'s generic (ex: `Optional`, `Union`, `List`)
    - Fixed input parameter validations
- v0.3
    - Support `File` and `Form` input parameters validation and automatic swagger.
    - Added constraint feature for parameters (ex: limit, max/min length, greater/less than, equals than etc)

## Key Tools inside this `toolkit`
- Automatic API documentation (`swagger`/`openapi`)
- Request-Response direct HTTP middleware (`flask-http-middleware`)
- Automatic parameters validation (`pydantic`)
- Response generator (JSON, Plain Text, HTML)

## Automatic Parameters Validation
The original `Blueprints` class from `flask` can't insert most of arguments inside endpoint.
Here our `APIRouter` allows you to have arguments inside your endpoint
```
from typing import Optional
from flask_toolkits import APIRouter, Body, Header, Query
from flask_toolkits.responses import JSONResponse


router = APIRouter("email", import_name=__name__, static_folder="/routers/email", url_prefix="/email")


@router.post("/read", tags=["Email Router])
def get_email(
    id: int,
    name: Optional[str],
):
    return JSONResponse({"id": id, "name": name})

```

## AUTOMATIC API DOCUMENTATION
Here our `APIRouter` allows you to auto-documenting your endpoint through `AutoSwagger`.
Define the new router using `APIRouter` class, lets put it in another pyfile

`email_view.py`
```
from typing import Optional
from flask_toolkits import APIRouter, Body, Header, Query
from flask_toolkits.responses import JSONResponse


router = APIRouter("email", import_name=__name__, static_folder="/routers/email", url_prefix="/email")


@router.post("/read", tags=["Email Router])
def get_email(
    id: int = Body(...),
    name: Optional[str] = Body(...),
    token: int = Header(...),
    race: Optional[str] = Query(None)
):
    return JSONResponse({"id":id, "name": name})
```

`main.py`
```
from flask import Flask
from flask_toolkits import AutoSwagger

from email_view import router as email_router


app = Flask(__name__)

auto_swagger = AutoSwagger()

app.register_blueprint(email_router)
app.register_blueprint(auto_swagger)


if __name__ == "__main__":
    app.run()
```

then you can go to `http://localhost:5000/docs` and you will found you router is already documented

![alt text](https://github.com/Danangjoyoo/flask-toolkits/blob/main/docs/auto1.png?raw=true)

## Request-Response direct HTTP middleware
```
import time
from flask import Flask
from flask_toolkits.middleware import MiddlewareManager, BaseHTTPMiddleware

app = Flask(__name__)

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()
    
    def dispatch(self, request, call_next):
        t0 = time.time()
        response = call_next(request)
        response_time = time.time()-t0
        response.headers.add("response_time", response_time)
        return response

app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(MetricsMiddleware)

@app.get("/health")
def health():
    return {"message":"I'm healthy"}
```