from flask import *
import pymysql
import os

# create/instantiate flask app
app= Flask(__name__)
app.config['UPLOAD_FOLDER']='static/images'
# print(__name__)
@app.route("/api/signup",methods=["POST"])
def signup():
    username=request.form["username"]
    password=request.form["password"]
    email=request.form["email"]
    phone=request.form["phone"]

    # print(username,password,email,phone)
    # establish a connection to DB
    connection=pymysql.connect(host="localhost",user="root",password="",database="kombasokogarden")
    


    return jsonify({"message":"Thank you for joining"})


# Signin
@app.route("/api/signin",methods=["POST"])
def signin():
    email=request.form["email"]
    password=request.form["password"]
    print(email,password)

    # connecting to DB
    connection=pymysql.connect(host="localhost",user="root",password="",database="kombasokogarden")
    
    # cursor to execute queries with
    cursor=connection.cursor()

    # prepare sql statement
    sql="select * from users where email=%s and password=%s"

    # prepare data
    data=(email,password)

    cursor.execute(sql,data)
    # check how many row are found to met the criteria/condition
    count=cursor.rowcount
    print(count)

    # if zero the invalid crediatials-no user found
    if count==0:
        return jsonify({"message":"Invalid Credentials"})
    else:
        # else there is a user, return a message and the user's details
        user=cursor.fetchone()
        return jsonify({"message":"Login Successfull","user":user})


# addproduct function
@app.route("/api/add_product", methods=["POST"])
def add_product():
    product_name=request.form["product_name"]
    product_description=request.form["product_description"]
    product_cost=request.form["product_cost"]
    # extrct image data
    product_photo=request.files["product_photo"]

    # extract file name
    filename=product_photo.filename

    print(product_name,product_description,product_cost,filename)

    # specify where the image will be saved (in static folder-image path)
    photo_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    product_photo.save(photo_path)

    # db connetion
    connection= pymysql.connect(host="localhost",user="root",password="",database="taisokogarden")
    cursor= connection.cursor()

    # sql statement
    sql="insert into product_details (product_name,product_description,product_cost,product_photo) values(%s,%s,%s,%s)"
    # prepare data
    data=(product_name,product_description,product_cost,filename)

    # executing query using cursor
    cursor.execute(sql,data)
    # commit 
    connection.commit()
    return jsonify({"message": "Product details added successfully"})

# Get Products
@app.route("/api/get_product_details")
def get_product_details():
    connection=pymysql.connect(host="localhost",user="root",password="",database="taisokogarden")
    cursor=connection.cursor(pymysql.cursors.DictCursor)

    sql="select * from product_details "
    cursor.execute(sql)
    product_details=cursor.fetchall()
    return jsonify(product_details)


# Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})


if __name__=='__main__':
    app.run(debug=True)