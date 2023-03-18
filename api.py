from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from table_manager import write_csv, read_csv, get_games, check_lock


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataModel(BaseModel):
    data: Dict[str, Dict[str, int]]
    folder: str


@app.post("/write")
async def write_data(data_model: DataModel):
    write_csv(data_model.data, data_model.folder)
    return {"message": "Data written successfully"}


@app.get("/read/{folder}")
async def read_data(folder: str):
    data = read_csv(folder)
    if data is None:
        return {"message": "No matching files found."}
    return data


@app.get("/folders")
async def list_folders():
    folders = get_games()
    return {"folders": folders}


@app.get("/lock/{folder}")
async def is_locked(folder: str):
    if folder == "undefined":
        return {"message": "Folder is not defined"}
    locked = check_lock(folder)
    return {"locked": locked}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
