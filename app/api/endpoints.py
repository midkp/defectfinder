# app/api/endpoints.py

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.services.openai_service import OpenAIService
# Replace AzureBlobService with LocalFileService
from app.services.local_file_service import LocalFileService
# from app.services.redis_cache import RedisCache
from app.utils import generate_cache_key
from fastapi import APIRouter

router = APIRouter()

@router.post("/process-image/")
async def process_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(None),
    blob_name: str = None,
    local_service: LocalFileService = Depends(),  # No need to pass 'connection_string' here
    openai_service: OpenAIService = Depends(OpenAIService),
):
    if file is None and blob_name is None:
        raise HTTPException(status_code=400, detail="Either 'file' or 'blob_name' must be provided.")
 
    if file:
        # Save the file locally
        file_content = await file.read()
        filename = file.filename
        local_service.save_file(file_content, filename)  # Save the file locally
        # Generate cache key using file_content
        cache_key = generate_cache_key(file_content)
    else:
        # Fetch the file locally
        file_content = local_service.fetch_file(blob_name)  # Fetch the file locally
        filename = blob_name
        # Generate cache key using blob_name
        cache_key = generate_cache_key(blob_name=blob_name)

    try:
        defect_response = await openai_service.call_model(file_content)
    except Exception as e:
        # Return an error response if the model call or parsing fails.
        return JSONResponse({"error": f"Failed to process image: {str(e)}"}, status_code=500)
    
    from fastapi.logger import logger as fastapi_logger
    fastapi_logger.info(f"Processed image '{filename}': {defect_response}")
    
    # Add caching logic here if needed
    return JSONResponse({"result": defect_response, "cached": False})
