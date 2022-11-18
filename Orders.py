import requests
import xmltodict
import json
import os
# import xml element tree - para cargar xml a mysql
import xml.etree.ElementTree as ET
# import mysql connector - conexión a la DB
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
URL_ORDER_LIST = os.getenv('URL_ORDER_LIST')


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
# # print(dictionary)

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
    # Convierto la variable en un str
    var3 = str(var2)
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
            # Ingresar codigo a mysql aquí

            # reading xml file , file name is file.xml
            tree = ET.ElementTree(ET.fromstring(var4))
            # in our xml file Orders is the root for all
            # Order data.
            data2 = tree.findall('OrderInfo')
            # retrieving the data and insert into table
            # i value for xml data #j value printing number of
            # values that are stored
            for i in data2:
                Id = i.find('Id').text
                ClientId = i.find('ClientId').text
                RecurringOrderId = i.find('RecurringOrderId').text
                Comments = i.find('Comments').text
                GrandTotal = i.find('GrandTotal').text
                OrderPaymentType = i.find('OrderPaymentType').text
                OrderChargeStatusType = i.find('OrderChargeStatusType').text
                OrderStatusType = i.find('OrderChargeStatusType').text
                PendingReasonType = i.find('PendingReasonType').text
                IsArchived = i.find('IsArchived').text
                OrderDate = i.find('OrderDate').text
                ModifiedAt = i.find('ModifiedAt').text
                OrderBundles = i.find('OrderBundles').text
                Discounts = i.find('Discounts').text
                ShippingTrackingMethods = i.find('ShippingTrackingMethods').text
                ShippingTaxes = i.find('ShippingTaxes').text
                OrderedAt = i.find('OrderedAt').text
                BillingCyclesCharged = i.find('BillingCyclesCharged').text
                CustomFields = i.find('CustomFields').text

            #     # sql query to insert data into database
                data = """INSERT INTO Orders_1(Id,ClientId,RecurringOrderId,Comments,GrandTotal,OrderPaymentType,
                OrderChargeStatusType,OrderStatusType,PendingReasonType,IsArchived,OrderDate,ModifiedAt,OrderBundles,
                Discounts,ShippingTrackingMethods,ShippingTaxes,OrderedAt,BillingCyclesCharged,CustomFields)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                # executing cursor object
                cursor.execute(data, (Id,ClientId,RecurringOrderId,Comments,GrandTotal,OrderPaymentType,
                OrderChargeStatusType,OrderStatusType,PendingReasonType,IsArchived,OrderDate,ModifiedAt,OrderBundles,
                Discounts,ShippingTrackingMethods,ShippingTaxes,OrderedAt,BillingCyclesCharged,CustomFields))
                conn.commit()
                print("Orders No-", Id, " stored successfully")
            conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        if conn.is_connected():
            conn.close()
