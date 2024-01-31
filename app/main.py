from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os


app = FastAPI()

dir_static = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'static')
dir_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
print(f"dir_static: {dir_static}")
print(f"dir_templates: {dir_templates}")

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory=dir_static), name="static")

templates = Jinja2Templates(directory=dir_templates)


# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/static", StaticFiles(directory=os.path.join(
#     os.path.dirname(os.path.realpath(__file__)),
#     os.pardir,
#     'static')
# ), name="static")

@app.get("/bb", response_class=HTMLResponse)
async def read(request: Request):
    return templates.TemplateResponse("bb.html", {"request": request})


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )

# @app.get("/", response_class=HTMLResponse)
# async def read_bb(request: Request):
#     # print(dir(templates))
#     # return {"ok"}
#     r = templates.TemplateResponse("bb.html", {"request": request})
#     print(r)
#     return r
#     # return templates.TemplateResponse(
#     #     request=request, name="bb.html"
#     # )


@app.get("/")
async def root():
    return {"message": "Hello World"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8002)
    