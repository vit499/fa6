from fastapi import APIRouter, Request, File, Form, Depends, HTTPException, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from starlette.responses import Response
from typing import Optional
from starlette.status import HTTP_404_NOT_FOUND
from typing import Union
import os
from app.settings import settings
from app.utils.logger.logger import logger

nvp_route = APIRouter()

# dir_nvp = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir,  os.pardir, 'nvpfiles')

# handler для устройства, загрузка файла настроек от устройства на сервер
@nvp_route.post('/nvp')
async def nvp_upload(request: Request, object_imei: str = Form(None), file: Optional[UploadFile] = File(None)):
    logger.info("post upload")

    # data = await request.form()
    # object_imei = data.get("object_imei")
    logger.info(f"object_imei: {object_imei}")

    if file is None:
        logger.info("file is None")
        return Response(content = '0000', media_type = "text/plain")
    fn = file.filename
    fsrc = file.file.read()
    len_dump = (fsrc[7] << 24) + (fsrc[6] << 16) + (fsrc[5] << 8) + fsrc[4]
    len_rec = len(fsrc)
    logger.info(f"len_dump: {hex(len_dump)}, len_rec: {hex(len_rec)}, fn: {fn}")
    if(len_rec < len_dump):
        logger.info(f"file len = {len_rec} len_dump={len_dump}")
        return Response(content = '0000', media_type = "text/plain")
    
    # file_name = f"{dir_nvp}/{object_imei}.nvp"
    # file_name_с = f"{dir_nvp}/{object_imei}_c.nvp"
    file_name = os.path.join(settings.NVP_PATH, f"{fn}{object_imei}.nvp")
    file_name_c = os.path.join(settings.NVP_PATH, f"{fn}{object_imei}_c.nvp")
    logger.info(f"-------------- file_name = {file_name}")
                
    with open(file_name, "wb") as f:
        f.write(fsrc)
    with open(file_name_c, "wb") as f:
        f.write(fsrc)
    crc_file = get_crc16_dump(file_name)
    # save_crc_file_to_db(object_imei, None, crc_file)
    # flags_redis_wpro.set_key_getfile(object_imei, "1")
    res = Response(content = '1111', media_type = "text/plain")   
    return res


# handler для устройства, скачивание файла настроек устройством с сервера частями
@nvp_route.get("/{object_imei}/downnvp")   
async def send_file(object_imei: str, offset: int = 0, limit: int = 0x400, fpro: str = "x", reqcrc: int = 0):
    b_file = b""
    res = b""
    len_dst = 1
    # file_name = f"{dir_nvp}/{object_imei}_c.nvp"
    if(fpro == "x"):
        logger.info(f"file error: {fpro} not exist")
        raise HTTPException(HTTP_404_NOT_FOUND)
    file_name = os.path.join(settings.NVP_PATH, f"{fpro}{object_imei}_c.nvp")
    if os.path.exists(file_name) != True:
        logger.info(f"file error: {file_name} not exist, {os.path.exists(file_name)}")
        raise HTTPException(HTTP_404_NOT_FOUND)
    len_file = os.path.getsize(file_name)
    if len_file < (offset + limit):
        logger.info(f"file error: {object_imei}.nvp, len_file: {len_file}")
        raise HTTPException(HTTP_404_NOT_FOUND)
    with open(file_name, "rb") as f:
        f.seek(offset)           
        b_file = f.read(limit)
    crc16 = get_crc16(b_file, limit)
    res = b_file + crc16.to_bytes(2, byteorder='big')               
    len_dst = limit + 2
    logger.info(f"file: {object_imei}.nvp, crc16: {hex(crc16)}, len_dst: {len_dst}")
    if reqcrc > 0:   # требуется контрольная сумма всего дампа в конце пакета
        crc16 = get_crc16_dump(file_name) 
        res = res + crc16.to_bytes(2, byteorder='big')
        len_dst = limit + 4          
        logger.info(f"file: {object_imei}.nvp, crc16: {hex(crc16)}, len_dst: {len_dst}")
    return Response(content=res, media_type="application/octet-stream")


# def get_crc16_dump(file_name):
#     crc16 = 0
#     with open(file_name, "rb") as f:
#         f.seek(0)                
#         resb = f.read(8)   # тут хранится длина дампа
#         len_dump = (resb[7] << 24) + (resb[6] << 16) + (resb[5] << 8) + resb[4]
#         f.seek(16)
#         resb = f.read(len_dump)
#         crc16 = calc_crc.get_crc16(resb, len_dump)
#     return crc16


def crc16_1(d, crc16):
    w = (d ^ crc16) & 0xff
    i = 8
    while i > 0:
        if (w & 1) != 0:
            w = (w >> 1) & 0xffff # w >>= 1
            w = (w ^ 0x8408) & 0xffff  # w ^= 0x8408
        else:
            w = (w >> 1) & 0xffff # w >>= 1
        i -= 1
    crc16 = (w ^ (crc16 >> 8)) & 0xffff
    return crc16

def get_crc16(buf, len):
    crc16 = 0xffff
    for i in range(len):
        crc16 = crc16_1(buf[i], crc16)
    return crc16

def get_crc16_dump(file_name):
    crc16 = 0
    if os.path.exists(file_name) != True:
        return crc16
    with open(file_name, "rb") as f:
        f.seek(0)                
        resb = f.read(8)   # тут хранится длина дампа
        len_dump = (resb[7] << 24) + (resb[6] << 16) + (resb[5] << 8) + resb[4]
        f.seek(16)
        resb = f.read(len_dump)
        crc16 = get_crc16(resb, len_dump)
    return crc16



