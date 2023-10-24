# Create hello world FastAPI app
from fastapi import FastAPI
from pydantic import BaseModel
from saiga__llm import get_model_response

app = FastAPI()

class Message(BaseModel):
    content: str


# @app.post("/items/")
# async def create_item(user_message: Message):
#     response = {"content": user_message}
#     return response


@app.post("/")
async def saiga_answer(user_message: Message):
    saiga_response = get_model_response("Привет")
    response =  f'Ответ модели: {saiga_response}'
    return response