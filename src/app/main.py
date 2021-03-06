from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from celery.result import AsyncResult
from PIL import Image

from app.celery_worker import resize_image_task
from app.files import PATH_FILES_ORIGINAL, PATH_FILES_RESIZED

app = FastAPI()

@app.get("/ping")
def ping():
    return "pong"

@app.post('/resize/image')
async def resize_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(PATH_FILES_ORIGINAL / file.filename, 'wb+') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=400, detail={"error": "There was an error uploading the file"})

    try: 
        img = Image.open(PATH_FILES_ORIGINAL / file.filename, mode="r")
    except:
         raise HTTPException(status_code=400, detail={"error": "Invalid image"})
    try:
        image = {'filename': file.filename, "image_size": str(img.size)}
        task = resize_image_task.delay(image)
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "There was an error resizing the file"})
    finally:
        await file.close()
    return {
        "message": f"Successfully uploaded {file.filename}",
        "task_id": str(task), 
        "task_status": "Processing"
    }

@app.get("/results/{task_id}")
async def task_results(task_id:str):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(
            status_code=202,
            content={
                "task_id": str(task_id), 
                "task_status": "Processing"
                })
    result = task.get()
    return {
        "task_id": str(task_id), 
        "task_status": "Succeeded",
        "outcome": result
        }

@app.get("/image/download/{task_id}")
async def image_download(task_id:str):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(
            status_code=202,
            content={
                "task_id": str(task_id), 
                "task_status": "Processing"
                })
    result = task.get()
    filename = result.get('filename')
    image_path = PATH_FILES_RESIZED / filename
    return FileResponse(image_path)