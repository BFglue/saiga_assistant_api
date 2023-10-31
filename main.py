from fastapi import FastAPI
from pydantic import BaseModel
import saiga_script

"""
data = {
    "prompt": "промпт который будет передан в system",
    "user": "вопрос пользователя"
}
"""

app = FastAPI()

class APIRequest(BaseModel):
    prompt: str
    user: str


@app.post("/saigav1/completions")
async def saiga_answer(api_request: APIRequest):
    saiga_response = saiga_script.main(api_request.user, api_request.prompt)
    return saiga_response

# @app.get("/saigav1/completions")
# def read_root():
#    return {"message": "It works!"}
