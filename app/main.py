#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json 
import requests
import os
import MySQLdb
from fastapi.staticfiles import StaticFiles
# import boto3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "zgb8ts" 

# The URL for this API has a /docs endpoint that lets you see and test
# your various endpoints/methods.


# The zone apex is the 'default' page for a URL
# This will return a simple hello world via GET method.

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "World"}

@app.get("/albums")
def get_albums():
    db= MySQLdb.connect(host= DBHOST, user= DBUSER, passwd= DBPASS , db= DB)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("""SELECT * FROM albums ORDER BY name""")
    results = c.fetchall()
    db.close()
    return results

@app.get("/albums/{id}")
def get_one_album(id):
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM albums WHERE id=" + id)
    results = c.fetchall()
    db.close()
    return results

@app.get("/github/repos/{user}")
def get_my_repos(user):
    url= "https://api.github.com/users/"+ user + "/repos"
    response= requests.get(url) 
    body= json.loads(response.text)
    return {"repos": body} # returning a key-value pair because it is in json

# Endpoints and Methods
# /blah - endpoint
# GET/POST/DELETE/PATCH - methods
# 
# Simple GET method demo
# Adds two integers as PATH parameters
@app.get("/add/{number_1}/{number_2}")
def add_me(number_1: int, number_2: int):
    sum = number_1 + number_2
    return {"sum": sum}

# Let's develop a new one:

@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int):
    multiply= num1 * num2
    return {"multiply": multiply}

# Test two
@app.get("/divide/{num1}/{num2}")
def divide(num1:int, num2: int):
    divide= num1/num2
    return {"divide":divide}


@app.get("/critical_value_quartile/{num}")
def critical_value_quartiles(num:float):
   quartile= round((1-num)/2, 3)
   quartile2= num + quartile
   return {"critical_value_quartile": (quartile, quartile2)}
 
## Parameters
# Introduce parameter data types and defaults from the Optional library
@app.get("/items/{item_id}")
def read_items(item_id: int, q: str = None, s: str = None):
    # to-do: could be used to read from/write to database, use item_id as query parameter
    # and fetch results. The q and s URL parameters are optional.
    # - database
    # - flat text
    # - another api (internal)
    # - another api (external)
    return {"item_id": item_id, "q": q, "s": s}


## Data Modeling
# Model data you are expecting.
# Set defaults, data types, etc.
#
# Imagine the JSON below as a payload via POST method
# The endpoint can then parse the data by field (name, description, price, tax)
# {
#     "name":"Trek Domaine 5000",
#     "description": "Racing frame",
#     "price": 7200,
#     "tax": 381
# }

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# Start using the "Item" BaseModel
# Post / Delete / Patch methods
@app.post("/items/{item_id}")
def add_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, item: Item):
    return {"action": "deleted", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    return {"action": "patch", "item_id": item_id}


# Use another library to make an external API request.
# An API within an API!
# https://api.github.com/users/garnaat/repos


# Incorporate with boto3: simpler than the `requests` library:
# @app.get("/aws/s3")
# def fetch_buckets():
#     s3 = boto3.client("s3")
#     response = s3.list_buckets()
#     buckets = response['Buckets']
#     return {"buckets": buckets}
