from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from chat_pipline import Chat
from pydantic import BaseModel, Field

app = FastAPI()
chat_instance = Chat()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, you can use ["*"] or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str = Field(..., min_length=5)
    threadId: str = Field(..., min_length=1)
    isStream: bool = Field(default=False)


@app.post("/chat")
async def chat_endpoint(request: Message):
    if request.isStream:
        return StreamingResponse(
            chat_instance.stream_message(request.message, request.threadId),
            media_type="text/plain",
        )
    else:
        response = chat_instance.send_message(request.message, request.threadId)
        reply = response["messages"][-1].content
        return {"message": reply}
