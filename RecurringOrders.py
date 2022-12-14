import requests
import xmltodict
import json
import os
from dotenv import load_dotenv
# import xml element tree - para cargar xml a mysql
import xml.etree.ElementTree as ET
# import mysql connector - conexión a la DB
import mysql.connector

load_dotenv()
API_KEY = os.getenv('API_KEY')
URL_ORDER_LIST = os.getenv('URL_ORDER_LIST')
URL_RECURRING = os.getenv('URL_RECURRING')


parametro = {
    'key': API_KEY,
    'LimitStartDate': '2022-10-01T00:00:00',
    'LimitEndDate': '2022-10-31T00:00:00'
}
resp = requests.get(URL_ORDER_LIST,
                    params=parametro)
obj = resp.content

# Convierte el xml a un diccionario
dictionary = xmltodict.parse(obj)

# Entramos al arreglo de ordenes
iter = dictionary['Response']['Orders']['Order']
# print(iter)

# Vamos a entrar al diccionario para hacer un reqest por cada link en el for
parametro2 = {'key': API_KEY}
for x in iter:
    #     # Agregar metodos de error o try catch
    # Realizo un Request por cada linea de iter donde la URL esta en la clave: @xlink:href
    ord = requests.get(x['@xlink:href'], params=parametro2)
    # Leo el contenido del request y lo almaceno en una variable
    var2 = ord.content

    ''' Codigo para cargar las Recurring Orders, trae la información por Order Id
    y debe buscar el Recurrent Order Id para hacer el request'''

    dictionary2 = xmltodict.parse(var2)

    for y in dictionary2:
        ri_id = dictionary2['Response']['OrderInfo']['RecurringOrderId']
        # print(type(ri_id))
        ri_id2 = str(ri_id)
        if ri_id2 == 'None':
            print('No es recurrente')
        else:
            parametro3 = {'key': API_KEY}
            urlRI = URL_RECURRING + ri_id2
            # print(urlRI)
            
            ri = requests.get(urlRI, params=parametro3)
            # print(ri)
            ri_content = ri.content
            ri3 = str(ri_content)
            sl = slice(40, (len(ri3)-1))
            ri4 = ri3[sl]
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
                    # reading xml file , file name is file.xml
                    tree = ET.ElementTree(ET.fromstring(ri4))
                    # in our xml file Orders is the root for all
                    # Order data.
                    recurring = tree.findall('RecurringOrderInfo')
                    for i in recurring:
                        Id = i.find('Id').text
                        MerchantId = i.find('MerchantId').text
                        OrderId = i.find('OrderId').text
                        ClientId = i.find('ClientId').text
                        ProductId = i.find('ProductId').text
                        RecurringPrice = i.find('RecurringPrice').text
                        Quantity = i.find('Quantity').text
                        CurrentRecurring = i.find('CurrentRecurring').text
                        TotalRecurringCycles = i.find(
                            'TotalRecurringCycles').text
                        LastCharge = i.find('LastCharge').text
                        NextCharge = i.find('NextCharge').text
                        Status = i.find('Status').text
                        Attempts = i.find('Attempts').text
                        IsRetryable = i.find('IsRetryable').text
                        IsValid = i.find('IsValid').text
                        CreatedAt = i.find('CreatedAt').text
                        DaysCycle = i.find('DaysCycle').text
                        IsDateBased = i.find('IsDateBased').text
                        MonthlyBillingDate = i.find('MonthlyBillingDate').text

                        # sql query to insert data into database
                recurring_data = """INSERT INTO RecurringOrders(Id,MerchantId,OrderId,ClientId,ProductId,RecurringPrice,Quantity,
                CurrentRecurring,TotalRecurringCycles,LastCharge,NextCharge,Status,Attempts,IsRetryable,IsValid,
                CreatedAt,DaysCycle,IsDateBased,MonthlyBillingDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s)"""

                # executing cursor object
                cursor.execute(recurring_data, (Id, MerchantId, OrderId, ClientId, ProductId, RecurringPrice, Quantity,
                                      CurrentRecurring, TotalRecurringCycles, LastCharge, NextCharge, Status, Attempts, IsRetryable, IsValid,
                                      CreatedAt, DaysCycle, IsDateBased, MonthlyBillingDate))
                conn.commit()
                print("Recurring Order No-", Id, " stored successfully")
            # Aquí termina la inserción a la DB
            except Exception as ex:
                print(ex)
            finally:
                if conn.is_connected():
                    conn.close()
