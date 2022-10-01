from flask import Flask, request, jsonify
import pymysql.cursors
from flask_cors import CORS
import tabula
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse



class Db:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", password="", cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.uid = 1
        self.pid = 1
        self.rid = 1
        try:
            self.cursor.execute("use website")
            self.cursor.execute("select * from user")
            result = self.cursor.fetchall()
            self.uid = len(result) + 1 
            self.cursor.execute("select * from properties")
            result = self.cursor.fetchall()
            self.pid = len(result) + 1 
            self.cursor.execute("select * from records")
            result = self.cursor.fetchall()
            self.rid = len(result) + 1 
            self.cursor.execute("SET GLOBAL max_allowed_packet=67108864")
            self.connection.commit()
            print(self.rid, self.uid, self.pid)
        except Exception:
            self.populate() 
        
    def populate(self):
        self.cursor.execute("source setup.sql")
        self.cursor.execute("SET GLOBAL max_allowed_packet=67108864")
        self.connection.commit()
    
    def is_date(self, string, fuzzy=False):
        try: 
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def login(self, email, password):
        self.cursor.execute(f"select * from user where uemail = \"{email}\";")
        result = self.cursor.fetchall()
        if len(result) > 0:
            paswrd = result[0]['upassword']
            if password == paswrd:
                return True
        return False

    def signup(self, username, password, email, phonenum):
        self.cursor.execute(f"select * from user where uemail = \"{email}\";")
        result = self.cursor.fetchall()
        if len(result) > 0:
            return False
        self.cursor.execute(f"insert into user values(\"{self.uid}\", \"{username}\", \"{password}\", \"{email}\", \"{phonenum}\");")
        self.connection.commit()
        self.uid += 1
        return True

    def getmyproperty(self, uemail):
        self.cursor.execute(f"select uid from user where uemail = \"{uemail}\"")
        uid = self.cursor.fetchall()
        uid = uid[0]["uid"]
        self.cursor.execute(f"select pname, prooms, pavgocc, pavgadr, plocation, pn from properties where uid = {uid}")
        result = self.cursor.fetchall()
        return result
    
    def addProp(self, uemail, name, rooms, location):
        self.cursor.execute(f"select uid from user where uemail = \"{uemail}\"")
        uid = self.cursor.fetchall()
        uid = uid[0]["uid"]
        self.cursor.execute(f"insert into properties values({self.pid}, \"{name}\", {rooms}, 0, 0, \"{location}\", 0, {uid})")
        self.pid += 1
        self.connection.commit()
        return 

    def editProp(self, uemail, oldName, name, rooms, location):
        self.cursor.execute(f"select uid from user where uemail = \"{uemail}\"")
        uid = self.cursor.fetchall()
        uid = uid[0]["uid"]
        self.cursor.execute(f"select pid from properties where uid={uid} and pname=\"{oldName}\"")
        pid = self.cursor.fetchall()[0]['pid']
        self.cursor.execute(f"update properties set pname=\"{name}\", prooms={rooms}, plocation=\"{location}\" where pid={pid}")
        self.cursor.fetchall()
        self.connection.commit()
        return 
    
    def deleteProp(self, uemail, pname):
        self.cursor.execute(f"select uid from user where uemail = \"{uemail}\"")
        uid = self.cursor.fetchall()
        uid = uid[0]["uid"]
        self.cursor.execute(f"select pid from properties where uid={uid} and pname=\"{pname}\"")
        pid = self.cursor.fetchall()[0]['pid']
        self.cursor.execute(f"delete from records where pid={pid};")
        self.cursor.execute(f"delete from properties where pid={pid};")
        self.connection.commit()
        return True

    def addRecord(self, uemail, pname, date, rev, rooms, currency):
        if pname == "0":
            print('not selected')
            return False
        if not self.is_date(date, True):
            return True
        self.cursor.execute(f"select pid from properties inner join user on properties.uid = user.uid where user.uemail = \"{uemail}\" and pname=\"{pname}\"")
        result = self.cursor.fetchall()
        pid = result[0]['pid']
        self.cursor.execute(f"select pavgocc, pavgadr, pn, prooms from properties where pid={pid}")
        result = self.cursor.fetchall()
        occ = result[0]['pavgocc']
        adr = result[0]['pavgadr']
        prooms = result[0]['prooms']
        n = result[0]['pn']
        self.cursor.execute(f"insert into records values({self.rid}, {pid}, \"{date}\", {rev}, {rooms})")
        n += 1
        occ += round((int(rooms) / int(prooms)) * 100, 2)
        adr += round(float(rev) / int(rooms))
        self.cursor.execute(f"update properties set pavgadr=\"{adr}\", pavgocc={occ}, pn=\"{n}\" where pid={pid}")
        self.connection.commit()
        self.rid += 1
        return True
    
    def loadRecord(self, uemail, pname, sdate, edate):
        self.cursor.execute(f"select pid from properties inner join user on properties.uid = user.uid where user.uemail = \"{uemail}\" and pname=\"{pname}\"")
        result = self.cursor.fetchall()
        pid = result[0]['pid']
        self.cursor.execute(f"select * from records where (pid={pid} and rdate <= \'{edate}\' and rdate >= \'{sdate}\') order by rdate asc")
        data = self.cursor.fetchall()
        return (data, True)
    
    def readpdf(self, uemail, pname, filename):
        # reading pdf file into dataframe
        df = tabula.read_pdf(filename)
        dataframe = pd.DataFrame(df[0])
        # extracting important columns and rows
        dataframe.columns = dataframe.iloc[3]
        dataframe = dataframe.iloc[6:, :]
        important_data = dataframe[['Date', '#Rooms', 'Net Room Rev']]
        for _, data in important_data.iterrows():
            date = data['Date']
            date = date[-6:-4] + date[2:-6] + date[:2]
            rooms = data['#Rooms']
            netrev = data['Net Room Rev'].replace(',', '')
            self.addRecord(uemail, pname, date, netrev, rooms, 'TL')
        return True
    
    def export(self, pname, sdate, edate, uemail):
        data, _ = self.loadRecord(uemail, pname, sdate, edate)
        df = pd.DataFrame(data)
        df = df[['rdate', 'rrooms', 'rrevenue']]
        df['rrevenue'] = round(pd.to_numeric(df['rrevenue']) / df['rrooms'], 2)
        df['rrooms'] = round(df['rrooms'] / prooms * 100, 2)
        df['rrevpar'] = round(df['rrooms'] * df['rrevenue'] / 100, 2)
        writer = pd.ExcelWriter("technical.xlsx", engine='xlsxwriter', date_format = 'yyyy-mm-dd', datetime_format='yyyy-mm-dd')
        workbook = writer.book
        sheet_name = 'All'
        df[['rdate', 'rrooms', 'rrevenue', 'rrevpar']].to_excel(writer, sheet_name=sheet_name)
        worksheet = writer.sheets[sheet_name]
        # Set column width of Date
        worksheet.set_column(1, 1, 10)
        
        # Create a new chart object.
        chart1 = workbook.add_chart({'type': 'line'})
        chart1.add_series({
                'name': 'Occupancy',
                'categories': [sheet_name, 1, 1, len(df), 1],
                'values': [sheet_name, 1, 2, len(df), 2],
        })
        # Create a new chart object.
        chart2 = workbook.add_chart({'type': 'line'})
        chart2.add_series({
                'name': "ADR",
                'categories': [sheet_name, 1, 1, len(data), 1],
                'values': [sheet_name, 1, 3, len(data), 3],
        })
        # Create a new chart object.
        chart3 = workbook.add_chart({'type': 'line'})
        chart3.add_series({
                'name': "RevPAR",
                'categories': [sheet_name, 1, 1, len(data), 1],
                'values': [sheet_name, 1, 4, len(data), 4],
        })
        # Insert the chart into the worksheet.
        worksheet.insert_chart('G2', chart1)
        worksheet.insert_chart('G20', chart2)
        worksheet.insert_chart('O2', chart3)
        writer.close()
        


