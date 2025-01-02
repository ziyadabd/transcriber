from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os


app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Request model
class TranscriptionRequest(BaseModel):
    link: str

@app.post("/transcribe")
async def transcribe(data: TranscriptionRequest):
    input_link = data.link

    if not input_link:
        raise HTTPException(status_code=400, detail="No link provided")

    try:
        # Run the transcribe-anything library
        subprocess.run(["transcribe-anything", input_link], check=True)
        
        # Specify the directory and file path (update if necessary)
        output_path = "output_directory/out.txt"
        if not os.path.exists(output_path):
            raise FileNotFoundError("out.txt not found. Check if the process completed successfully.")

        # Read the contents of out.txt
        with open(output_path, "r") as file:
            result = file.read()

        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
