from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secure-key"

DB_PATH = os.path.join("database", "bigbasket_bi.db")

# Validate login from DB
def validate_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Business Logic
def predict_churn(cluster, satisfaction, spend):
    if satisfaction < 3 and spend < 2000:
        return "High Risk of Churn"
    elif satisfaction < 3:
        return "Moderate Risk"
    else:
        return "Low Risk"

def suggest_offer(cluster):
    return {
        0: "10% cashback on essentials",
        1: "Buy 1 Get 1 on snacks",
        2: "Free delivery + loyalty points"
    }.get(cluster, "Standard Coupon")

def estimate_clv(spend, months, margin):
    return round(spend * months * (margin / 100), 2)

def get_persona(cluster):
    return {
        0: "Budget-conscious, needs frequent offers.",
        1: "Mid-tier loyal buyers. Value bundles work.",
        2: "Premium spenders. Prefer exclusives and early access."
    }.get(cluster, "General buyer")

# Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if validate_login(username, password):
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard_extended.html", active_section="report")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/churn", methods=["POST"])
def churn():
    if not session.get("logged_in"): return redirect(url_for("login"))
    cluster = int(request.form["cluster"])
    satisfaction = float(request.form["satisfaction"])
    spend = float(request.form["spend"])
    result = predict_churn(cluster, satisfaction, spend)
    return render_template("dashboard_extended.html", churn_result=result, active_section="churn")

@app.route("/offer", methods=["POST"])
def offer():
    if not session.get("logged_in"): return redirect(url_for("login"))
    cluster = int(request.form["cluster"])
    result = suggest_offer(cluster)
    return render_template("dashboard_extended.html", offer_result=result, active_section="offer")

@app.route("/clv", methods=["POST"])
def clv():
    if not session.get("logged_in"): return redirect(url_for("login"))
    spend = float(request.form["spend"])
    months = int(request.form["months"])
    margin = float(request.form["margin"])
    clv_value = estimate_clv(spend, months, margin)
    return render_template("dashboard_extended.html", clv=clv_value, active_section="clv")

@app.route("/persona", methods=["POST"])
def persona():
    if not session.get("logged_in"): return redirect(url_for("login"))
    cluster = int(request.form["cluster"])
    result = get_persona(cluster)
    return render_template("dashboard_extended.html", persona_result=result, active_section="persona")

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=10000)

