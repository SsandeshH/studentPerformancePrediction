from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():   #async makes root() a coroutine, which can we stopped and presumed, dont wait for one task to complete
    return {"Welcome to Student Performance Prediction App"}



