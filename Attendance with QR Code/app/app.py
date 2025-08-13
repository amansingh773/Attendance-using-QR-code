from flask import Flask,request, render_template,url_for,send_from_directory
from qr import Qr
import os
from datetime import datetime
import csv
import socket
ip=[]
Port = 5657
app = Flask(__name__, static_url_path='/static', static_folder='static')


def file_attendance(cred_data,subject):
   rows=list()
   rows.append(cred_data)
   fields = ['Name', 'RollNo', 'Year', 'Time']  
   filename =r"attendance/"+ str(datetime.date(datetime.now()))+f"_"+subject+".csv"
   if not os.path.exists(filename) :
        with open(filename, 'w') as csvfile: 
  
            csvwriter = csv.writer(csvfile)  

            # riting the fields  
            csvwriter.writerow(fields)  

            # riting the data rows  
            csvwriter.writerow(cred_data)
   else:
       with open(filename, 'a') as f:
 
    # Pass this file object to csv.writer()
    # and get a writer object
          writer_object = csv.writer(f)
 
    # Pass the list as an argument into
    # the writerow()
          writer_object.writerow(cred_data)
       
       # writing to csv file 
   

@app.route('/')
def home():
    return render_template("Teacher.html")


@app.route('/teacher_login/', methods=['GET', 'POST'])
def Teacher_login():
    if request.method=='POST':
        global l_url
        global subject
        subject=request.form['subject']
        name=request.form['name']
        email=request.form['email']
        password=request.form['pswd']
        credential = [name,email,subject,password]
        with open("teacher.csv","r") as f:
            data= csv.DictReader(f)
            
            new_data =[list(i.values()) for i in data]
            if credential not in new_data:
                err=True
                return render_template('Teacher.html',err=err)
        lc_ip= socket.gethostbyname(socket.gethostname())
        l_url =f"http://{lc_ip}:{Port}/attendance/create/"+subject
        QR=Qr(l_url)
    return render_template('home.html',QR=QR)


@app.route(f'/attendance/create/<subject>', methods=['GET', 'POST'])
def add_attendance(subject):
    if request.method =='POST':
        if request.remote_addr in ip:
            return render_template("add_attendance.html",res=True)
        ip.append(request.remote_addr)
        try:
            c_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            name = str(request.form.get("name"))
            year = int(request.form.get("year"))
            rollno =int(request.form.get("rollno"))
        except Exception as e:
            print(e)
            return render_template("Student.html",err=True)
        
        cred_data=[name,rollno,year,c_time]
        print(cred_data)
        file_attendance(cred_data=cred_data,subject=subject)
        print(cred_data)
        return render_template("sucess.html",year=year,rollno=rollno,name=name,time=c_time)
        
    return render_template("Student.html")



@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        subject=request.form["subject"]
        password = request.form["pswd"]
        cred_data=[name,email,subject,password]
        print(cred_data)
        with open("teacher.csv", 'a') as f:
       
            writer_object = csv.writer(f)
    
     
            writer_object.writerow(cred_data)
            message="Account created successfully"
        return render_template("Teacher.html",message=message)

    return render_template("Teacher.html")



@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='images\icon.png')
   

app.run(host="0.0.0.0", port = Port)
