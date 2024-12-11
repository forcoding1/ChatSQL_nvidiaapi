import os
import json
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from db_connector import *
import pandas as pd

def load_credentials(file_path):
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        os.environ["NVIDIA_API_KEY"] = data["NVIDIA_API_KEY"]
    except Exception as e:
        print(f"Error loading credentials: {e}")
        raise


def generate_chain(model_name, sys_prompt, max_tokens=1000, temperature=0.7):
    
    try:
        llm = ChatNVIDIA(model=model_name, max_tokens=max_tokens, temperature=temperature)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", sys_prompt),
                ("user", "{input}")
            ]
        )
        chain = prompt_template | llm | StrOutputParser()
        return chain
    except Exception as e:
        print(f"Error in generating chain: {e}")
        return None

def execute_sql_chain(chain, db_obj, schema, query):
    try:
        if not chain:
            raise ValueError("Chain is not initialized.")
        
        formatted_query = f"Here is the schema: {schema}\n\n{query}"
        result = chain.invoke({"input": formatted_query})
        print("Generated Query:", result)
        
        sql_outputs = execute_query(db_obj, result.strip())
        
        if sql_outputs:
            dataframes = [
                pd.DataFrame(table_result) for table_result in sql_outputs
            ]
            return dataframes
        return sql_outputs
    except Exception as e:
        print(f"Error executing SQL chain: {e}")
        return None


    
# load_credentials("nemotron/creds.json")
# model_name = "meta/llama-3.1-8b-instruct"
# sql_sys_prompt = "You are an expert coding AI. Respond only in valid MySQL statements; no narration whatsoever."
# db_obj = create_database(db_name="chatsql", host="localhost", user = "root", password = "root")
# schema = get_database_schema_wrapper(db_obj, "chatsql")
# query = "get names of users of instagram"
# chain = generate_chain(model_name, sql_sys_prompt)
# print(execute_sql_chain(chain, db_obj, schema, query))

# if __name__ == "__main__":
#     main()
