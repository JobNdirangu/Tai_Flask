from flask  import *

# create/instatiate  flask app
app=Flask(__name__)

# routing
@app.route("/api/home")
def home():
    return jsonify({"message":"Welcome to HOME API"})

@app.route("/api/products")
def products():
    return jsonify({"message":"Welcome to products API"})

@app.route("/api/calc",methods=["POST"])
def calc():
    number1=request.form["number1"]
    number2=request.form["number2"]
    sum=int(number1)+int(number2)
    dif=int(number1)-int(number2)

    return jsonify({"answer":sum,"dif":dif})

if __name__=='__main__':
    app.run(debug=True)