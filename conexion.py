from datetime import datetime, timedelta
import os
from random import randint
from flask import Flask, redirect, render_template, request, send_from_directory, session
import mysql.connector
import hashlib

principal = Flask(__name__)
mi_DB = mysql.connector.connect(host="localhost",
                                port="3306",
                                user="root",
                                password="",
                                database="proyecto")
principal.config['CARPETAU'] = os.path.join('uploads')
principal.secret_key = str(randint(10000,99999))
principal.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
mi_cursor = mi_DB.cursor()
