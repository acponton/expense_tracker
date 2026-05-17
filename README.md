# Overview

This project is a simple Expense Tracker that I built to practice working with Python and a SQL relational database. 
My goal was to learn how a real program can store information, update it, and run useful reports using SQL queries. 
I wanted hands‑on experience connecting Python code to a database and performing basic operations like adding data, reading it, editing it, and deleting it.

The program runs in the terminal. When you start it, you see a menu with options to add an expense, list all expenses, edit an expense, delete an expense, and view reports. 
All the information is saved in a SQLite database file, which the program creates automatically the first time it runs.

This project helped me understand how Python and SQL work together and how to design a small but functional database‑driven application.

[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

This project uses SQLite, which is a simple relational database stored in a single file. It works well for small projects and is easy to use with Python.

# Database Structure
The database has one table called expenses, which stores all the information the program needs:

id – a unique number for each expense

amount – how much money was spent

category – the type of expense (Food, Rent, etc.)

date – the date of the expense in YYYY-MM-DD format

note – an optional description

This structure makes it easy to run SQL queries like totals, averages, and filtering by date.

# Development Environment

I used the following tools to build this project:

Python 3

SQLite (through Python’s built‑in sqlite3 library)

Visual Studio Code as my code editor

Windows PowerShell to run the program

# Programming Language & Libraries

Python was used to write the program

sqlite3 was used to connect to the database and run SQL commands

datetime was used to check and format dates

No extra libraries were needed.

# Useful Websites

These websites helped me understand Python, SQL, and SQLite:

https://www.sqlite.org/docs.html
https://www.w3schools.com/sql/
https://www.w3schools.com/python/

# Future Work

Here are some things I would like to add or improve in the future:

* Add a separate categories table and use SQL JOINs

* Add more reports (weekly, monthly, yearly summaries)

* Add an option to export expenses to a CSV file

* Add search filters (by category, amount range, or keyword)

* Create a simple graphical interface instead of a terminal menu

* Add charts to visualize spending trends
