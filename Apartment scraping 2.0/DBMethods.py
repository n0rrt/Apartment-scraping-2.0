import pyodbc
import pandas as pd
from ApartmentClasses import Apartment, ApartmentProperty
def start_connection():
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=TIM-LAPTOP\MSSQLSERVER01;'
                        'Database=master;'
                        'Trusted_Connection=True;')
        print('connection successful')
    except:
        print('connection failed')
    cursor = conn.cursor()
    return cursor
cursor = start_connection()


def write_apt_to_db(apartment):
    df = pd.DataFrame({'ID':apartment.getID(), 'Status':apartment.getStatus(), 'Timestamp':apartment.getTimestamp()}, index = [0])
    for index, row in df.iterrows():
        cursor.execute('''
        INSERT INTO master.dbo.Apartments (ID, Status)
        VALUES (?,?)
        ''', row['ID'], row['Status'])
        cursor.commit()


def write_prop_to_db(property):
    df = pd.DataFrame({'recordID':property.get_record_id(), 'aptID':property.get_apt_id(), 'type':property.get_type(), 'value':property.get_value()}, index = [0])
    for index, row in df.iterrows():
        print(row['aptID'])
        cursor.execute('''
        INSERT INTO master.dbo.Properties (recordID, aptID, type, value)
        VALUES (?, ?, ?, ?)''', row['recordID'], row['aptID'], row['type'], row['value'])
        cursor.commit()


def validate_apt(entry):
    cursor.execute('SELECT * FROM Apartments WHERE ID = (?)', entry.get_id())
    rows = cursor.fetchall()
    if len(rows) == 0:
        return True
    return False


def validate_prop(entry):
    cursor.execute('SELECT * FROM Properties WHERE aptID = (?) AND type = (?)', entry.get_apt_id(), entry.get_type())
    rows = cursor.fetchall()
    if len(rows) == 0:
        return True
    return False


def get_old_db():
    cursor.execute('SELECT * FROM Apartments')
    rows = cursor.fetchall()
    return rows


def compare(entry, old):
    for item in old:
        if entry == item:
            return False
    return True


def write(value):
    if isinstance(value, Apartment):
        if validate_apt(value):
            if compare(value, old):
                print('New entry!')
                value.setStatus('New')
            else:
                value.setStatus('Old')
            write_apt_to_db(value)
    
    elif isinstance(value, ApartmentProperty):
        if validate_prop(value):
            write_prop_to_db(value)
    else:
        print('Invalid type')
    cursor.close()
