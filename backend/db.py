from sqlalchemy import create_engine,inspect,text 

current_engine=None


def get_schema(db_url:str):

    global current_engine
    current_engine=create_engine(db_url)

    inspector=inspect(current_engine)

    schema={}

    for table in inspector.get_table_names():
        columns=inspector.get_columns(table)

        schema[table]=[
            {
                "name":col['name'],
                "type":str(col["type"])
            }
            for col in columns
        ]
    return {
        "connection_name": current_engine.url.database,
        "schema": schema
    }


def execute_sql(sql_query:str):
    global current_engine
    with current_engine.connect() as connection:
        result=connection.execute(text(sql_query))
        return [
            dict(row._mapping)
            for row in result
        ]

#db_url="postgresql://postgres:21wdspvabd@localhost:5432/sql_agent_demo"