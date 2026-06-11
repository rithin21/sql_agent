from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import get_schema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class query(BaseModel):
    connectionString: str

@app.post('/')
def getsqlschema(connection:query):
    try:
        schema=get_schema(connection.connectionString)

        return {
            "status":"success",
            "schema":schema
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
