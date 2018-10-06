#!/usr/bin/env python
from flask_tagit import app
from flask import render_template

app.run(debug = True)
@app.route("/",methods=["GET","POST"])


def index():
       return render_template("input.html")
