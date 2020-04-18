# SRS Distribution Locker System
The purpose of this application is to allow SRS Distribution to securely store ordered items so customers to pick them up at their convenience at anytime. The locker interfaces with an internal order and employee database in order to keep track of the orders stocked and notify customers their orders are stocked.
This program shall be paired with a MySQL Database and hardware components including a touchscreen, a Southco physical lock and lock controller, a barcode scanner, and a keypad entry device (usually a keyboard).

## Getting Started
Instructions to get the software up and running.

### Prerequisites
Things you need to install the software.

Tested and developed on a Raspberry Pi with the following version:
```
+-------------------------+-------------------------+
| Variable_name           | Value                   |
+-------------------------+-------------------------+
| innodb_version          | 5.7.29                  |
| protocol_version        | 10                      |
| slave_type_conversions  |                         |
| tls_version             | TLSv1,TLSv1.1,TLSv1.2   |
| version                 | 5.7.29-0ubuntu0.18.04.1 |
| version_comment         | (Ubuntu)                |
| version_compile_machine | x86_64                  |
| version_compile_os      | Linux                   |
+-------------------------+-------------------------+
```

### Installing 
Step by step instructions to get a development environment running.

Type the following commands into the Raspberry Pi terminal so Main.py can run.
```
pip3 install pyqrcode
pip3 install email
pip3 install pymysql
pip3 install mysql-connector
pip3 install mysql
sudo apt-get install python3-pymysql
sudo apt-get install python3-mysqldb
pip3 install pypng
pip3 install pyqrcode
```

To install a local mysql server type these commands in:
```
sudo apt install mariadb-server
sudo mysql_secure_installation
```
To import the srs_database.sql file type the following commands:
```
sudo mysql -u root -p srs < srs_database.sql
```

To use a MySQL database hosted on the UNT network, you will need to connect to the VPN. 
For a VPN connection on a Raspberry Pi use OpenConnect
```
sudo apt-get install openconnect network-manager-openconnect-gnome
sudo openconnect vpn.unt.edu
```
Support website for OpenConnect:
```
https://cs.uwaterloo.ca/twiki/view/CF/OpenConnect
```

For the MySQL Database, import the srs_database.sql file, or create your own tables using these commands:
```
CREATE table Orders(
	OrderID int,
	CustomerName varchar(255),
	CustomerEmail varchar(255),
	CustomerPhoneNumber BIGINT
);

CREATE TABLE ActiveUnlockCodes(
	UnlockCode int
);

CREATE table OrdersStocked(
	StockedOrderID int,
	EmployeeID int,
	OrderID int,
	UnlockCode int,
	LockID int,
	DateTimeStocked datetime
);

CREATE table ArchiveOrdersStocked(
	StockedOrderID int,
	EmployeeID int,
	OrderID int,
	UnlockCode int,
	LockID int,
	DateTimeStocked datetime,
	DateTimeRetrieved datetime
);

CREATE TABLE EmployeePins(pin INTEGER, employee_name TEXT);
CREATE TABLE EmployeeAccess(employee_id INTEGER, order_id INT);
CREATE TABLE Lockers(locker_id INTEGER, in_use_status TEXT, locked_status TEXT);
CREATE TABLE WorkingLocker(locker_id INTEGER);
```

For testing purposes:
* Change the employee pins to whatever you like.
* Insert your own email and phone number in the Orders table.
* Insert into Lockers as many locks plugged into the lock controller (up to 14) with the corresponding lock_id being '1' through '14'
```
INSERT INTO EmployeePins
VALUES ('131415', 'John Smith');
INSERT INTO EmployeePins
VALUES ('212223', 'Zach Waters');
INSERT INTO EmployeePins
VALUES ('313233', 'Jake Farms');
INSERT INTO Orders
VALUES ('10001', 'Sam Smorkle', 'EMAILHERE', 'PHONENUMBERHERE');
INSERT INTO Orders
VALUES ('10002', 'Sam Smorkle', '<EMAILHERE>', '<PHONENUMBERHERE');
INSERT INTO Lockers
VALUES ('1', 'FALSE', 'CLOSED');
```

In sql_functions.py, change the dbConnect function with your own mysql hostname, username, password, and database.
```
def dbConnect(): 
    mydb = mysql.connector.connect(
            host="localhost",
            user="locker",
            passwd="srslocker@265bs*",
            database="srs"
    )
    return mydb
```

## Deployment
Plug all of the hardware into the Raspberry Pi, the FTDI drivers should be included in the Linux kernel.
To run the program, run Main.py with sql_functions.py, email_functions.py, and lock_functions.py in the same directory.
 

## Authors
* **R. Cooper Snyder** 
* **Animesh Siwakoti** 
* **Ryan Heckmann**
* **Colton Butler**