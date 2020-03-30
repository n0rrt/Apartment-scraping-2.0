from ApartmentClasses import *
from City import City
from bs4 import BeautifulSoup
import requests
import pyodbc
import pandas as pd

Philadelphia = City('Philadelphia%2C+PA', 'rx2721')
Tempe = City('Tempe%2C+AZ', 'zu85280')
Charlotte = City('Charlotte%2C+NC', 'rx2465')
Kirkland = City('Kirkland%2C+WA', 'zu98033')
Atlanta = City('Atlanta%2C+GA', 'rx394')
links = Philadelphia.getLinks() + Tempe.getLinks() + Charlotte.getLinks() + Kirkland.getLinks() + Atlanta.getLinks()

def scrapeApts():
    apts = []
    for link in links:
        r = requests.get('http:'+link)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        property = {}
        for first in soup.findAll('span', class_='first'):
            try:
                first_content = str(first.encode_contents())
                next = str(first.next_sibling.encode_contents())
                property[first_content] = next
            except:
                pass
        print('new raw', str(property))
        apts.append(property)
    return apts
def prettify():
    apts = scrapeApts()
    ad_string = "b'Ad number:'"
    count = 0
    apartments = []
    properties = []
    for apt in apts:
        ad_num = apt.get(ad_string).split("'")[1]
        apartment = Apartment(ad_num, 'status')
        print(apartment)
        apartments.append(apartment)
        print('New apartment:', apartment)
        for key in apt.keys():
            if key != ad_string:
                type = key.split("'")[1]
                value = apt.get(key).split("'")[1]
                if type == 'Price:':
                    property = ApartmentProperty(count, ad_num, type, value.split(">")[1].split("<")[0])
                elif type == 'Square\\xc2\\xa0ft:':
                    property = ApartmentProperty(count, ad_num, type.split("\\")[0] + " " + type.split("0")[1], value)
                else:
                    property = ApartmentProperty(count, ad_num, type, value)
                properties.append(property)
                print('New Property:', property)
                count += 1

    return (apartments, properties)
data = prettify()
apartments = data[0]
properties = data[1]
def startConnection():
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
cursor = startConnection()
def writeAptToDB(apartment):
    df = pd.DataFrame({'ID':apartment.getID(), 'Status':apartment.getStatus(), 'Timestamp':apartment.getTimestamp()}, index = [0])
    for index, row in df.iterrows():
        cursor.execute('''
        INSERT INTO master.dbo.Apartments (ID, Status)
        VALUES (?,?)
        ''', row['ID'], row['Status'])
        cursor.commit()
def writePropToDB(property):
    df = pd.DataFrame({'recordID':property.getRecordID(), 'aptID':property.getAptID(), 'type':property.getType(), 'value':property.getValue()}, index = [0])
    for index, row in df.iterrows():
        print(row['aptID'])
        cursor.execute('''
        INSERT INTO master.dbo.Properties (recordID, aptID, type, value)
        VALUES (?, ?, ?, ?)''', row['recordID'], row['aptID'], row['type'], row['value'])
        cursor.commit()
def validateApt(entry):
    cursor.execute('SELECT * FROM Apartments WHERE ID = (?)', entry.getID())
    rows = cursor.fetchall()
    if len(rows) == 0:
        return True
    return False
def validateProp(entry):
    cursor.execute('SELECT * FROM Properties WHERE recordID = (?)', entry.getRecordID())
    rows = cursor.fetchall()
    if len(rows) == 0:
        return True
    return False
def getOldDB():
    cursor.execute('SELECT * FROM Apartments')
    rows = cursor.fetchall()
    return rows
old = getOldDB()
def compare(entry):
    for item in old:
        if entry == item:
            return False
    return True
def write():
    for apt in apartments:
        if validateApt(apt):
            if compare(apt):
                print('New entry!')
            writeAptToDB(apt)
    for prop in properties:
        if validateProp(prop):
            writePropToDB(prop)
    cursor.close()
write()