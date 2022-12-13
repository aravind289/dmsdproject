import pymysql
from flask import Flask, render_template, request,session

from flask_session import Session
 

# connection = pymysql.connect(host="mysql01.arcs.njit.edu",port=3306,user="ak2855", password="Sampletest123%%", database="ak2855")

connection = pymysql.connect(host="127.0.0.1",port=3306,user="root", password="Test123%%", database="libdata")
print("Database connected...")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


reader_id = 0

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/reader_login')
def reader_login():
    return render_template('reader_login.html')


@app.route('/reader_login_auth',methods=['GET'])
def reader_login_auth():
    global reader_id
    reader_id = int(request.args.get('Id'))
    session["reader_id"] = reader_id
    try:
        command = f"SELECT EXISTS(SELECT * from READER where RID={reader_id})"
        connection.ping()
        check_data = connection.cursor()
        check_data.execute(command)
        output = check_data.fetchall()
        if output[0][0] ==1:
            return render_template('reader_menu.html', reader_id = reader_id)
        else:
            return render_template('reader_login.html', result="reader details not present")

    except Exception as e:
        print(e)
        return render_template('reader_login.html', result="reader details not present")
    
    

# NOTE: ADD HTML RENDERING!
@app.route('/admin/login',methods=["POST"])
def admin_login():
    id = request.json.get('Id')
    name = request.json.get('Name')
    password =request.json.get("Password")
    try:
        command = f'SELECT EXISTS(SELECT * from ADMIN where ADMINID={id} AND ADMIN_NAME="{name}" AND ADMIN_PWD="{password}")'
        connection.ping()
        check_data = connection.cursor()
        check_data.execute(command)
        doesExists = bool(check_data.fetchall()[0][0])
        if not doesExists:
            return "User doesn't exists!"
        else:
            return "Valid User!"
    except Exception as e:
        print("ERROR!!!",e)
        return "Server Error",500

@app.route('/admin_login_auth',methods=['GET'])
def admin_login_auth():
    id = int(request.args.get('Id'))
    pwd = request.args.get('Pwd')
    try:
        command = f"SELECT EXISTS(SELECT * from ADMIN WHERE ADMINID={id} AND ADMIN_PWD = '{pwd}');"
        connection.ping()
        check_data = connection.cursor()
        check_data.execute(command)
        output = check_data.fetchall()
        print(output)
        if output[0][0] ==1:
            return render_template('admin_menu.html',result = id)
        else:
            return render_template('admin_login.html', result="Admin details not present")

    except Exception as e:
        print(e)
        return render_template('admin_login.html', result="Admin details not present")


@app.route('/reader_menu',methods=['GET'])
def menu_page():
    searchType = request.args.get('search_type')
    searchTypeVal = request.args.get('SearchType')
    print("search type",searchType)
    print("search type value is ",searchTypeVal)
    connection.ping()
    try:
        if searchType == 'Id':
            searchval=int(searchTypeVal)
            retrieve_doc_by_id = f"Select D.DOCID,D.TITLE, P.PUBNAME from DOCUMENT D JOIN PUBLISHER P ON D.PUBLISHERID = P.PUBLISHERID WHERE D.DOCID={searchval}"
            doc_cur = connection.cursor()
            doc_cur.execute(retrieve_doc_by_id)
            output = doc_cur.fetchall()
            for i in output:
                print(i)
            return render_template("reader_menu.html",result = output)
        elif searchType == 'Title':
            retrieve_doc_by_title = f"Select D.DOCID,D.TITLE, P.PUBNAME from DOCUMENT D JOIN PUBLISHER P ON D.PUBLISHERID = P.PUBLISHERID WHERE D.TITLE = '{searchTypeVal.capitalize()}'"
            doc_cur = connection.cursor()
            doc_cur.execute(retrieve_doc_by_title)
            output = doc_cur.fetchall()
            for i in output:
                print(i)
            return render_template("reader_menu.html",result = output)
        else:
            retrieve_doc_by_publisher_name = f"Select D.DOCID,D.TITLE, P.PUBNAME from DOCUMENT D JOIN PUBLISHER P ON D.PUBLISHERID = P.PUBLISHERID WHERE P.PUBNAME = '{searchTypeVal.capitalize()}'"
            doc_cur = connection.cursor()
            doc_cur.execute(retrieve_doc_by_publisher_name)
            output = doc_cur.fetchall()
            for i in output:
                print(i)
            return render_template("reader_menu.html",result = output)
    except Exception as e:
        print("error message is ",e)


