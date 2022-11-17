import requests
import xmltodict
import json
# import xml element tree - para cargar xml a mysql
import xml.etree.ElementTree as ET
# import mysql connector - conexión a la DB
import mysql.connector


parametro = {
    'key': '21E09DD1C4484DEEA325DA7D554CC588',
    'LimitStartDate': '2022-10-01T00:00:00',
    'LimitEndDate': '2022-10-31T00:00:00'
}
resp = requests.get('https://www.mcssl.com/API/461142/Orders/LIST',
                    params=parametro)
obj = resp.content

# Convierte el xml a un diccionario
dictionary = xmltodict.parse(obj)
iter = dictionary['Response']['Orders']['Order']
# print(iter)

# Vamos a entrar al diccionario para hacer un reqest por cada link en el for
parametro2 = {'key': '21E09DD1C4484DEEA325DA7D554CC588'}
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
            # reading xml file , file name is file.xml
            tree = ET.ElementTree(ET.fromstring(var4))
            # in our xml file Orders is the root for all
            # Order data.
            data2 = tree.findall('OrderShippingProfileInfo')
            # retrieving the data and insert into table
            # i value for xml data #j value printing number of
            # values that are stored
            for i in data2:
                Id = i.find('Id').text
                Name = i.find('Name').text
                Address1 = i.find('Address1').text
                Address2 = i.find('Address2').text
                City = i.find('City').text
                Zip = i.find('Zip').text
                StateName = i.find('StateName').text
                CountryName = i.find('CountryName').text
                IsResidential = i.find('IsResidential').text

                # sql query to insert data into database
                data = """INSERT INTO OrderShippingProfileInfo(Id,Name,Address1,Address2,
                City,Zip,StateName,CountryName,IsResidential)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                # executing cursor object
                cursor.execute(data, (Id,Name,Address1,Address2,
                City,Zip,StateName,CountryName,IsResidential))
                conn.commit()
                print("OrderShippingProfileInfo No-", Id, " stored successfully")
            conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        if conn.is_connected():
            conn.close()
