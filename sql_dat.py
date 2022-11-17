# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 13:36:42 2022

@author: Utkucan.Genc
"""

def show_tables(cursor): #Shows the tables in the master database
    
    cmd = 'SELECT * FROM information_schema.tables ORDER BY table_name ASC;'
    
    cursor.execute(cmd)
    
    for lam,i in enumerate(list(cursor)):
        temp_arr = str(lam) + " " + " ".join(i)
        print(temp_arr)

def show_data_types(cursor, table_name) -> list: #Returns data types of columns
    cmd = f'SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = \'{table_name}\''
    cursor.execute(cmd)
    
    col_types = []
    
    for i in list(cursor):
        col_types.append(i[0])
    return col_types

def num_elems(cursor,table_name): #Returns the number of elements in the table
    
    cmd=f'SELECT COUNT(*) FROM {table_name}'
    cursor.execute(cmd)
    
    while True:
        row = cursor.fetchone()
        if not row:
            break
        print(f'{row[0]} elements are found.')
        return int(row[0])

def return_headers(cursor, table_name)-> list: #Returns column names
    cmd = f'SELECT * FROM {table_name}'
    cursor.execute(cmd)
    headers = [header[0] for header in cursor.description]
    return headers

def show_row (cursor, table_name:str,unique_id:None):
    headers = return_headers(cursor, table_name)
    if unique_id is None:
        unique_id = int(input('Please enter the unique ID of the entry: '))
    cmd = f'SELECT * FROM {table_name} WHERE {headers[0]}={unique_id}'
    cursor.execute(cmd)
    
    while True:
        row = cursor.fetchone()
        if not row:
            break
        
        elem =" ".join(map(str,list(row)))
        print(elem)
    
    
def preview_table (cursor,table_name : str): #Shows the table
    
    cmd = f'SELECT * FROM {table_name}'    
    cursor.execute(cmd)
    #Write column headers
    headers = " ".join(return_headers(cursor, table_name))
    print(headers)
    
    #Print elements of each row
    while True:
        row = cursor.fetchone()
        if not row:
            break
        
        elem =" ".join(map(str,list(row)))
        print(elem)

def del_row(cursor, table_name, del_all = False): #Deletes an entry
    if not del_all:
        unique_id = int(input('Please enter the unique ID of the entry: '))
        headers = return_headers(cursor, table_name)
        cmd = f'DELETE FROM {table_name} WHERE {headers[0]}={unique_id}'
    else:
        cmd = f'DELETE FROM {table_name}'
    cursor.execute(cmd)
    user_approval(cursor)
    

def add_row (cursor, table_name:str): #Adds a row to the table' s end
    
    num_elem = num_elems(cursor,table_name)
    dtypes = show_data_types(cursor,table_name)
    new_row = (num_elem+1,)
    
    for lam,colID in enumerate(return_headers(cursor, table_name)):
        if lam == 0:
            continue
        else:
            temp = input(f'Please enter {colID}: ')
            if dtypes[lam] == 'int':
                temp = int(temp)
            new_row += (temp,)
    print(f'The row will be inserted --> {new_row}')
    cmd = f'INSERT INTO {table_name} VALUES {new_row}'
    user_approval(cursor)
    
    print('Table is updated as following: ')
    preview_table(cursor, table_name)
    
def update_row (cursor, table_name:str): #Updates a given row   
    new_cmd = tuple()
    dtypes = show_data_types(cursor,table_name)
    headers = return_headers(cursor, table_name)
    unique_id = int(input('Please enter the unique ID of the entry: '))
    
    for lam,colID in enumerate(headers):
        colID = str(colID)
        if lam == 0:
            continue
        else:
            temp = input(f'Please enter the new {colID} (Enter blank if {colID} stays the same): ')
            if not temp == "":
                if dtypes[lam] == 'int':
                    temp = int(temp)
                if not str(temp).isnumeric():
                    new_cmd+=(colID + '=' + '\''+str(temp)+'\'',)
                else:
                    new_cmd+=(colID + '=' + str(temp),)
        print(new_cmd)
        
    print('The following row will be updated.')
    show_row(cursor, table_name, unique_id)
    new_cmd = ",".join(new_cmd)
    print(new_cmd)
    cmd = f'UPDATE {table_name} SET {new_cmd} WHERE {headers[0]}={unique_id};'
    print(cmd)
    cursor.execute(cmd)
    user_approval(cursor)
    print('Table is updated as following: ')
    preview_table(cursor, table_name)
    
def user_approval(cursor): #Check whether to save or to take backl the changes
    ratata = input('--->Proceed? (y/n): ')
    
    while True:
        if ratata =='y':
            cursor.commit()
            print('Changes are saved!!')
            break
        elif ratata =='n':
            cursor.rollback()
            print('Changes are NOT saved!!')
            break
        else:
            print('You did not enter a valid value. Try again!!')

def remove_table(cursor, table_name):
    cursor.execute(f'DROP TABLE {table_name}')
    user_approval(cursor)

def create_table(cursor):
    
    table_name = input('Enter the table name: ')
    columns = ('UniqueID int',)
    print('Enter column names. First column is reserved for UniqueID. Enter blank to terminate.')
    flag = 1
        
    while True:
        flag+=1
        temp_name = input(f'Enter the name for Column{flag}: ')
                
        if temp_name =="":
            break
        else:
            temp_name = temp_name.strip()
            temp_name = temp_name.replace(" ","")
            while True:    
                temp_dtype = input(f'Enter the data type for Column{flag}: ')
                if len(temp_dtype)<1:
                    print('Invalid datatype is entered. Try again!')
                else:
                    if temp_dtype=='0':
                        break
                    else:
                        columns += (" ".join([temp_name , temp_dtype]),)
                        break

    cmd = f'CREATE TABLE {table_name} ('
    for column in columns:
        cmd+=str(column)
        cmd+=','
    cmd=cmd[:-1]
    cmd+=')'
    cursor.execute(cmd)
    print('Table created!')
    preview_table(cursor, table_name)
    user_approval(cursor)
    return table_name

def customSQL(cursor):
    cmd = input('Please enter the custom SQL query you want to execute: ')
    cursor.execute(cmd)
    user_approval(cursor)
    
    
def runUI(cursor):
    intro_string = "\n\n\n1-Show a table\n2-Create a table\n3-Add an entry in a table\n4-Delete an entry from a table\n5-Update an entry from a table\n6-Clear a table\n7-Remove a table\n8-Show an entry\n9-Show all tables\n0-Enter a custom SQL query\n\n Enter \'q\' to exit.\n"
    table_name = ""
    print(intro_string)
    x = input('Enter your choice: ')
    while True:
        if x.isnumeric():
            x = int(x)
            if x in [1,3,4,5,6,7,8]:
                if table_name == "":
                    table_name = input(f'No table name is detected. Please enter a valid table name. Enter blank to go back: ')
                    if table_name=="":
                        runUI(cursor)
            if x == 0:
                customSQL(cursor)
            elif x==1:
                preview_table(cursor, table_name)
            elif x==2:
                table_name = create_table(cursor)
            elif x==3:
                add_row(cursor, table_name)
            elif x==4:
                del_row(cursor, table_name)
            elif x==5:
                update_row(cursor, table_name)
            elif x==6:
                del_row(cursor, table_name, True)
            elif x==7:
                remove_table(cursor, table_name)
            elif x==8:
                show_row(cursor, table_name)
            elif x==9:
                show_tables(cursor)
            runUI(cursor)
        else:
            if x=='q':
                pass
            else:
                print('Invalid choice!! Try again.')
        
    
            
            
                       
            
            