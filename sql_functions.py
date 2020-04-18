import mysql.connector
import numpy as np
from random import randint
import pyqrcode
import png
import datetime
import os

class EmployeeAccess:
    def __init__(self, employee_pin):
        self.employee_id = employee_pin

#######################
#Establish connection #
#to mysql database    #
#######################
def dbConnect(): 
    mydb = mysql.connector.connect(
            host="localhost",
            user="locker",
            passwd="srslocker@265bs*",
            database="srs"
    )
    return mydb
#######################
#Select statement to  #
#gather table data    #
#######################
def dbSelect(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT OrderID FROM Orders")
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult

#Select all pins from EmployeePin
def dbSelectEmployeePin(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT pin FROM EmployeePins")
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult

def dbSelectOrderID(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT OrderID FROM Orders")
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult

def dbSelectUnlockCode(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT UnlockCode FROM OrdersStocked")
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult

#######################
#Formats string from  #
#previous statement   #
#to get rid of        #
#delimiters           #
#######################
def dbFormat(myresult):
    myresult = str(myresult).replace("(","")
    myresult = str(myresult).replace(")","")
    myresult = str(myresult).replace(",","")
    myresult = str(myresult).replace("[","")
    myresult = str(myresult).replace("]","")
    myresult = str(myresult).replace("'","")
    myresult = str(myresult).replace("'","")
    return myresult

def removebrackets(myresult):
    myresult = str(myresult).replace("[","")
    myresult = str(myresult).replace("]","")
    return myresult

#######################
#Converts string to a #
#list of split        #
#strings              #
#######################
def dbList(myresult):
    ids = list(map(int, myresult.split()))
    return ids

#######################
#Uses numpy to convert#
#list into array      #
#######################
def dbArray(ids):
    id_array = np.array(ids)
    return id_array

def makearray(myresult):
    ids = list(map(int, myresult.split()))
    id_array = np.array(ids)
    return id_array

#######################
#Prints array         #
#                     #
#######################
def printArray(id_array):
    for x in id_array:
        print(x)

#######################
#Primary function that can be used that returns a formatted
#array containing the selected data
#######################
def storePin():
    mydb = dbConnect()
    myresult = dbSelect(mydb)
    myresult = dbFormat(myresult)
    mylist = dbList(myresult)
    myarray = dbArray(mylist)
    return myarray

def storeEmployeePin():
    mydb = dbConnect()
    myresult = dbSelectEmployeePin(mydb)
    myresult = dbFormat(myresult)
    mylist = dbList(myresult)
    myarray = dbArray(mylist)
    return myarray

def storeOrderID():
    mydb = dbConnect()
    myresult = dbSelectOrderID(mydb)
    myresult = dbFormat(myresult)
    mylist = dbList(myresult)
    myarray = dbArray(mylist)
    return myarray

def storeUnlockCode():
    mydb = dbConnect()
    myresult = dbSelectUnlockCode(mydb)
    myresult = dbFormat(myresult)
    mylist = dbList(myresult)
    myarray = dbArray(mylist)
    return myarray

#######################
#Compare unlock code  #
#to order id          #
#######################
def comparePin(pin, id_array):
    myarraylen = len(id_array)
    for x in range(myarraylen):
        if pin == id_array[x]:
            print('hello')


def compareEmployeePin(pin, id_array):
    myarraylen = len(id_array)
    for x in range(myarraylen):
        if int(pin) == int(id_array[x]):
            return True
    return False

def compareOrderID(order_id, id_array):
    myarraylen = len(id_array)
    for x in range(myarraylen):
        if int(order_id) == int(id_array[x]):
            return True
    return False

def compareUnlockCode(unlock_code, id_array):
    myarraylen = len(id_array)
    for x in range(myarraylen):
        if int(unlock_code) == int(id_array[x]):
            return True
    return False

#######################
#Constructors and 
#Destructors for 
#OrdersStocked table
#######################
def InsertOrdersStocked(orders_stocked_tuple):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_insert_query = "INSERT INTO OrdersStocked (StockedOrderID, EmployeeID, OrderID, UnlockCode, LockID, DateTimeStocked) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql_insert_query, orders_stocked_tuple)
    mydb.commit()
    mydb.close()
    
def CreateOrdersStocked(employee_id, order_id, unlock_code, lock_id):
    stocked_order_ID = GenerateStockedOrderID()
    date_time_stocked = datetime.datetime.now()
    orders_stocked_tuple = (stocked_order_ID, employee_id, order_id, unlock_code, lock_id, date_time_stocked)
    return orders_stocked_tuple

def GenerateStockedOrderID():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query1 = "SELECT COUNT(*) FROM ArchiveOrdersStocked"
    sql_select_query2 = "SELECT COUNT(*) FROM OrdersStocked"
    mycursor.execute(sql_select_query1)
    myresult = mycursor.fetchall()
    myresult = dbFormat(myresult)
    num_archive_orders = int(myresult)

    mycursor.execute(sql_select_query2)
    myresult = mycursor.fetchall()
    myresult = dbFormat(myresult)
    num_stocked_orders = int(myresult)
    
    mydb.close()

    stocked_order_id = int(num_archive_orders) + int(num_stocked_orders) + int(100000)
    return stocked_order_id

#insert into OrdersStocked
def SwitchOrdersStockToArchive(unlock_code):
    mydb = dbConnect()
    mycursor = mydb.cursor(buffered=True)
    sql_select_query = "SELECT * FROM OrdersStocked WHERE UnlockCode = %s"
    mycursor.execute(sql_select_query, (unlock_code,))
    
    myresult = mycursor.fetchone()
    
    datetime_retrieved = datetime.datetime.now()

    archive_tuple = myresult + (datetime_retrieved,)

    sql_insert_query = "INSERT INTO ArchiveOrdersStocked (StockedOrderID, EmployeeID, OrderID, UnlockCode, LockID, DateTimeStocked, DateTimeRetrieved) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql_insert_query, archive_tuple)
    mydb.commit()

    sql_delete_query = "DELETE FROM OrdersStocked WHERE UnlockCode = %s"
    mycursor.execute(sql_delete_query, (unlock_code,))

    mydb.commit()
    mydb.close()

#extract customer email and phone number
def ExtractEmail(order_id):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = "SELECT CustomerEmail FROM Orders WHERE OrderID = %s"
    mycursor.execute(sql_select_query, (order_id,))
    myresult = mycursor.fetchall()
    customer_email = dbFormat(myresult)
    mydb.close()
    return(customer_email)

def ExtractPhone(order_id):
    pass
    
def UnlockCodeInUse(unlock_code):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = """SELECT * FROM ActiveUnlockCodes"""
    mycursor.execute(sql_select_query)
    myresult = mycursor.fetchall()
    myresult = dbFormat(myresult)
    mylist = dbList(myresult)
    myarray = dbArray(mylist)
    mydb.close()
    myarraylen = len(myarray)
    for x in range(myarraylen):
        if int(unlock_code) == int(myarray[x]):
            return True
    return False
    
def InsertUnlockCodeInActiveCodes(unlock_code):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_insert_query = "INSERT INTO ActiveUnlockCodes (UnlockCode) VALUES (%s)"
    mycursor.execute(sql_insert_query, (unlock_code,))
    mydb.commit()
    mydb.close()
    

#generate unlock code
def GenerateUnlockCode():
    unlock_code = randint(2000, 4000)
    
    while UnlockCodeInUse(unlock_code) is True:
        unlock_code = randint(2000, 4000)

    InsertUnlockCodeInActiveCodes(unlock_code)
    return unlock_code
    
#generate qrcode png with order_id and unlock_code
def GenerateQRCode(order_id, unlock_code):
    qrcode = pyqrcode.create(int(unlock_code))
    qrcode.png(str(order_id), scale=6)

#Delete <order_id>.png
def DeleteQRCodeFile(order_id):
    file_name = str(order_id)
    if os.path.exists(file_name):
        os.remove(file_name)
    
def GetOrderIDOfUnlockCode(unlock_code):
    mydb = dbConnect()
    mycursor = mydb.cursor(buffered=True)
    sql_select_query = "SELECT OrderID FROM OrdersStocked WHERE UnlockCode = %s"
    mycursor.execute(sql_select_query, (unlock_code,))
    myresult = mycursor.fetchone()
    mydb.close()
    return myresult[0]
    

def InsertEmployeeIDEmployeeAccess(employee_id):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_insert_query = "INSERT INTO EmployeeAccess (employee_id, order_id) VALUES (%s, %s)"
    mycursor.execute(sql_insert_query, (employee_id, 'NULL',))
    mydb.commit()
    mydb.close()

def InsertOrderIDEmployeeAccess(order_id):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_update_query = "UPDATE EmployeeAccess SET order_id = %s WHERE order_id = %s"
    mycursor.execute(sql_update_query, (order_id, 'NULL',))
    mydb.commit()
    mydb.close()

def ReadEmployeeIDEmployeeAccess():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = ("SELECT * FROM EmployeeAccess")
    mycursor.execute(sql_select_query)
    myresult = mycursor.fetchone()
    mydb.close()
    return myresult[0]

def ReadOrderIDEmployeeAccess():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = ("SELECT * FROM EmployeeAccess")
    mycursor.execute(sql_select_query)
    myresult = mycursor.fetchone()
    mydb.close()
    return myresult[1]

def DeleteEmployeeAccess():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_delete_query = ("DELETE FROM EmployeeAccess")
    mycursor.execute(sql_delete_query)
    mydb.commit()
    mydb.close()

def OpenLockersExist():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = ("SELECT * FROM Lockers Where in_use_status = %s")
    mycursor.execute(sql_select_query, ("FALSE",))
    myresult = mycursor.fetchall()
    mydb.close()
    if len(myresult) == 0:
        return False
    else:
        return True
    
def FindOpenLocker():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = ("SELECT * FROM Lockers Where in_use_status = %s")
    mycursor.execute(sql_select_query, ("FALSE",))
    myresult = mycursor.fetchone()
    mydb.close()
    return int(myresult[0])

def SetWorkingLockerID(locker_id):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_insert_query = ("INSERT INTO WorkingLocker(locker_id) VALUES (%s)")
    mycursor.execute(sql_insert_query, (locker_id,))
    mydb.commit()
    mydb.close()

def DeleteWorkingLockerID():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_delete_query = ("DELETE FROM WorkingLocker")
    mycursor.execute(sql_delete_query)
    mydb.commit()
    mydb.close()

def GetWorkingLockerID():
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = ("SELECT * FROM WorkingLocker")
    mycursor.execute(sql_select_query)
    locker_id = mycursor.fetchone()
    mydb.close()
    return int(locker_id[0])

def ChangeLockerState(locker_id, state):
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_update_query = ("UPDATE Lockers SET in_use_status = %s WHERE locker_id = %s")
    mycursor.execute(sql_update_query, (state, locker_id))
    mydb.commit()
    mydb.close()


def GetLockerID(unlock_code):
    unlock_code = int(unlock_code)
    mydb = dbConnect()
    mycursor = mydb.cursor()
    sql_select_query = ("SELECT LockID FROM OrdersStocked WHERE UnlockCode = %s")
    mycursor.execute(sql_select_query, (unlock_code,))
    locker_id = mycursor.fetchone()
    mydb.close()
    return (locker_id[0])
    
