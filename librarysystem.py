import pymysql
from flask import Flask, render_template, request,session

from flask_session import Session
# from datetime import timedelta
from datetime import datetime
 

# connection = pymysql.connect(host="mysql01.arcs.njit.edu",port=3306,user="ak2855", password="Sampletest123%%", database="ak2855")

connection = pymysql.connect(host="127.0.0.1",port=3306,user="root", password="Test123%%", database="libdata")
print("Database connected...")
connection.query('SET GLOBAL connect_timeout=6000')
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
        books_borrowed = f"SELECT  D.DOCID,D.TITLE,B.BID,B.COPYNO FROM DOCUMENT D JOIN BORROWS B ON B.DOCID = D.DOCID JOIN BORROWING BW ON BW.BOR_NO = B.BOR_NO WHERE B.RID={reader_id} AND BW.RETURN_STATUS = 'N';"
        boo_bor = connection.cursor()
        boo_bor.execute(books_borrowed)
        books_result = boo_bor.fetchall()
        fineCalulate = f"Select SUM(fine) as sum_fine from (select DATEDIFF(bg.rdtime, bg.bdtime) as borr_days, DATEDIFF(bg.rdtime, bg.bdtime) * 0.20 as fine from BORROWING bg inner join BORROWS bs on bs.bor_no = bg.bor_no  where DATEDIFF(bg.rdtime, bg.bdtime) > 20 AND bg.RETURN_STATUS='Y' AND bs.RID={reader_id} ) as penalties ;"
        fineConn = connection.cursor()
        fineConn.execute(fineCalulate)
        outputCheck = fineConn.fetchall()

        if output[0][0] ==1:
            return render_template('reader_menu.html', reader_id = reader_id,books_result=books_result, fineAmount = outputCheck)
        else:
            return render_template('reader_login.html', result="reader details not present")

    except Exception as e:
        print(e)
        return render_template('reader_login.html', result="reader details not present")
    
    


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

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
        branchInfo = f"SELECT * FROM BRANCH"
        branchData = connection.cursor()
        branchData.execute(branchInfo)
        finalOutput = branchData.fetchall()
        print("branch details",finalOutput)

        if output[0][0] ==1:
            return render_template('admin_menu.html',result = id,finalOutput = finalOutput)
        else:
            return render_template('admin_login.html', result="Admin details not present")

    except Exception as e:
        print(e)
        return render_template('admin_login.html', result="Admin details not present")


@app.route('/reader_menu',methods=['GET'])
def menu_page():
    global reader_id
    searchType = request.args.get('search_type')
    searchTypeVal = request.args.get('SearchType')
    print("search type",searchType)
    print("search type value is ",searchTypeVal)
    try:
        if searchType == 'Id':
            searchval=int(searchTypeVal)
            checkDoc  = f"SELECT EXISTS(SELECT * FROM DOCUMENT WHERE DOCID={searchval});"
            checkCur = connection.cursor()
            checkCur.execute(checkDoc)
            checkOuput = checkCur.fetchall()
            if(checkOuput[0][0] ==1):
                retrieve_doc_by_id = f"SELECT d.DOCID,d.TITLE,c.COPYNO,p.PUBNAME,c.BID FROM DOCUMENT d JOIN PUBLISHER p ON p.PUBLISHERID = d.PUBLISHERID JOIN COPY C ON d.DOCID = c.DOCID WHERE d.DOCID={searchval} AND c.DOC_COPY_STATUS = 'Y';"
                doc_cur = connection.cursor()
                doc_cur.execute(retrieve_doc_by_id)
                output = doc_cur.fetchall()
                for i in output:
                    print(i)
                return render_template("reader_menu.html",result = output)
            else:
                return render_template("reader_menu.html",failureMsg = "id doesnt exist")
        elif searchType == 'Title':
            checkTitle  = f"SELECT EXISTS(SELECT * FROM DOCUMENT WHERE TITLE='{searchTypeVal.capitalize()}');"
            checktitleCur = connection.cursor()
            checktitleCur.execute(checkTitle)
            checkOutputtitle = checktitleCur.fetchall()
            if (checkOutputtitle[0][0] ==1):
                retrieve_doc_by_title = f"SELECT d.DOCID,d.TITLE,c.COPYNO,p.PUBNAME,c.BID FROM DOCUMENT d JOIN PUBLISHER p ON p.PUBLISHERID = d.PUBLISHERID JOIN COPY C ON d.DOCID = c.DOCID WHERE d.TITLE = '{searchTypeVal.capitalize()}' AND c.DOC_COPY_STATUS = 'Y';"
                doc_cur = connection.cursor()
                doc_cur.execute(retrieve_doc_by_title)
                output = doc_cur.fetchall()
                for i in output:
                    print(i)
                return render_template("reader_menu.html",result = output)
            else:
                return render_template("reader_menu.html",failureMsg = "title doesnt exist")
        else:
            checkPublisher  = f"SELECT EXISTS(SELECT * FROM PUBLISHER WHERE PUBNAME='{searchTypeVal.capitalize()}');"
            checkPublisherCur = connection.cursor()
            checkPublisherCur.execute(checkPublisher)
            checkOutputpub = checkPublisherCur.fetchall()
            if (checkOutputpub[0][0] ==1):
                retrieve_doc_by_publisher_name = f"SELECT d.DOCID,d.TITLE,c.COPYNO,p.PUBNAME,c.BID FROM DOCUMENT d JOIN PUBLISHER p ON p.PUBLISHERID = d.PUBLISHERID JOIN COPY C ON d.DOCID = c.DOCID WHERE p.PUBNAME = '{searchTypeVal.capitalize()}' AND c.DOC_COPY_STATUS = 'Y';"
                doc_cur = connection.cursor()
                doc_cur.execute(retrieve_doc_by_publisher_name)
                output = doc_cur.fetchall()
                for i in output:
                    print(i)
                return render_template("reader_menu.html",result = output)
            else:
                return render_template("reader_menu.html",failureMsg = "Pubisher doesnt exist")
    except Exception as e:
        print("error message is ",e)

