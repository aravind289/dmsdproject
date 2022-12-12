import pymysql
from flask import Flask, render_template, request,redirect
 



connection = pymysql.connect(host="127.0.0.1",port=3306,user="root", password="Test123%%", database="libdata")
print("Database connected...")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/reader_login')
def reader_login():
    return render_template('reader_login.html')


@app.route('/reader_login_auth',methods=['GET'])
def reader_login_auth():
    id = request.args.get('Id')
    name = request.args.get('Name')
    try:
        command = f"SELECT EXISTS(SELECT * from READER where RID={id})"
        connection.ping()
        check_data = connection.cursor()
        check_data.execute(command)
        output = check_data.fetchall()
        for i in output:
            print(i)
    except Exception as e:
        print(e)
        return render_template('reader_login.html', result="reader details not present")
    
    return render_template('reader_menu.html',result = id)


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login_auth')
def admin_login_auth():
    return render_template('admin_menu.html')


@app.route('/reader_menu',methods=['POST','GET'])
def menu_page():
    id=int(request.args.get('Id'))
    name = request.args.get('Name')
    personType= request.args.get('Person_type')
    id_lhs = "RID" if personType == "READER" else "ADID"
    print("id is",id)
    print("name is",name)
    # check for card number  -reader
    # check for id and pwd  - admin
    try:
        command = f"SELECT EXISTS(SELECT * from {personType} where {id_lhs}={id})"
        connection.ping()
        check_data = connection.cursor()
        check_data.execute(command)
        output = check_data.fetchall()
        for i in output:
            print(i)
            if personType=="READER" and i[0] ==1:
                return render_template('reader_menu.html')
            elif personType == "ADMIN" and i[0] == 1:
                return render_template('admin_menu.html')

        connection.commit()
        
    except Exception as e:
        print(e)
        return render_template('index.html', result="Library staff SSN/Member SSN is wrong")






# @app.route('/menu',methods=['POST','GET'])
# def menu_page():
#     id=int(request.args.get('Id'))
#     name = request.args.get('Name')
#     personType= request.args.get('Person_type')
#     id_lhs = "RID" if personType == "READER" else "ADID"
#     print("id is",id)
#     print("name is",name)
#     # check for card number  -reader
#     # check for id and pwd  - admin
#     try:
#         command = f"SELECT EXISTS(SELECT * from {personType} where {id_lhs}={id})"
#         connection.ping()
#         check_data = connection.cursor()
#         check_data.execute(command)
#         output = check_data.fetchall()
#         for i in output:
#             print(i)
#             if personType=="READER" and i[0] ==1:
#                 return render_template('reader_menu.html')
#             elif personType == "ADMIN" and i[0] == 1:
#                 return render_template('admin_menu.html')

#         connection.commit()
        
#     except Exception as e:
#         print(e)
#         return render_template('index.html', result="Library staff SSN/Member SSN is wrong")


@app.route('/document_search',methods=['POST','GET'])   
def search_book():
    id=request.args.get('DocId')
    name = request.args.get('Title')
    publisher_name= request.args.get('PublisherName')
    try:
        if id != "":
            id=int(id)
            retrieve_doc_by_id = f"SELECT * FROM DOCUMENT WHERE DOCID = {id}"
            connection.ping()
            doc_cur = connection.cursor()
            doc_cur.execute(retrieve_doc_by_id)
            output = doc_cur.fetchall()
            return render_template("reader_menu.html",result = output)
        elif name != "":
            retrieve_doc_by_title = f"SELECT * FROM DOCUMENT WHERE TITLE = {name}"
            connection.ping()
            doc_cur = connection.cursor()
            doc_cur.execute(retrieve_doc_by_title)
            output = doc_cur.fetchall()
            return render_template("reader_menu.html",result = output)
        elif publisher_name != "":
            retrieve_doc_by_publisher_name = f"Select * from DOCUMENT D JOIN PUBLISHER P ON D.PUBLISHERID = P.PUBLISHERID WHERE P.PUBNAME = {publisher_name}"
            connection.ping()
            doc_cur = connection.cursor()
            doc_cur.execute(retrieve_doc_by_publisher_name)
            output = doc_cur.fetchall()
            return render_template("reader_menu.html",result = output)
        
            
    except Exception as e:
        print("error message is ",e)







connection.commit()
connection.close()


if __name__ == '__main__':
    app.run()



# print(connection)

# retrieve = "Select * from PERSON;"

# cursor.execute(retrieve)
# rows = cursor.fetchall()

# for item in rows:
#     print(type(item))
#     print("item is",item)


