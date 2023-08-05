# Pyutter

## What is it

Pyutter is a python package that allows easy and fast simple front end development with python.

## Example
```
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pyutter.core.primitive import View
from pyutter.widgets.text import H1

root = View([H1(child=["Hello World"])])

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
async def demo():
    return root()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
```

## Main Features

* Basic material component Card, Chip and Appbar
* Layout components Column, Row, Grid ...
* Ability to return server side function using Function and State

## How to get it

`pip install pyutter`

## Dependency

[FastAPI](https://fastapi.tiangolo.com/)

[uvicorn](https://www.uvicorn.org/)