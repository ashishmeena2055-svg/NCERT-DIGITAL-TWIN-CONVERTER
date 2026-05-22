from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from pdf_engine import process_full_pdf

app = FastAPI(title="NEET PDF Translator Backend")

# CORS पॉलिसी चालू ताकि फ्रंटएंड बिना किसी ब्लॉक के जुड़ सके
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend Server is running flawlessly!"}

@app.post("/api/v1/translate")
async def translate_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        pdf_content = await file.read()
        translated_pdf_bytes = await process_full_pdf(pdf_content)
        
        return StreamingResponse(
            io.BytesIO(translated_pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=translated_{file.filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
