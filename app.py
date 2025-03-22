from flask import Flask, render_template, request, redirect, url_for
from Database import Database
from datetime import datetime as dt
import os

app = Flask(__name__)
DB_PATH = "/app/db/budget.db" if "IS_INSIDE_DOCKER" in os.environ.keys() else "budget.db"
db = Database(DB_PATH)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        category = request.form.get("category")
        amount1 = request.form.get("amount1") or "0.0"
        amount2 = request.form.get("amount2") or "0.0"
        date = request.form.get("date")
        is_shared = request.form.get("isShared")
        prop1 = request.form.get("prop1") or "0"
        prop2 = request.form.get("prop2") or "0"

        is_shared = True if is_shared == "on" else False
        amount1 = round(float(amount1), 2)
        amount2 = round(float(amount2), 2)
        prop1 = int(prop1)
        prop2 = int(prop2)  

        if is_shared:
            share1 = round((amount1 + amount2) * (prop1 / (prop1 + prop2)), 2)
            share2 = round((amount1 + amount2) * (prop2 / (prop1 + prop2)), 2)
        elif amount1 < 0 or amount2 < 0:
            amount1 = abs(amount1)
            amount2 = abs(amount2)
            share1 = amount2
            share2 = amount1
        else:
            share1 = amount1
            share2 = amount2

        db.addRecord(category, amount1, amount2, share1, share2, date, is_shared, prop1, prop2)

        return redirect(url_for("main"))
    
    date = request.args.get('date')
    year, month = str(dt.now().year), str(dt.now().month)
    if date:
        year, month, _ = date.split("-")

    return render_template("index.html", **db.getMonthlyRecords(year, month))


@app.route("/delete/<int:recordID>", methods=["POST"])
def delete_record(recordID):
    db.delRecord(recordID)

    return redirect(url_for("main"))


@app.route("/month/<string:date>", methods=["GET"])
def getSpecificMonthRecords(date):
    return redirect(url_for("main", date=date))


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=2306)