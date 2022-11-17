import pyodbc
import ctypes, sys
import sql_dat

#Uncomment the row below to run it as Admin privileges.
#ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

#Connection informatin using SQL Login
cnxn_str = ("Driver={SQL Server};"
    "Server=localhost,1433;" #Server name and Port
    "UID=sa;" #Username
    "PWD=a1s2d3f4.;" #Password
    "Trusted_Connection=no;") #Set untouched

cnxn = pyodbc.connect(cnxn_str) #Database connected
cursor = cnxn.cursor() #Cursor of the database

while True: #Run the interface
    if not sql_dat.runUI(cursor):
        break

cursor.close()
cnxn.close()
