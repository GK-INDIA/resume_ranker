import ast
import io
import json
import os
from typing import List

import pandas as pd
import PyPDF2
from docx import Document
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

from utils.openai_function import get_completion

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class ExtractCriteriaResponse(BaseModel):
    criteria: List[str]


class ScoreResumesResponse(BaseModel):
    message: str = "File generated successfully"
    download_link: str


# Helper Functions
async def extract_text(file: UploadFile):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.filename.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    else:
        raise ValueError("Unsupported file type")


async def get_criteria_from_text(text: str):
    try:
        prompt = f"""
        You are the best Job Description analyser. Analyse the Job description given as input text in triple backticks:
        Input text: ```{text}```\n
        and list down key selection criteria for section of candidates for the job according to the description in simple english as bullet points.

        Output format: Output a json object with key "Critera":
        Critera: (list type output)[ <criteria 1>, <criteria 2>, <criteria 3>...<criteria n>]

        Note: Output the criteria in crisp and precise; like skills, certifications, experience, and qualifications etc.
        Note: Output all the criteria of selection with repective condition as list of criteria under the key "Criteria". Incase none of the criteria is present output "Not Mentioned"
        """
        result = get_completion(prompt)
        data = ast.literal_eval(result)
        return data.get("Criteria", [])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing criteria: {str(e)}"
        )


# Endpoints
@app.post(
    "/extract-criteria",
    response_model=ExtractCriteriaResponse,
    summary="Extract ranking criteria from job description",
    description="Extracts key criteria like skills, certifications, and experience from a job description file (PDF/DOCX).",
)
async def extract_criteria(file: UploadFile = File(...)):
    try:
        text = await extract_text(file)
        criteria = await get_criteria_from_text(text)
        return JSONResponse(content={"criteria": criteria})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Task 2 Implementation
async def score_resume(resume_text: str, criteria: List[str]):
    try:
        n = len(criteria)
        prompt = f"""
        You are the best resume scoring machine. Given the list of criteria in triple backtick: critera = ```{criteria}```
        and a resume of candidate who applied in triple arrows: resume = <<<{resume_text}>>>\n
        Anlyse the resume based on the marking critera given as list of criterias by scoring the person whose resume has been given as input for each critera mentioned in a range of 0-5

        Output format: Output a json object with 2 keys: 'name', 'scores':
        name: (string type output) <Mention the name of the person whose resume is being analysed and given as input>
        scores: (list type output)<mention {n} number of scores against each critera (in 0-5); as mentioned in list of critera for the candidate>
        """
        result = get_completion(prompt)
        data = ast.literal_eval(result)
        return {
            "name": data.get("name", "Unknown"),
            "scores": data.get("scores", {c: 0 for c in criteria}),
        }
    except Exception as e:
        return {"name": "Unknown", "scores": {c: 0 for c in criteria}}


@app.post(
    "/score-resumes",
    summary="Score resumes against criteria",
    description="Scores multiple resumes based on provided criteria and returns an Excel file.",
)
async def score_resumes(
    criteria: str = Form(...),
    files: List[UploadFile] = File(...),
):
    try:
        criteria_list = ast.literal_eval(criteria)
        if not isinstance(criteria_list, list):
            raise HTTPException(status_code=400, detail="Criteria must be a list")

        rows = []
        for file in files:
            text = await extract_text(file)
            result = await score_resume(text, criteria_list)
            row = {"Candidate Name": result["name"]}

            # Ensure scores are mapped correctly
            for idx, criterion in enumerate(criteria_list):
                row[criterion] = (
                    result["scores"][idx] if idx < len(result["scores"]) else 0
                )

            row["Total Score"] = sum(row[criterion] for criterion in criteria_list)
            rows.append(row)

        df = pd.DataFrame(rows)
        columns = ["Candidate Name"] + criteria_list + ["Total Score"]
        df = df[columns]

        # Save Excel file in-memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Return file directly as response
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=scores.xlsx"},
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid criteria format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
