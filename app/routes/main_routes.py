from flask import app, render_template

@app.route("/")
def landing():
    return render_template("landing.html")
