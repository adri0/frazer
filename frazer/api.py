from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from frazer.analyser import analyse_sentence

app = FastAPI()


class InputPayload(BaseModel):
    sentence: str


class OutputPayload(BaseModel):
    analysis: str


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; customize for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/sentence", response_model=OutputPayload)
async def process_payload(payload: InputPayload):
    result = analyse_sentence(payload.sentence)
    response = OutputPayload(analysis=result)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("frazer.api:app", host="127.0.0.1", port=8011, reload=True)
