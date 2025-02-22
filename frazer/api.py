import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from frazer.analyser import Sentence, analyse_sentence

logger = logging.getLogger(__name__)
app = FastAPI()


class InputPayload(BaseModel):
    sentence: str


class OutputPayload(BaseModel):
    sentence: Sentence


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
    logger.info(f"Incoming sentence: {payload.sentence}")
    sentence = analyse_sentence(payload.sentence)
    response = OutputPayload(sentence=sentence)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("frazer.api:app", host="127.0.0.1", port=8011, reload=True)
