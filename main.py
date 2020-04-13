import pyodbc
from os import listdir
from os.path import isfile, join
import datetime
import csv
import sys
import threading
import config

logfile = open(config.logfile_name, "w")
try:
    SQLConnection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SQLServer+';DATABASE='+config.DataBase+';Trusted_Connection=yes;', autocommit=False)
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print('Connection failed. Error:', sqlstate, '\n', ex.args[1])
cursor = SQLConnection.cursor()
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print(row[0])
    row = cursor.fetchone()

def quoted(input):
    return "'" + input + "'"

def pair_order_customer(
        customer_id,
        order_id
):
    try:
        query = "INSERT INTO dbo.paired_order_customer \
                (order_id, customer_id) \
                              VALUES (" + str(order_id) + ", " + str(customer_id) + ")"
        print(query, file=logfile)
        cursor.execute(query)
    except:
        print('During "pair creation" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
    return

def create_customer_info(
        first_name,
        second_name,
        third_name,
        address,
        contacts,
        phone_number
):
    try:
        query = "INSERT INTO dbo.customers " \
                    "(first_name, " \
                    "second_name," \
                    "third_name," \
                    "address, " \
                    "contacts," \
                    "phone_number)" \
                "VALUES (" + quoted(first_name) +  ", " +  \
                    quoted(second_name) +  ", " +  \
                    quoted(third_name) +  ", " +  \
                    quoted(address) +  ", "  + \
                    quoted(contacts) +  ", "  + \
                    quoted(phone_number) + ")"
        print(query, file=logfile)
        cursor.execute(query)
    except:
        print('Into "create_customer_info" during "customer info creation" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
        return None
    try:
        query = "SELECT customer_id FROM dbo.customers " \
            "WHERE ( first_name = " + quoted(first_name) +  " AND " + \
                "second_name = " + quoted(second_name) +  " AND " + \
                "third_name = " + quoted(third_name) +  " AND " + \
                "address = " + quoted(address) +  " AND "  + \
                "contacts =" + quoted(contacts) +  " AND "  + \
                "phone_number = " + quoted(phone_number) +  ");"
        print(query, file=logfile)
        cursor.execute(query)
        row = cursor.fetchone()
        return int(row[0])
    except:
        print('Into "create_customer_info" during "getting last customer id" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
    return None

def create_order_info(
        customer_id,
        status,
        sum
):
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(now, file=logfile)
    try:
        query = "INSERT INTO dbo.orders " + \
                    "(customer_id, " + \
                    "status_id," + \
                    "cost," + \
                    "creation_time) " + \
                "VALUES (" + str(customer_id) +  ", " +  \
                    quoted(status) +  ", " +  \
                    str(sum) +  ", " + \
                    quoted(now) + ")"
        print(query, file=logfile)
        cursor.execute(query)
    except Exception as e :
        print('Into "create_order_info" during "order info creation" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
        return None
    try:
        query = "SELECT order_id FROM dbo.orders " \
            "WHERE ( customer_id = " + str(customer_id) +  " AND " + \
                "status_id = " + quoted(status) +  " AND " + \
                "cost = " + str(sum) +  " AND " + \
                "creation_time = " + quoted(now) + ");"
        print(query, file=logfile)
        cursor.execute(query)
        row = cursor.fetchone()
        return int(row[0])
    except Exception as e :
        print('Into "create_order_info" during "getting last order id" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', str(e), '\n', file=logfile)
    return None

def get_order_info(
        order_id
):
    try:
        query = "SELECT * FROM dbo.orders " \
            "WHERE ( order_id = " + str(order_id) + ");"
        print(query, file=logfile)
        cursor.execute(query)
        row = cursor.fetchone()
        return row
    except:
        print('Into "get_order_info" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
    return None

def get_customer_info(
        customer_id
):
    try:
        query = "SELECT * FROM dbo.customers " \
            "WHERE ( customer_id = " + str(customer_id) + ");"
        print(query, file=logfile)
        cursor.execute(query)
        row = cursor.fetchone()
        return row
    except:
        print('Into "get_order_info" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
    return None

def get_full_order_info(
        order_id
):
    try:
        query = "SELECT * from " \
                "( SELECT * FROM dbo.orders " \
            "WHERE ( order_id = " + str(order_id) + ") ) as ORD " \
                "LEFT JOIN dbo.customers as CUST on CUST.customer_id = ORD.customer_ID; "
        print(query, file=logfile)
        cursor.execute(query)
        row = cursor.fetchone()
        return row
    except:
        print('Into "get_order_info" smth went wrong.. Error says:',
              sys.exc_info()[0], '\n', file=logfile)
    return None


def change_order_info(
        order_id,
        customer_id,
        prev_customer_id,
        status,
        prev_status,
        sum,
        prev_sum,
        prev_now
):
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
        query = "UPDATE  dbo.orders " \
                "SET customer_id = " + str(customer_id) +  " , " + \
                "status_id = " + quoted(status) +  " ," + \
                "cost = " + str(sum) +  " , " + \
                "creation_time = " + quoted(prev_now) + " , "\
                "update_time = " + quoted(now) + " " + \
                "WHERE ( customer_id = " + str(prev_customer_id) + " AND " + \
                "status_id = " + quoted(prev_status) + " AND " + \
                "cost = " + str(prev_sum) + " AND " + \
                "creation_time = " + quoted(prev_now) + ");"
        print(query, file=logfile)
        cursor.execute(query)
    except Exception as e:
        print('Into "change_order_info" smth went wrong.. Error says:',
              sys.exc_info()[0],'\n', str(e), '\n', file=logfile)
    return None


def change_full_order_info(
        order_id, *,
        status = None,
        sum = None,
        first_name = None,
        second_name = None,
        third_name = None,
        address = None,
        contacts = None,
        phone_number = None
):
    order_info = get_full_order_info(order_id)
    customer_id = order_info[6]
    prev_customer_id = order_info[6]
    prev_status = order_info[2]
    prev_sum = order_info[3]
    prev_now = order_info[4].strftime("%d-%m-%Y %H:%M:%S")


    if (first_name is not None or second_name is not None or third_name is not None
        or address is not None or contacts is not None or phone_number is not None):
        first_name = order_info[7] if first_name is None else str(first_name)
        second_name = order_info[8] if second_name is None else str(second_name)
        third_name = order_info[9] if third_name is None else str(third_name)
        address = order_info[10] if address is None else str(address)
        contacts = order_info[11] if contacts is None else str(contacts)
        phone_number = order_info[12] if phone_number is None else str(phone_number)
        customer_id = create_customer_info(
            first_name,
            second_name,
            third_name,
            address,
            contacts,
            phone_number)

    status = order_info[2] if status is None else status
    sum = order_info[3] if sum is None else sum

    change_order_info(
        order_info,
        customer_id,
        prev_customer_id,
        status,
        prev_status,
        sum,
        prev_sum,
        prev_now
    )
    SQLConnection.commit()

def create_order(
        status,
        sum,
        first_name,
        second_name,
        third_name,
        address,
        contacts,
        phone_number

):
    try:
        customer_id = create_customer_info(
            first_name,
            second_name,
            third_name,
            address,
            contacts,
            phone_number)
        order_id = create_order_info(
            customer_id,
            status,
            sum)
        pair_order_customer(customer_id, order_id)
        print("Order #" + str(order_id) + " created", file=logfile)
        SQLConnection.commit()
        return order_id
    except:
        print("PANIC ATTACK!!! Create order dead...", file=logfile)
    return