@app.route('/borrowPage/<docId>')
def borrow_page(docId):
    global reader_id
    doc_id = docId
    # try:

    return render_template('addbook.html')


@app.route('/reservePage/<docId>')
def reserve_page():
    return render_template('borrowBook.html')



    # check for card number  -reader
    # check for id and pwd  - admin
    # try:
    #     command = f"SELECT EXISTS(SELECT * from {personType} where {id_lhs}={id})"
    #     connection.ping()
    #     check_data = connection.cursor()
    #     check_data.execute(command)
    #     output = check_data.fetchall()
    #     for i in output:
    #         print(i)
    #         if personType=="READER" and i[0] ==1:
    #             return render_template('reader_menu.html')
    #         elif personType == "ADMIN" and i[0] == 1:
    #             return render_template('admin_menu.html')

    #     connection.commit()
        
    # except Exception as e:
    #     print(e)
    #     return render_template('index.html', result="Library staff SSN/Member SSN is wrong")






# # @app.route('/menu',methods=['POST','GET'])
# # def menu_page():
# #     id=int(request.args.get('Id'))
# #     name = request.args.get('Name')
# #     personType= request.args.get('Person_type')
# #     id_lhs = "RID" if personType == "READER" else "ADID"
# #     print("id is",id)
# #     print("name is",name)
# #     # check for card number  -reader
# #     # check for id and pwd  - admin
# #     try:
# #         command = f"SELECT EXISTS(SELECT * from {personType} where {id_lhs}={id})"
# #         connection.ping()
# #         check_data = connection.cursor()
# #         check_data.execute(command)
# #         output = check_data.fetchall()
# #         for i in output:
# #             print(i)
# #             if personType=="READER" and i[0] ==1:
# #                 return render_template('reader_menu.html')
# #             elif personType == "ADMIN" and i[0] == 1:
# #                 return render_template('admin_menu.html')

# #         connection.commit()
        
# #     except Exception as e:
# #         print(e)
# #         return render_template('index.html', result="Library staff SSN/Member SSN is wrong")


# @app.route('/document_search',methods=['POST','GET'])   
# def search_book():
#     id=request.args.get('DocId')
#     name = request.args.get('Title')
#     publisher_name= request.args.get('PublisherName')
#     try:
#         if id != "":
#             id=int(id)
#             retrieve_doc_by_id = f"SELECT * FROM DOCUMENT WHERE DOCID = {id}"
#             connection.ping()
#             doc_cur = connection.cursor()
#             doc_cur.execute(retrieve_doc_by_id)
#             output = doc_cur.fetchall()
#             return render_template("reader_menu.html",result = output)
#         elif name != "":
#             retrieve_doc_by_title = f"SELECT * FROM DOCUMENT WHERE TITLE = {name}"
#             connection.ping()
#             doc_cur = connection.cursor()
#             doc_cur.execute(retrieve_doc_by_title)
#             output = doc_cur.fetchall()
#             return render_template("reader_menu.html",result = output)
#         elif publisher_name != "":
#             retrieve_doc_by_publisher_name = f"Select * from DOCUMENT D JOIN PUBLISHER P ON D.PUBLISHERID = P.PUBLISHERID WHERE P.PUBNAME = {publisher_name}"
#             connection.ping()
#             doc_cur = connection.cursor()
#             doc_cur.execute(retrieve_doc_by_publisher_name)
#             output = doc_cur.fetchall()
#             return render_template("reader_menu.html",result = output)
        
            
#     except Exception as e:
#         print("error message is ",e)







connection.commit()
connection.close()


if __name__ == '__main__':
    app.run(port=8888)



# print(connection)

# retrieve = "Select * from PERSON;"

# cursor.execute(retrieve)
# rows = cursor.fetchall()

# for item in rows:
#     print(type(item))
#     print("item is",item)


