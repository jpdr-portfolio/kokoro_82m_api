import json
import os
import soundfile as sf
import torch
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from kokoro import KPipeline
from IPython.display import display, Audio
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime


class AppRequest(BaseModel):
	text: str

class AppResponse(BaseModel):
	message: str

PORT = 3090
pipeline = KPipeline(lang_code='e')

app = FastAPI()

# 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
# 🇪🇸 'e' => Spanish es
# 🇫🇷 'f' => French fr-fr
# 🇮🇳 'h' => Hindi hi
# 🇮🇹 'i' => Italian it
# 🇯🇵 'j' => Japanese: pip install misaki[ja]
# 🇧🇷 'p' => Brazilian Portuguese pt-br
# 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]


@app.post("/audio")
def audio(body: AppRequest):
    try:
        text = body.text
        generator = pipeline(text, voice='af_heart')
        for i, (gs, ps, audio) in enumerate(generator):
            print(i, gs, ps)
            display(Audio(data=audio, rate=24000, autoplay=i==0))
            sf.write(f'output.wav', audio, 24000)
            return FileResponse(path='output.wav', filename='output.wav', media_type='audio/wav')
    except Exception as e:
        print(f'Error procesing audio file')
        return {"message":str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
