from flask import Flask, render_template, redirect, request, session, url_for, make_response
from flask_session import Session
import crypt
from hmac import compare_digest as compare_hash
import hashlib

import pandas as pd
import psycopg2

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='template')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_table_list = []
gtable = str()


def get_db_connection():
    db_host = 'localhost'
    db_port = '5432'
    db_user = 'postgres'
    db_password = 'postgres'
    db_name = 'flask_db'
    conn = psycopg2.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=db_name)
    cursor = conn.cursor()
    # conn = psycopg2.connect(f'postgresql://postgres:postgres@localhost:5432/flask_db')
    return conn, cursor


def select_query(table):
    # breakpoint()
    global gtable
    gtable = table
    conn, cursor = get_db_connection()
    result = pd.read_sql_query("select * from " + gtable, conn)
    return result


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


@app.route('/home')
def home():
    global db_table_list, gtable
    db_table_list = get_all_table()
    username = session.get("useremail")
    return render_template('index.html', db_table_list=db_table_list, username=username, gtable=gtable)


@app.route('/home/<table_data>')
def show_home(table_data):
    global db_table_list, gtable
    db_table_list = get_all_table()
    return render_template('index.html', db_table_list=db_table_list, table_data_dict=table_data, gtable=gtable)


# @app.route('/home/<table_data>')
# def home(table_data):
#     # breakpoint()
#     if request.cookies.get('useremail'):
#         return render_template('index.html', db_table_list=db_table_list,
#                                username=session.get("useremail"), table_data=table_data)
#     return render_template('login_page.html', msg="Wrong username or password.")


# @app.route('/show/<table_data>')
# def show_table(table_data):
#     # if session.get("useremail"):
#     # table_data = select_query()
#     return render_template('index.html', db_table_list=db_table_list, user_data=table_data,
#                            username=session.get("useremail"))


# show login page
@app.route('/')
def login_page():
    get_db_connection()
    return render_template('login_page.html')


@app.route('/signup_page', methods=['GET'])
def signup_page():
    if request.method == "GET":
        return render_template('signup.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['userpassword']
        email = request.form['useremail']
        conn, cursor = get_db_connection()
        cursor.execute('INSERT INTO users (user_name, email, password)' 'VALUES (%s,%s,%s)', (name, email, password))
        conn.commit()
        return redirect('/')


@app.route('/logout')
def logout():
    # breakpoint()
    session.pop('useremail', None)
    return redirect('/')


@app.route('/get_data/<string:table>', methods=['POST', 'GET'])
def get_data(table):
    # breakpoint()
    global db_table_list, gtable
    result = select_query(table)
    table_data = pd.DataFrame(result).to_dict('records')
    table_head_data = table_heading()
    return render_template('index.html', db_table_list=db_table_list,
                           username=session.get("useremail"), table_head_data=table_head_data
                           , table_data_dict=table_data, gtable=gtable)


@app.route('/login', methods=['POST', 'GET'])
def login():
    conn, cursor = get_db_connection()
    row = get_query(conn)
    # breakpoint()
    # password = request.form['userpassword']
    # ps = pd.DataFrame(row['password']).to_dict('records')
    # hashed = ps[0]['password']['hashedpassword']
    # value = compare_hash(hashed, crypt.crypt(password, hashed))
    # print(value)
    # {"salt": "a3b2e",
    #  "hashedpassword": "7102d3f9332700a02df5d50d69e1315f990a11a3aa2f43e29309c8f33074668a012b674bccd07537dd8207fb4120d26f443a81d3c6680de4ae6c5e351545470f"}
    if request.method == 'POST':
        email = request.form['useremail']
        password = request.form['userpassword']
        pd_instance = row[(row['email'] == email) & (row['password'] == password)]
        if not pd_instance.empty:
            if not pd_instance[(pd_instance['email'] == email) & (pd_instance['password'] == password)].empty:
                # resp = make_response(redirect("/home"))
                # resp.set_cookie('useremail', email)
                # session["useremail"] = request.form.get("useremail")
                # return resp
                # print(resp)
                # breakpoint()
                session["useremail"] = request.form.get("useremail")
                return redirect("/home")
    return redirect('/')


@app.route('/show_records', methods=["POST", "GET"])
def show_records():
    global db_table_list, gtable
    table_head_data = table_heading()
    result = select_query(gtable)
    table_data = pd.DataFrame(result).to_dict('records')
    username = session.get("useremail")
    return render_template('index.html', db_table_list=db_table_list, table_data_dict=table_data, username=username,
                           table_head_data=table_head_data, gtable=gtable)


@app.route('/delete/<string:deleteid>', methods=["POST", "GET"])
def delete(deleteid):
    global db_table_list, gtable
    select_query(gtable)
    print(gtable, deleteid)
    db_table_list = get_all_table()
    conn, cursor = get_db_connection()
    cursor.execute(f"delete from {gtable} where id = {deleteid}")
    conn.commit()
    return redirect(url_for('show_records'))


@app.route('/edit/<string:editid>', methods=["POST", "GET"])
def edit(editid):
    global gtable
    # breakpoint()
    conn, cursor = get_db_connection()
    result = pd.read_sql_query(f"select * from  {gtable} where id = {editid}", conn)
    table_data = pd.DataFrame(result).to_dict('records')
    return render_template('update_form.html', editData=table_data[0])


@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    global gtable
    conn, cursor = get_db_connection()
    if request.method == "POST":
        name = request.form.get('updatename')
        email = request.form.get('updateemail')
        password = request.form.get('updatepassword')
        cursor.execute(
            f"UPDATE {gtable} SET user_name = '{name}', email = '{email}', password = '{password}' where id = {id}")
        conn.commit()
        return redirect(url_for('show_records'))


@app.route('/insert', methods=["POST"])
def add():
    conn, cursor = get_db_connection()
    if request.method == "POST":
        # breakpoint()
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute('INSERT INTO users (user_name, email, password)' 'VALUES (%s,%s,%s)', (name, email, password))
        conn.commit()
        return redirect(url_for('show_records'))


def table_heading():
    global gtable
    conn, cursor = get_db_connection()
    result = pd.read_sql_query(f"select * from {gtable}", conn)
    return list(pd.DataFrame(result))


app.run(debug=True)
