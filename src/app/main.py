from fastapi import FastAPI, File, HTTPException, UploadFile

from app.celery_worker import resize_image_task
from app.core.files import PATH_FILES_ORIGINAL

app = FastAPI()

@app.get("/ping")
def ping():
    return "pong"

@app.post('/resize/image')
async def resize_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(PATH_FILES_ORIGINAL+ file.filename, 'wb+') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=400, detail={"error": "There was an error uploading the file"})

    try: 
        task = resize_image_task.delay(file.filename)
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "There was an error resizing the file"})
    finally:
        await file.close()
    return {
        "message": f"Successfully uploaded {file.filename}",
        "task_id": str(task), 
        "task_status": "Processing"
    }