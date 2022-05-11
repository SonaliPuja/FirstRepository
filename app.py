from fastapi import FastAPI, File, UploadFile, Request,Form, APIRouter, Query, Header,Depends,HTTPException
import aiofiles
from config import *
import random
import shutil
import os
from faqbot_parse import *
from fastapi.responses import FileResponse
import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from enum import Enum
from fastapi.openapi.utils import get_openapi
from util import *
from zipfile import ZipFile
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

async def valid_content_length(content_length: int = Header(..., lt=1_000_000)):
    return content_length

class Type_Format(str, Enum):
    faqbot = "Faqbot"
    taskbot  = "Taskbot"

#todo - add try and catch 1. to check file is uplodade fine or not and second that value is between 0 or 1
# check that folder is uploaded in correct format
# todo - handle big files
# todo - delete zip file and domain folder and result file
# todo - make folders automatically


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile,bot_type :Type_Format = Type_Format.faqbot):
    '''upload a file in zip format.
    Pass second argument as number 0 for faqbot and 1 for taskbot,
    Assumptions:
    1. The training file is train.txt '''
    print("it is coming")
    n = random.randint(0, 1000000)
    filename = os.path.join(path, str(n))

    filename = filename + ".zip"
    print(filename)

    file_object = file.file
    #create empty file to copy the file_object to
    upload_folder = open(filename, 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()

    #unzipping file
    # importing required modules


    # specifying the zip file name
    file_name = filename

    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall(str(n))
        print('Done!')

    if bot_type.value == "Faqbot":
        result = faqbotparse(str(n))

    result_filename = str(n)+".json"
    with open(result_filename, 'w') as outfile:
        json.dump(result, outfile)


    return FileResponse(result_filename)


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="MINDMELD PARSER",
#         version="1.1",
#         description="Mindmeld parser parses the mindmeld training data and convert it into sandbox consumable form",
#         routes=app.routes,
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


@app.get("/")
def home(request:Request,response_class=HTMLResponse):
    """
    Displays the home page
    :return:
    """
    return templates.TemplateResponse("upload.html",{"request":request})


@app.post("/submitform",dependencies=[Depends(valid_content_length)])
async def handle_form(test:UploadFile = File(...)):

    print(test.filename)
    print(test.content_type)
    if test.content_type not in ["application/zip"]:
        raise HTTPException(400, detail="Invalid document type")
    # create folder if not exist
    create_folder(zipfile_folder)
    create_folder(unzipped_folder)
    create_folder(result_folder)


    # generating file identification
    n = str(random.randint(0, 1000000))

    filename = os.path.join(zipfile_folder, n) + ".zip"
    #print(filename)
    file_object = test.file
    #create empty file to copy the file_object to
    try:
        upload_folder = open(filename, 'wb+')
        shutil.copyfileobj(file_object, upload_folder)
        upload_folder.close()
    except:
        return {"error":True, "message":"could not read zip file"}

    #unzip
    unzipped_file = os.path.join(unzipped_folder,n)
    with ZipFile(filename, 'r') as zip:
        zip.extractall(unzipped_file)
    #print(unzipped_file)
    os.system('find . -name ".DS_Store" -print -delete')

    # bot parsing
    error,result = faqbotparse(unzipped_file)
    if error == True:
        return {"error":True, "message":result}

    # saving result
    result_filename = os.path.join(result_folder,n) + ".json"
    with open(result_filename, 'w') as outfile:
        json.dump(result, outfile)
    #print(result_filename)

    # delete the zip file
    delete_file(filename)


    return FileResponse(result_filename, media_type='application/octet-stream',filename="faqbot.json")



#app.openapi = custom_openapi


@app.get("/upload", response_class=HTMLResponse)
def get_upload(request: Request):
    result = "Hello from upload.py"
    return templates.TemplateResponse('upload.html', context={'request': request, 'result': result})



# @app.post("/upload")
# async def upload(file: UploadFile = File(...)):
#     filename = os.path.join('path/to/', file.filename)
#     async with aiofiles.open(filename, 'wb') as f:
#         while content := await file.read(1024):  # async read chunk
#             await f.write(content)
#
#     return {"Uploaded File": file.filename}


#if os.path.exists(filepath)