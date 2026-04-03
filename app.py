# file for main flask app.

from flask import Flask, render_template, request, redirect, session
from database.db import db_connection
from models.user import User
from models.ticket import Ticket
from datetime import datetime

app = Flask(__name__)
app.secret_key = "akumar_secret_key"

@app.route('/')
def login():
    ()

@app.route('/logout')
def logout():
    ()

@app.route('/register', methods=['GET', 'POST'])
def register():
    ()