# database class
db = Db()


# API
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/login", methods=['get'])
def login():
    email = request.args.get("username", None)
    password = request.args.get("password", None)
    data = {"status": False, "text": "credentials are wrong "}
    if db.login(email, password):
        data = {"status": True, "text": "user successfully logged in"}
    return jsonify(data)

@app.route("/signup", methods=['get'])
def signup():
    username = request.args.get("username", None)
    password = request.args.get("password", None)
    email = request.args.get("email", None)
    phonenum = request.args.get("phone", None)
    data = {"status": False, "text": "You already have an account"}
    if db.signup(username, password, email, phonenum):
        data = {"status": True , "text": "user successfully registired"}
    return jsonify(data)
    
@app.route("/getmyproperty", methods=['get'])
def getmyproperty():
    uemail = request.args.get("username", None)
    result = db.getmyproperty(uemail)
    return jsonify(result)

@app.route("/addProp", methods=['get'])
def addProp():
    uemail = request.args.get("username", None)
    name = request.args.get("name", None)
    rooms = request.args.get("rooms", None)
    location = request.args.get("location", None)
    db.addProp(uemail, name, rooms, location)
    result = {"status": True, "text": "Property Added Successfully"}
    return jsonify(result)

@app.route("/editProp", methods=['get'])
def editProp():
    uemail = request.args.get("username", None)
    name = request.args.get("name", None)
    old = request.args.get("old", None)
    rooms = request.args.get("rooms", None)
    location = request.args.get("location", None)
    db.editProp(uemail, old, name, rooms, location)
    result = {"status": True, "text": "Property Edited Successfully"}
    return jsonify(result)

