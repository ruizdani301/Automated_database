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
    'LimitEndDate': '2022-10-02T00:00:00'
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
    
    dictionary2 = xmltodict.parse(var2)

    for y in dictionary2:
        P_id = dictionary2['Response']['OrderInfo']['LineItems']['LineItemInfo']['ProductId']['@href']

        products = requests.get(P_id, params=parametro2)
        products2 = products.content
        var3 = str(products2)
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

                data2 = tree.findall('ProductInfo')

                for i in data2:
                    Id = i.find('Id').text
                    ProductName = i.find('ProductName').text
                    ProductPrice = i.find('ProductPrice').text
                    ShortDescription = i.find('ShortDescription').text
                    ProductBasedShippingCost = i.find('ProductBasedShippingCost').text
                    HasShippingCalculation = i.find('HasShippingCalculation').text
                    ProductWeight = i.find('ProductWeight').text
                    IsCommissionable = i.find('IsCommissionable').text
                    IsTaxable = i.find('IsTaxable').text
                    IsFeaturedProduct = i.find('IsFeaturedProduct').text
                    ProductType = i.find('ProductType').text
                    IsAmemberProduct = i.find('IsAmemberProduct').text
                    CommissionTier1 = i.find('CommissionTier1').text
                    CommissionTier2 = i.find('CommissionTier2').text
                    IsDiscountEnabled = i.find('IsDiscountEnabled').text
                    IsValid = i.find('IsValid').text
                    UseSalePrice = i.find('UseSalePrice').text
                    SalePrice = i.find('SalePrice').text
                    IsActive = i.find('IsActive').text


                    data = """INSERT INTO ProductInfo(Id,ProductName,ProductPrice,ShortDescription,ProductBasedShippingCost,
                    HasShippingCalculation,ProductWeight,IsCommissionable,IsTaxable,IsFeaturedProduct,ProductType,
                    IsAmemberProduct,CommissionTier1,CommissionTier2,IsDiscountEnabled,IsValid,UseSalePrice,SalePrice,IsActive)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                    cursor.execute(data, (Id,ProductName,ProductPrice,ShortDescription,ProductBasedShippingCost,
                    HasShippingCalculation,ProductWeight,IsCommissionable,IsTaxable,IsFeaturedProduct,ProductType,
                    IsAmemberProduct,CommissionTier1,CommissionTier2,IsDiscountEnabled,IsValid,UseSalePrice,SalePrice,IsActive))

                    conn.commit()
                    print("Product No-", Id, " stored successfully")
                conn.commit()
        except Exception as ex:
            print(ex)
        finally:
            if conn.is_connected():
                conn.close()
