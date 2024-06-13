import json
from flask import Flask, render_template, request
import sqlite3
import pickle

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/contact", methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")
        state = request.form.get("state")
        message = request.form.get("message")
        print(name, email, country, state, message)
        conn = sqlite3.connect("CONTACTUS.DB")
        cur = conn.cursor()
        cur.execute(f"""
        INSERT INTO CONTACT VALUES(
                    "{name}","{email}",
                    "{country}","{state}",
                    "{message}"
        )
        """
        )
        conn.commit()
        return render_template("message.html")
    else:
        return render_template("contactus.html")

@app.route("/check", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        make = request.form.get("make")
        model = request.form.get("model")
        year = request.form.get("year")
        kms_driven = request.form.get("kms")
        fuel = request.form.get("fuel")
        reg_city = request.form.get("city")
        car_doc = request.form.get("documents")
        assembly = request.form.get("assembly")
        transmission = request.form.get("transmission")
        print(make, model, year, kms_driven, fuel, reg_city, car_doc, assembly, transmission)

        with open("encdata.json", "r") as file:
            data = json.load(file)

        # Handle missing or unseen features by setting a default value
        mkenc = int(data["Make"].get(make, 0))
        mdlenc = int(data["Model"].get(model, 0))
        flenc = int(data["Fuel"].get(fuel, 0))
        rgctenc = int(data["Registration city"].get(reg_city, 0))
        cardcdnc = int(data["Car documents"].get(car_doc, 0))
        assenc = int(data["Assembly"].get(assembly, 0))
        trenc = int(data["Transmission"].get(transmission, 0))

        print(mkenc, mdlenc, flenc, rgctenc, cardcdnc, assenc, trenc)

        with open("model.pickle", "rb") as model_file:
            mymodel = pickle.load(model_file)

        res = mymodel.predict([[int(year), int(kms_driven), mkenc, mdlenc, flenc, rgctenc, cardcdnc, assenc, trenc]])
        print(res[0])
        return render_template("result.html", price=str(int(res[0] * 0.3)))
    else:
        return render_template("predict.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500)
