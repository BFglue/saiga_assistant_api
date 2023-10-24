# Create hello world FastAPI app
from fastapi import FastAPI
from pydantic import BaseModel
import saiga_script

app = FastAPI()

class Message(BaseModel):
    content: str


@app.post("/")
async def saiga_answer(user_message: Message):
    saiga_response = saiga_script.main(user_message.content)
    return saiga_response