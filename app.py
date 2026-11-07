"""
FastAPI Application
LLM Guardrails Workshop
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from guardrails import check_input
from output_guardrails import check_output
from gemini_service import generate_response

#FASTAPI Application

app = FastAPI(
    title="LLM Guardrails Workshop",
    description=(
        "Gemini + FastAPI +"
        "Input and Output Guardrails"
    ),
    version="1.0.0",
)

# Static files

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# Templates
templates = Jinja2Templates(
    directory="templates"
)

# Request Model

class PromptRequest(BaseModel):
    prompt: str

# Home Page

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="Index.html",
        context={}
    )

# Health Check

@app.get("/Health")
async def health():
    return{
        "status": "healthy",
        "Application": "LLM Guardrails Workshop"
    }

# Generate
@app.post("/generate")
async def generate(request: PromptRequest):
    user_input = request.prompt

# INPUT Guardrails
    input_result = check_output(
        user_input
    )
    #Block unsafe input
    if not input_result["allowed"]:
        return {
            "status" : "blocked",
            "stage" : "input_guardrails",
            "category" : input_result["category"],
            "message" : input_result["message"],
            "response": None
        }

    # GEMINI
    model_response = generate_response(
        user_input
    )

# OUTPUT Guardrails
    output_result = check_output(
        model_response
    )

# Block UNSAFE OUTPUT
    if not output_result["allowed"]:
        return {
            "status" : "blocked",
            "stage" : "output_guardrails",
            "category" : output_result["category"],
            "message" : output_result["message"],
            "response": None
        }

# SUCCESS
    return{
        "status" : "success",
        "stage" : "completed",
        "category" : "SAFE",
        "message" : (
            "Response generated successfully."
        ),
        "response": model_response
    }