@app.route("/deleteProp", methods=['get'])
def deleteProp():
    uemail = request.args.get("username", None)
    pname = request.args.get("pname", None)
    result = {"status": False, "text": "Error Deleting Property"}
    if db.deleteProp(uemail, pname):
        result = {"status": True, "text": "Property Deleted Successfully"}
    return jsonify(result)

@app.route("/addRecord", methods=['get'])
def addRecord():
    uemail = request.args.get("uemail", None)
    pname = request.args.get("pname", None)
    date = request.args.get("date", None)
    rev = request.args.get("rev", None)
    rooms = request.args.get("rooms", None)
    currency = request.args.get("curr", None)
    result = {"status": False, "text": "Error adding record"}
    if db.addRecord(uemail, pname, date, rev, rooms, currency):
        result = {"status": True, "text": "Record Added Successfully"}
    return jsonify(result)

@app.route("/loadRecords", methods=['get'])
def loadRecord():
    pname = request.args.get("pname", None)
    startdate = request.args.get("sd", None)
    enddate = request.args.get("ed", None)
    uemail = request.args.get("uemail", None)
    result = {"status": False, "text": "Error loading record", "data": {}}
    data, check = db.loadRecord(uemail, pname, startdate, enddate)
    if check:
        result = {"status": True, "text": "Record Loaded Successfully", "data": data}
    return jsonify(result)

@app.route("/upload", methods=['post'])
def upload():
    data = request.data
    uemail = request.args.get('uemail', None)
    pname = request.args.get('pname', None)
    f = open('output.pdf', 'wb')
    f.write(data)
    f.close()
    result = {"status": False, "text": "Failed to Upload File"}
    if db.readpdf(uemail, pname, 'output.pdf'):
        result = {"status": True, "text": "File Uploaded Successfully"}
    return jsonify(result)

@app.route("/export", methods=["get"])
def export():
    pname = request.args.get("pname", None)
    startdate = request.args.get("sd", None)
    enddate = request.args.get("ed", None)
    uemail = request.args.get("uemail", None)
    result = {"status": False, "text": "Error Exporting Report"}
    if db.export(pname, startdate, enddate, uemail):
        result = {"status": True, "text": "Report Exported Successfully"}
    return jsonify(result)


app.run(debug=True, port=5000)