# borrow book
@app.route('/borrowPage/<docId>/<copyNo>/<bid>')
def borrow_page(docId,copyNo,bid):
    global reader_id
    doc_id = int(docId)
    copy_no = int(copyNo)
    b_id = int(bid)
    now = datetime.now()
    borrowDate= now.strftime('%Y-%m-%d')
    # returnDate = borrowDate+timedelta(days=20)

    try:
        connection.ping()
        upcursor = connection.cursor()
        print("1")
        upcursor.execute("INSERT INTO BORROWING (BDTIME,RETURN_STATUS) VALUES (%s,%s)",(borrowDate,'N'))
        print("2")
        print("3")
        maxOfBorrowing = "SELECT MAX(BOR_NO) FROM BORROWING"
        upcursor.execute(maxOfBorrowing)
        output = upcursor.fetchall()
        print(output[0][0])
        print(type(output[0][0]))
        updStatus= f"UPDATE COPY SET DOC_COPY_STATUS = 'N' WHERE COPYNO={copy_no} AND DOCID={doc_id};"
        upcursor.execute(updStatus)
        print("4")
        upcursor.execute("INSERT INTO BORROWS VALUES (%s,%s,%s,%s,%s)",(reader_id,doc_id,b_id,copy_no,output[0][0]))
        connection.commit()
        return render_template("reader_menu.html",successMsg = "document borrowed")

    except Exception as e:
        print('error message is',e)
        return render_template("reader_menu.html",failureMsg = e)



@app.route('/reservePage/<docId>/<copyNo>/<bid>')
def reserve_book(docId,copyNo,bid):
    global reader_id
    doc_id = int(docId)
    copy_no = int(copyNo)
    b_id = int(bid)
    now = datetime.now()
    rservetime= now.strftime('%Y-%m-%d %H:%M:%S')
    # returnDate = borrowDate+timedelta(days=20)
    # TO DO CHECK THE RESERVATION TIMING SHOULD BE BEFORE 6 
    try:
        connection.ping()
        upcursor = connection.cursor()
        print("1")
        upcursor.execute("INSERT INTO RESERVATION (DTIME,RESERVATION_STATUS) VALUES (%s,%s)",(rservetime,'R'))
        print("2")
        print("3")
        maxOfBorrowing = "SELECT MAX(RES_NO) FROM RESERVATION"
        upcursor.execute(maxOfBorrowing)
        output = upcursor.fetchall()
        print(output[0][0])
        print(type(output[0][0]))
        updStatus= f"UPDATE COPY SET DOC_COPY_STATUS = 'N' WHERE COPYNO={copy_no} AND DOCID={doc_id};"
        upcursor.execute(updStatus)
        print("4")
        upcursor.execute("INSERT INTO RESERVES VALUES (%s,%s,%s,%s,%s)",(output[0][0],reader_id,doc_id,b_id,copy_no))
        connection.commit()
        return render_template("reader_menu.html",successMsg = "document RESERVED")

    except Exception as e:
        print('error message is',e)
        return render_template("reader_menu.html",failureMsg = e)



