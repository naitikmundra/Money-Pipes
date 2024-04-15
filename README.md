# Money-Pipes
This is  the backend flask code in main.py and the front end code in Templates folder.
entire website is hosted/availabe here- https://naitikmundra18.pythonanywhere.com (it might be a bit slow to load, hosted on a testing platform.)

**GETTING AN ERROR LIKE THIS ON WEBSITE - JUST RELOAD THE PAGE 2-3 TIMES**
[![](https://i.ibb.co/19XYR3Y/Capture34.png)]

# How to run the website locally?
First clone the repository to a local folder.

Also make sure you have **python** installed.

This website runs on a flask server hosted locally, just execute **main.py** file and open the highlighted link that includes your ip address in the browser 
[![](https://i.ibb.co/vJQyLvR/Capture.png)]



**THE MAIN.PY FILE REQUIRES FLASK and MYSQL DB TABLES TO RUN AND A PRE-SETUP MYSQL SERVER (you can download and install xampp) WITH username and password known.**
Download xampp here - https://www.apachefriends.org/
In terminal or comand prompt do:

```pip install flask Flask-SQLAlchemy mysqlclient ipinfo requests sqlalchemy```

In mysql terminal do:

```
CREATE DATABASE IF NOT EXISTS moneypipes;

USE moneypipes;

CREATE TABLE User (
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE Likes (
    email VARCHAR(100) PRIMARY KEY,
    postid INT
);

CREATE TABLE Dislikes (
    email VARCHAR(100) PRIMARY KEY,
    postid INT
);

CREATE TABLE Pipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100),
    title VARCHAR(100),
    content VARCHAR(10000),
    fullname VARCHAR(100),
    category VARCHAR(1000),
    salary VARCHAR(1000),
    country VARCHAR(1000),
    likes INT,
    dislikes INT,
    fun VARCHAR(100)
);

CREATE TABLE Comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100),
    content VARCHAR(10000),
    fullname VARCHAR(100),
    type INT,
    postid INT
);
```

In main.py file line no. 31
`app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moneypipes'
`

CHANGE THIS LINE ACCORDING TO YOUR NEEDS 

**root**  to **your mysql username**

after: add the password 

**:passwordhere** 

if **no password** leave blank after **:** 

leave **`@localhost/moneypipes` the same**

# Additional Notes

AUTO COUNTRY DETECTION WORKS ONLY WITH PUBLICALLY HOSTED WEBSITE - https://naitikmundra18.pythonanywhere.com. 
If you are still unable to run, You can chek the basic html//css frontend code in the Templates folder or simply check functionality at  https://naitikmundra18.pythonanywhere.com
