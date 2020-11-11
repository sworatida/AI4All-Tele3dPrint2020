import mysql.connector
# from mysql.connector import Error

mydb=mysql.connector.connect(host="119.59.104.44",user="teledpr1_tele3dprinting",passwd="auF[hhci")
mycursor=mydb.cursor()
mycursor.execute("show databases")
 
for db in mycursor:
    print(db)