# return book
@app.route('/returnBook/<docId>/<bid>/<copyNo>')
def return_book(docId,bid,copyNo):
    global reader_id
    doc_id = int(docId)
    copy_no = int(copyNo)
    b_id = int(bid)
    now = datetime.now()
    returnDate= now.strftime('%Y-%m-%d')
    print("what is the value",returnDate)
    try:
        updateStatus = f"Update BORROWING SET RETURN_STATUS='Y' , RDTIME = '{returnDate}' WHERE BOR_NO = (SELECT B.BOR_NO FROM BORROWS B WHERE B.RID={reader_id} AND B.DOCID={doc_id} AND B.BID={b_id} AND B.COPYNO={copy_no});"
        connection.ping()
        upStacursor = connection.cursor()
        upStacursor.execute(updateStatus)
        connection.commit()
        updStatus= f"UPDATE COPY SET DOC_COPY_STATUS = 'Y' WHERE COPYNO={copy_no} AND DOCID={doc_id};"
        upStacursor.execute(updStatus)
        output = upStacursor.fetchall()
        print(output)
        connection.commit()
        if len(output )== 0:
                return render_template("reader_menu.html",successMsg = "document returned")
    except Exception as e:
        print(e)
        return render_template("reader_menu.html",failureMsg = e)



# admin


@app.route('/add_reader')
def add_reader_page():
    return render_template('addReader.html')

@app.route('/add_document')
def add_document_page():
    return render_template('addDocument.html')

@app.route('/admin/document/upload',methods=["POST"])
def upload_document():
    # docid= int(request.form.get('docid'))
    title = request.form.get('title').capitalize()
    pdate = request.form.get('pdate')
    pubid =int(request.form.get("publisherid"))
    copies=int(request.form.get("noOfcopies"))
    print(pdate)
    print(type(pdate))

    try:
        checkPublisherId = f"SELECT EXISTS (SELECT * FROM PUBLISHER WHERE PUBLISHERID = {pubid});"
        connection.ping()
        chkPubId = connection.cursor()
        chkPubId.execute(checkPublisherId)
        output = chkPubId.fetchall()
        print(output)
        if output[0][0] == 1:
            check_data = connection.cursor()
            check_data.execute("INSERT INTO DOCUMENT (TITLE, PDATE, PUBLISHERID, NumberOfCopies) VALUES (%s,%s,%s,%s)",(title,pdate,pubid,copies))
            connection.commit()
            created = check_data.fetchall()
            print("what is created",created)
        if len(created)==0:
            return render_template("addDocument.html",result ="Successfully created!")
        
    except Exception as e:
        print("ERROR!!!",e)
        return render_template("addDocument.html",result ="publisherId doesnt exist")





@app.route('/admin/add_reader',methods=["POST"])
def add_reader():
    name= request.form.get('Name')
    addr = request.form.get('Addr')
    phno = request.form.get('Phno')
    readerType =request.form.get("reader_type")
    try:
        connection.ping()
        check_data = connection.cursor()
        check_data.execute("INSERT INTO READER (RTYPE, RNAME, RADDRESS, PHONE_NO) VALUES (%s,%s,%s,%s)",(readerType,name,addr,phno))
        connection.commit()
        created = check_data.fetchall()
        print("what is created",created)
        if len(created)==0:
            return render_template("addReader.html",result ="Successfully created!")
        
    except Exception as e:
        print("ERROR!!!",e)


@app.route('/documentCopyStatus')
def documentCopyStatus():
    docId = int(request.args.get('docId'))
    copyNo = int(request.args.get('copyNo'))
    try:
        connection.ping()
        checkStatus = f"SELECT BW.RDTIME FROM BORROWING BW JOIN BORROWS B ON B.BOR_NO=BW.BOR_NO JOIN COPY C ON C.COPYNO = B.COPYNO AND C.DOCID =B.DOCID WHERE C.DOCID = {docId} AND C.COPYNO = {copyNo};"
        checkComm = connection.cursor()
        checkComm.execute(checkStatus)
        status = checkComm.fetchall()
        print(status)
        return render_template("admin_menu.html")
    except Exception as e:
        print("error is ",e)
        return render_template('admin_menu.html')


