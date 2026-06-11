from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import get_schema,execute_sql
from fastapi.middleware.cors import CORSMiddleware
from ollama import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

currentschema=None

class query(BaseModel):
    connectionString: str

class userprompt(BaseModel):
    prompt: str
    connectionString: str

@app.post('/')
def getsqlschema(connection:query):
    try:
        result=get_schema(connection.connectionString)

        global currentschema
        currentschema = result["schema"]

        return {
            "connection_name":result["connection_name"],
            "status":"success",
            "schema":result["schema"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )

def formulate_prompt(userprompt:str,schema:dict):
    schema_text=""
    for table,columns in schema.items():
        schema_text+=f"Table:{table}\n"
        for col in columns:
            schema_text+=f"-{col['name']}:{col['type']}\n"
    
    final_prompt=f"Given the following database schema:\n{schema_text}\nGenerate an SQL query for the following request:\n{userprompt}"
    return final_prompt

system_prompt='''
You are an expert PostgreSQL developer.

Use ONLY columns that exist in the schema.

Before generating SQL:
1. Verify every referenced column exists.
2. Verify every table exists.
3. Use fully qualified column names when joining tables.

Return SQL only.
No markdown.
No explanations.'''

def generate_sql(formulatedprompt:str):
    response=chat(
        model='llama3.2:1b',
        messages=[
            {'role':'system',
             'content':system_prompt},
            {'role':'user',
             'content':formulatedprompt}
        ]
    )
    sql=response['message']['content']
    sql=sql.replace("```sql","")
    sql=sql.replace("```","")
    sql=sql.strip()
    return sql


@app.post('/run_query/')
def run_query(combinedprompt: userprompt):
    result=get_schema(combinedprompt.connectionString)#how do i get the db_url here?
    schema=result["schema"]
    final_prompt=formulate_prompt(combinedprompt.prompt,schema)#this fn shud convert my json schema to str and attach the actual prompt the user gave
    sql_query=generate_sql(final_prompt)
    queryresult=execute_sql(sql_query)
    return {
        "sql_query":sql_query,
        "query_result":queryresult
    }