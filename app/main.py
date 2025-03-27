from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time
import os
from app.servernvp.router import nvp_route
from app.utils.logger.logger import logger

app = FastAPI()

dir_static = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'static')
dir_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
app.mount("/static", StaticFiles(directory=dir_static), name="static")
templates = Jinja2Templates(directory=dir_templates)

app.include_router(
    nvp_route,
    prefix="/nvp"
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    logger.info(f"req: {request.url}")
    if request.headers.get('content-type') == 'application/x-www-form-urlencoded':
        a = dict(await request.form())
        logger.info(f"content: {a}")
    if request.headers.get('content-type') == 'multipart/form-data':
        b = dict(await request.form())
        logger.info(f"content: {b}")
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"req: {request.url}, res:{response.status_code}, time={process_time}")
    # logger.info("resp: %s ", response.status_code)
    # response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/bb", response_class=HTMLResponse)
async def read(request: Request):
    return templates.TemplateResponse("form_upload.html", {"request": request})

@app.get("/")
async def root():
    h = "aaaa"
    return Response(content=h, status_code=200)
    # return {"message": "Hello "}

    