import requests
import xmltodict
import os
import xml.etree.ElementTree as ET
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
URL_ORDER_LIST = os.getenv('URL_ORDER_LIST')
URL_RECURRING = os.getenv('URL_RECURRING')


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
        
        # Order data

            orders = tree.findall('OrderInfo')
            # retrieving the data and insert into table
            # i value for xml data #j value printing number of
            # values that are stored
            for i in orders:
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

                # sql query to insert data into database
                orders_data = """INSERT INTO Orders_1(Id,ClientId,RecurringOrderId,Comments,GrandTotal,OrderPaymentType,
                OrderChargeStatusType,OrderStatusType,PendingReasonType,IsArchived,OrderDate,ModifiedAt,OrderBundles,
                Discounts,ShippingTrackingMethods,ShippingTaxes,OrderedAt,BillingCyclesCharged,CustomFields)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                # executing cursor object
                cursor.execute(orders_data, (Id,ClientId,RecurringOrderId,Comments,GrandTotal,OrderPaymentType,
                OrderChargeStatusType,OrderStatusType,PendingReasonType,IsArchived,OrderDate,ModifiedAt,OrderBundles,
                Discounts,ShippingTrackingMethods,ShippingTaxes,OrderedAt,BillingCyclesCharged,CustomFields))
                conn.commit()
                print("Orders No-", Id, " stored successfully")

        #Items

            items = tree.findall('.//OrderInfo/LineItems/LineItemInfo')
            # retrieving the data and insert into table
            # i value for xml data #j value printing number of
            # values that are stored
            for i in items:
                Id = i.find('Id').text
                OrderId = i.find('OrderId').text
                ProductId = i.find('ProductId').text
                Quantity = i.find('Quantity').text
                ProductName = i.find('ProductName').text
                ProductType = i.find('ProductType').text
                UnitPrice = i.find('UnitPrice').text
                IsRecurring = i.find('IsRecurring').text
                IsTaxable = i.find('IsTaxable').text
                IsCommissionable = i.find('IsCommissionable').text
                CreatedAt = i.find('CreatedAt').text
                ModifiedAt = i.find('ModifiedAt').text
                SelectedOptions = i.find('SelectedOptions').text
                ProductTaxes = i.find('ProductTaxes').text
                Discounts = i.find('Discounts').text
                LineItemAttributeValues = i.find('LineItemAttributeValues').text


                # sql query to insert data into database
                items_data = """INSERT INTO ItemsInfo(Id,OrderId,ProductId,Quantity,ProductName,
                ProductType,UnitPrice,IsRecurring,IsTaxable,IsCommissionable,CreatedAt,
                ModifiedAt,SelectedOptions,ProductTaxes,Discounts,LineItemAttributeValues)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                # creating the cursor object

                # executing cursor object
                cursor.execute(items_data, (Id,OrderId,ProductId,Quantity,ProductName,
                ProductType,UnitPrice,IsRecurring,IsTaxable,IsCommissionable,CreatedAt,
                ModifiedAt,SelectedOptions,ProductTaxes,Discounts,LineItemAttributeValues))
                conn.commit()
                print("Item No-", Id, " stored successfully")

        # Clients

            dictionary2 = xmltodict.parse(var2)

            for y in dictionary2:
                C_id = dictionary2['Response']['OrderInfo']['ClientId']['@href']
                clients = requests.get(C_id, params=parametro2)
                clients2 = clients.content
                clients3 = str(clients2)
                sl = slice(40, (len(clients3)-1))
                clients4 = clients3[sl]

                tree = ET.ElementTree(ET.fromstring(clients4))

                clients5 = tree.findall('ClientInfo')

                for i in clients5:
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

                    clients_data = """INSERT INTO ClientInfo(Id,Email,FirstName,LastName,Address1,
                    Address2,City,Zip,StateName,CountryName,Phone,CreatedAt,IsValid)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                    cursor.execute(clients_data, (Id,Email,FirstName,LastName,Address1,Address2,City,
                                          Zip,StateName,CountryName,Phone,CreatedAt,IsValid))

                    conn.commit()
                    print("Client No-", Id, " stored successfully")

        # Products

            for y in dictionary2:
                P_id = dictionary2['Response']['OrderInfo']['LineItems']['LineItemInfo']['ProductId']['@href']

                products = requests.get(P_id, params=parametro2)
                products2 = products.content
                products3 = str(products2)
                sl = slice(40, (len(products3)-1))
                products4 = products3[sl]

                tree = ET.ElementTree(ET.fromstring(products4))

                products5 = tree.findall('ProductInfo')

                for i in products5:
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


                    products_data = """INSERT INTO ProductInfo(Id,ProductName,ProductPrice,ShortDescription,ProductBasedShippingCost,
                    HasShippingCalculation,ProductWeight,IsCommissionable,IsTaxable,IsFeaturedProduct,ProductType,
                    IsAmemberProduct,CommissionTier1,CommissionTier2,IsDiscountEnabled,IsValid,UseSalePrice,SalePrice,IsActive)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                    cursor.execute(products_data, (Id,ProductName,ProductPrice,ShortDescription,ProductBasedShippingCost,
                    HasShippingCalculation,ProductWeight,IsCommissionable,IsTaxable,IsFeaturedProduct,ProductType,
                    IsAmemberProduct,CommissionTier1,CommissionTier2,IsDiscountEnabled,IsValid,UseSalePrice,SalePrice,IsActive))

                    conn.commit()
                    print("Product No-", Id, " stored successfully")

        # Recurring Orders
            for y in dictionary2:
                ri_id = dictionary2['Response']['OrderInfo']['RecurringOrderId']
                # print(type(ri_id))
                ri_id2 = str(ri_id)
                if ri_id2 == 'None':
                    print('No es recurrente')
                else:
                    parametro3 = {'key': API_KEY}
                    urlRI = URL_RECURRING + ri_id2

                    ri = requests.get(urlRI, params=parametro3)
                    # print(ri)
                    ri_content = ri.content
                    ri3 = str(ri_content)
                    sl = slice(40, (len(ri3)-1))
                    ri4 = ri3[sl]

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

            conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        if conn.is_connected():
            conn.close()
