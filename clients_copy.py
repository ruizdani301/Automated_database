import requests
import xmltodict
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import mysql.connector

load_dotenv()
API_KEY = os.getenv('API_KEY')
URL_ORDER_LIST = os.getenv('URL_ORDER_LIST')
URL_CLIENT = os.getenv('URL_CLIENT')

parametro2 = {'key': API_KEY}

parametro = {
    'key': API_KEY,
    'LimitStartDate': '2022-10-01T00:00:00',
    'LimitEndDate': '2022-10-31T00:00:00'
}

def urlList():
    
    iter = apiConsult()
   
    for x in iter:

        ord = requests.get(x['@xlink:href'], params=parametro2)

        var2 = ord.content

        dictionary2 = xmltodict.parse(var2)
        clients4 = getClient(dictionary2)
        conn = dbConnect()
        addToDataBase(conn, clients4) 
       
def apiConsult():
    resp = requests.get(URL_ORDER_LIST,
                        params=parametro)
    obj = resp.content

    dictionary = xmltodict.parse(obj)

    iter = dictionary['Response']['Orders']['Order']
    return iter

  
def getClient(dictionary2):
    for y in dictionary2:
        C_id = dictionary2['Response']['OrderInfo']['ClientId']['@href']
        clients = requests.get(C_id, params=parametro2)
        clients2 = clients.content
        clients3 = str(clients2)
        sl = slice(40, (len(clients3)-1))
        clients4 = clients3[sl]
        return clients4
def dbConnect():
        
    try:
        conn = mysql.connector.connect(
            user='adminDB',
            port='3306',
            password='admin.1',
            host='143.244.148.34',
            database='TESTINSSPIRA'
        )
    except Exception as ex:
        print(ex)
    return conn

def addToDataBase(conn, clients4):
    
    if conn.is_connected():

        cursor = conn.cursor()

        tree = ET.ElementTree(ET.fromstring(clients4))

        data2 = tree.findall('ClientInfo')
    try:
        for i in data2:
            Id = i.find('Id').text
            Email = i.find('Email').text
            FirstName = i.find('FirstName').text
            LastName = i.find('LastName').text
            Address1 = i.find('Address1').text
            Address2 = i.find('Address2').text
            City = i.find('City').text
            Zip = i.find('Zip').text
            StateName = i.find('StateName').text
            CountryName = i.find('CountryName').text
            Phone = i.find('Phone').text
            CreatedAt = i.find('CreatedAt').text
            IsValid = i.find('IsValid').text

            data = """INSERT INTO ClientInfo(Id,Email,FirstName,LastName,Address1,
            Address2,City,Zip,StateName,CountryName,Phone,CreatedAt,IsValid)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            cursor.execute(data, (Id,Email,FirstName,LastName,Address1,Address2,City,
                                Zip,StateName,CountryName,Phone,CreatedAt,IsValid))

            conn.commit()
            print("Client No-", Id, " stored successfully")
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        if conn.is_connected():
            conn.close()
urlList()