@app.route('/question1')
def question1():
    inputVal = request.args.get('RandN')
    inputbranch = request.args.get('BranchI')
    try:
        connection.ping()
        checkOutput = f"SELECT b.rid, r.rname, count(*) as borrow_count FROM BORROWS b  inner join READER r on b.rid = r.rid  where b.BID = {inputbranch}  group by b.RID  order by borrow_count desc limit {inputVal};"
        conn1 = connection.cursor()
        conn1.execute(checkOutput)
        output1 = conn1.fetchall()
        print("output 1",output1)
        return render_template("admin_menu.html",output1 = output1)
    except Exception as e:
        return render_template('admin_menu.html')

@app.route('/question2')
def question2():
    inputVal = request.args.get('RandN')
    try:
        connection.ping()
        checkOutput = f"SELECT b.rid, r.rname, count(*) as borrow_count FROM BORROWS b  inner join READER r on b.rid = r.rid group by b.RID  order by borrow_count desc limit {inputVal};"
        conn1 = connection.cursor()
        conn1.execute(checkOutput)
        output2 = conn1.fetchall()
        print("output2",output2)
        return render_template("admin_menu.html",output2 = output2)
    except Exception as e:
        return render_template('admin_menu.html')

@app.route('/question3')
def question3():
    inputVal = request.args.get('RandN')
    inputbranch = request.args.get('BranchI')
    try:
        connection.ping()
        checkOutput = f"select b.docid, d.title, count(*) as borrow_count from BORROWS b inner join DOCUMENT d ON b.docid = d.docid where b.bid = {inputbranch} group by b.docid order by borrow_count desc limit {inputVal};"
        conn1 = connection.cursor()
        conn1.execute(checkOutput)
        output3 = conn1.fetchall()
        print("output3",output3)
        return render_template("admin_menu.html",output3 = output3)
    except Exception as e:
        return render_template('admin_menu.html')

@app.route('/question4')
def question4():
    inputVal = request.args.get('RandN')
    try:
        connection.ping()
        checkOutput = f"select b.docid, d.title, count(*) as borrow_count from BORROWS b inner join DOCUMENT d ON b.docid = d.docid group by b.docid order by borrow_count desc limit {inputVal};"
        conn1 = connection.cursor()
        conn1.execute(checkOutput)
        output4 = conn1.fetchall()
        print("output4",output4)
        return render_template("admin_menu.html",output4 = output4)
    except Exception as e:
        return render_template('admin_menu.html')
    

@app.route('/question5')
def question5():
    inputVal = request.args.get('yearInput')
    print("what is inputval",inputVal)
    yearVal = inputVal[:4]
    print("year should be ",yearVal)

    try:
        connection.ping()
        checkOutput = f"SELECT bs.DOCID, d.TITLE, count(*) book_count FROM BORROWING bg INNER JOIN BORROWS bs ON bs.BOR_NO = bg.BOR_NO INNER JOIN DOCUMENT d ON bs.DOCID = d.DOCID WHERE YEAR(bg.BDTIME) = {yearVal} GROUP BY bs.DOCID;"
        conn1 = connection.cursor()
        conn1.execute(checkOutput)
        output5 = conn1.fetchall()
        print("output5",output5)
        return render_template("admin_menu.html",output5 = output5)
    except Exception as e:
        return render_template('admin_menu.html')
    
@app.route('/question6')
def question6():
    startDate = request.args.get('startdate')
    endDate = request.args.get('endDate')
    try:
        connection.ping()
        checkOutput = f"select bid, lname as branch_name, avg(fine) as average_fine from (select bs.bid, b.lname,DATEDIFF(bg.rdtime, bg.bdtime) as borr_days, DATEDIFF(bg.rdtime, bg.bdtime) * 0.20 as fine from BORROWING bg inner join BORROWS bs on bs.bor_no = bg.bor_no  inner join BRANCH b on bs.bid = b.bid where DATEDIFF(bg.rdtime, bg.bdtime) > 20 ) as penalties group by bid;"
        conn1 = connection.cursor()
        conn1.execute(checkOutput)
        output6 = conn1.fetchall()
        print("output6",output6)
        return render_template("admin_menu.html",output6 = output6)
    except Exception as e:
        return render_template('admin_menu.html')
    






connection.commit()
connection.close()


if __name__ == '__main__':
    app.run(host='localhost',port=8000)




