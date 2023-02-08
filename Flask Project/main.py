from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Form, Response, Header, UploadFile, File
from flask import request, session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pandas as pd
import psycopg2
from pydantic import BaseSettings

db_table_list = []
dbtable = str()
db_dict = None
t = ''
global conn


# def table_head(conn, cursor):
#     result = pd.read_sql_query(f"select * from {t}", conn)
#     print(list(pd.DataFrame(result)))


def get_db_connection():
    global conn
    db_host = 'localhost'
    db_port = '5432'
    db_user = 'postgres'
    db_password = 'postgres'
    db_name = 'flask_db'
    conn = psycopg2.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=db_name)
    cursor = conn.cursor()
    # conn = psycopg2.connect(f'postgresql://postgres:postgres@localhost:5432/flask_db')
    return conn, cursor


class Userlogin(BaseModel):
    email: str
    password: str


class Table_data(BaseSettings):
    table_name: str


class User_signup(BaseModel):
    user_name: str
    email: str
    password: str


class Get_data_by_id(BaseModel):
    table_name: str
    id: str


app = FastAPI()


def select_query(table):
    # breakpoint()
    global dbtable
    dbtable = table
    conn, cursor = get_db_connection()
    result = pd.read_sql_query("select * from " + dbtable, conn)
    return result


#

# breakpoint()
# print(table_data)
# global dbtable
# conn, cursor = get_db_connection()
# result = pd.read_sql_query(f"select * from {dbtable}", conn)
# print(list(pd.DataFrame(result)))
# for i in list(pd.DataFrame(result)):
#     i: str
# def getTable(self):
#     conn, cursor = get_db_connection()
#     result = pd.read_sql_query(f"select * from {dbtable}", conn)
#     breakpoint()
#     print(list(pd.DataFrame(result)))
#     # return list(pd.DataFrame(result))
#     test_data: list(pd.DataFrame(result))


def get_query(conn):
    get_all_table()
    query = 'select * from platform_users'
    user_data = pd.read_sql_query(query, conn)
    return user_data


def get_all_table():
    global db_table_list
    conn, cursor = get_db_connection()
    cursor.execute("""SELECT relname FROM pg_class WHERE relkind='r'
                  AND relname !~ '^(pg_|sql_)';""")
    db_table_list = [i[0] for i in cursor.fetchall()]
    return db_table_list


# @app.get("/")
# async def data_get():
#     conn, cursor = get_db_connection()
#     query = 'select * from data_extractor_regex_rules'
#     user_data = pd.read_sql_query(query, conn)
#     file = pd.DataFrame(user_data).to_dict('records')
#     return file


@app.post('/login/')
async def login(user_login: Userlogin):
    user_data = dict(user_login)
    conn, cursor = get_db_connection()
    row = get_query(conn)
    if user_login:
        email = user_data.get('email')
        password = user_data.get('password')
        pd_instance = row[(row['email'] == email) & (row['password'] == password)]
        if not pd_instance.empty:
            if not pd_instance[(pd_instance['email'] == email) & (pd_instance['password'] == password)].empty:
                session["useremail"] = request.form.get("useremail")
                return "Logedin"


@app.post('/table_data/')
async def get_tabel_data(table: Table_data):
    json_compatible_item_data = jsonable_encoder(table)
    result = select_query(json_compatible_item_data['table_name'])
    table_data = pd.DataFrame(result).to_dict('records')
    return JSONResponse(content=table_data)


@app.post('/delete/')
async def delete_data(delete: Table_data):
    json_compatible_item_data = jsonable_encoder(delete)
    conn, cursor = get_db_connection()
    cursor.execute(
        f"select * from {json_compatible_item_data['table_name']} where id = {json_compatible_item_data['id']}")
    select_delete_data = cursor.fetchall()
    if isinstance(select_delete_data, list) and len(select_delete_data) > 0:
        cursor.execute(
            f"delete from {json_compatible_item_data['table_name']} where id = {json_compatible_item_data['id']}")
        conn.commit()
        return JSONResponse(content=select_delete_data)
    return JSONResponse(content={'msg': f"Data is Not Exists for this {json_compatible_item_data['id']} "})


def get_table_head(table):
    conn, cursor = get_db_connection()
    result = pd.read_sql_query(f"select * from {table}", conn)
    print(list(pd.DataFrame(result)))
    return list(pd.DataFrame(result))


# class Update_data(BaseModel):
#     global dbtable, db_dict, conn
#
#     class config:
#         db_dict = dict()
#         db_table_list = get_all_table()
#         count = 0
#         for dtable in db_table_list:
#             result = pd.read_sql_query(f"select * from {dtable}", conn)
#             all_table_instance = pd.DataFrame(result).to_dict('records')
#             db_dict[dtable] = all_table_instance
#             all_table_head = list(pd.DataFrame(result))
#             all_table_head[count]: str
#             count = - len(all_table_head)
#             pprint(all_table_head)
#             breakpoint()


@app.post('/data_by_id/')
async def get_table_data_by_id(data: Get_data_by_id):
    # breakpoint()
    global conn
    json_compatible_item_data = jsonable_encoder(data)
    global dbtable
    get_table_head(json_compatible_item_data['table_name'])
    dbtable = json_compatible_item_data['table_name']
    conn, cursor = get_db_connection()
    result = pd.read_sql_query(
        f"select * from {json_compatible_item_data['table_name']} where id = {json_compatible_item_data['id']}", conn)
    table_result = pd.DataFrame(result).to_dict('records')
    return JSONResponse(content=table_result)


#
# @app.put('/data_by_id/')
# async def edit_data(data: Update_data):
#     json_compatible_item_data = jsonable_encoder(data)
#     # breakpoint()
#     print(json_compatible_item_data)
#

@app.post('/signup/')
async def signup(data: User_signup):
    json_compatible_item_data = jsonable_encoder(data)
    # breakpoint()
    name = json_compatible_item_data.get('user_name')
    email = json_compatible_item_data.get('email')
    password = json_compatible_item_data.get('password')
    conn, cursor = get_db_connection()
    cursor.execute(
        f'INSERT INTO USERS (user_name, email, password)' 'VALUES (%s,%s,%s)',
        (name, email, password))
    conn.commit()
    return JSONResponse(content=json_compatible_item_data)


# @app.post("/cookie/")
# def create_cookie(response: Response):
#     response.set_cookie(key="fakesession", value="fake-cookie-session-value")
#     return {"message": "Come to the dark side, we have cookies"}

# @app.post("/cookie/")
# def create_cookie(response: Response):
#     content = {"message": "Come to the our web-side, we have cookies"}
#     response = JSONResponse(content=content)
#     # breakpoint()
#     response.set_cookie(key="fakesession", value="fake-cookie-session-value")
#     return response


# @app.post("/file_upload/")
# def create_cookie(file: UploadFile = File()):
#     # breakpoint()
#     converter = jsonable_encoder(file)
#     # breakpoint()
#     conn, cursor = get_db_connection()
#     if converter:
#         cursor.execute(
#             # f'INSERT INTO file(picture) VALUES("{converter["filename"]}")')
#             f'INSERT INTO file(image) VALUES (decode("{converter["filename"]}");')
#         conn.commit()
#     return JSONResponse(content={"file size ": len(converter)})


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
