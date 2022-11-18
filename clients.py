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


parametro = {
    'key': API_KEY,
    'LimitStartDate': '2022-10-01T00:00:00',
    'LimitEndDate': '2022-10-31T00:00:00'
}
resp = requests.get(URL_ORDER_LIST,
                    params=parametro)
obj = resp.content

dictionary = xmltodict.parse(obj)

iter = dictionary['Response']['Orders']['Order']

parametro2 = {'key': API_KEY}
for x in iter:

    ord = requests.get(x['@xlink:href'], params=parametro2)

    var2 = ord.content

    dictionary2 = xmltodict.parse(var2)

    for y in dictionary2:
        C_id = dictionary2['Response']['OrderInfo']['ClientId']['@href']
        clients = requests.get(C_id, params=parametro2)
        clients2 = clients.content
        var3 = str(clients2)
        sl = slice(40, (len(var3)-1))
        var4 = var3[sl]

        try:
            conn = mysql.connector.connect(
                user='adminDB',
                port='3306',
                password='admin.1',
                host='143.244.148.34',
                database='TESTINSSPIRA'
            )
            if conn.is_connected():

                cursor = conn.cursor()

                tree = ET.ElementTree(ET.fromstring(var4))

                data2 = tree.findall('ClientInfo')

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

