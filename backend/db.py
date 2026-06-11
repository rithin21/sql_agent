from sqlalchemy import create_engine,inspect

def get_schema(db_url:str):
    engine=create_engine(db_url)

    inspector=inspect(engine)

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
    return schema

#db_url="postgresql://postgres:21wdspvabd@localhost:5432/sql_agent_demo"