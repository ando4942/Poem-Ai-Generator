from fastapi import FastAPI, HTTPException
from poem_ai import gen_poem, MAX_CHAR_LEN
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get("/generate_poem")
async def root(prompt: str):
    validate_len(prompt)
    poem = gen_poem(prompt)
    return {"message": f"{poem}"}

def validate_len(user_input):
    if len(user_input) >= MAX_CHAR_LEN:
        raise HTTPException(status_code=400, detail=f"Input length too long. Must be under {MAX_CHAR_LEN} characters")
    