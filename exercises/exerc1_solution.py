#!/usr/bin/env python
# coding=utf-8

# ------------------------------------------------------------------------------
# Connect to Google Drive API | Exercise 1
# ------------------------------------------------------------------------------
# jose maria sosa


import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

file_name = "credentials.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

book_name = 'sales'
sheet_name = 'sales1'
sheet = client.open(book_name).worksheet(sheet_name)

# ------------------------------------------------------------------------------
# 1. Print the Total_Orders.

###############################
### Code the solution here! ###
###############################

# ------------------------------------------------------------------------------
# 2. Print the sales and orders only of May 2019.

###############################
### Code the solution here! ###
###############################


# ------------------------------------------------------------------------------
# 3. Print the table of sales as a Pandas DataFrame.

###############################
### Code the solution here! ###
###############################


# ------------------------------------------------------------------------------
# 4. Calculate the Forecast for september using the average of the last 3 month.

###############################
### Code the solution here! ###
###############################


# ------------------------------------------------------------------------------
# 5. Calculate the Average Ticket Price.

###############################
### Code the solution here! ###
###############################

