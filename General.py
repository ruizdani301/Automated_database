import requests
import xmltodict
import os
import xml.etree.ElementTree as ET
import mysql.connector
from dotenv import load_dotenv
from datetime import date
from datetime import timedelta

load_dotenv()
API_KEY = os.getenv('API_KEY')
URL_ORDER_LIST = os.getenv('URL_ORDER_LIST')
URL_RECURRING = os.getenv('URL_RECURRING')

today = date.today() 
yesterday = today - timedelta(days = 1)
LimitStartDate = str(yesterday) + ' 00:00:00.000000'

# Para consultar fechas especificas agregar a parametros el rango de fechas:
# 'LimitStartDate': '2022-10-01T00:00:00',
# 'LimitEndDate': '2022-10-02T00:00:00'

parametro = {
    'key': API_KEY,
    'LimitStartDate': LimitStartDate,
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
                orders_Id = i.find('Id').text
                orders_ClientId = i.find('ClientId').text
                orders_RecurringOrderId = i.find('RecurringOrderId').text
                orders_Comments = i.find('Comments').text
                orders_GrandTotal = i.find('GrandTotal').text
                orders_OrderPaymentType = i.find('OrderPaymentType').text
                orders_OrderChargeStatusType = i.find('OrderChargeStatusType').text
                orders_OrderStatusType = i.find('OrderChargeStatusType').text
                orders_PendingReasonType = i.find('PendingReasonType').text
                orders_IsArchived = i.find('IsArchived').text
                orders_OrderDate = i.find('OrderDate').text
                orders_ModifiedAt = i.find('ModifiedAt').text
                orders_OrderBundles = i.find('OrderBundles').text
                orders_Discounts = i.find('Discounts').text
                orders_ShippingTrackingMethods = i.find('ShippingTrackingMethods').text
                orders_ShippingTaxes = i.find('ShippingTaxes').text
                orders_OrderedAt = i.find('OrderedAt').text
                orders_BillingCyclesCharged = i.find('BillingCyclesCharged').text
                orders_CustomFields = i.find('CustomFields').text

        #Items

            items = tree.findall('.//OrderInfo/LineItems/LineItemInfo')
            # retrieving the data and insert into table
            # i value for xml data #j value printing number of
            # values that are stored
            for i in items:
                items_Id = i.find('Id').text
                items_OrderId = i.find('OrderId').text
                items_ProductId = i.find('ProductId').text
                items_Quantity = i.find('Quantity').text
                items_ProductName = i.find('ProductName').text
                items_ProductType = i.find('ProductType').text
                items_UnitPrice = i.find('UnitPrice').text
                items_IsRecurring = i.find('IsRecurring').text
                items_IsTaxable = i.find('IsTaxable').text
                items_IsCommissionable = i.find('IsCommissionable').text
                items_CreatedAt = i.find('CreatedAt').text
                items_ModifiedAt = i.find('ModifiedAt').text
                items_SelectedOptions = i.find('SelectedOptions').text
                items_ProductTaxes = i.find('ProductTaxes').text
                items_Discounts = i.find('Discounts').text
                items_LineItemAttributeValues = i.find('LineItemAttributeValues').text

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
                    clients_Id = i.find('Id').text
                    clients_Email = i.find('Email').text
                    clients_FirstName = i.find('FirstName').text
                    clients_LastName = i.find('LastName').text
                    clients_Address1 = i.find('Address1').text
                    clients_Address2 = i.find('Address2').text
                    clients_City = i.find('City').text
                    clients_Zip = i.find('Zip').text
                    clients_StateName = i.find('StateName').text
                    clients_CountryName = i.find('CountryName').text
                    clients_Phone = i.find('Phone').text
                    clients_CreatedAt = i.find('CreatedAt').text
                    clients_IsValid = i.find('IsValid').text

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
                    products_Id = i.find('Id').text
                    products_ProductName = i.find('ProductName').text
                    products_ProductPrice = i.find('ProductPrice').text
                    products_ShortDescription = i.find('ShortDescription').text
                    products_ProductBasedShippingCost = i.find('ProductBasedShippingCost').text
                    products_HasShippingCalculation = i.find('HasShippingCalculation').text
                    products_ProductWeight = i.find('ProductWeight').text
                    products_IsCommissionable = i.find('IsCommissionable').text
                    products_IsTaxable = i.find('IsTaxable').text
                    products_IsFeaturedProduct = i.find('IsFeaturedProduct').text
                    products_ProductType = i.find('ProductType').text
                    products_IsAmemberProduct = i.find('IsAmemberProduct').text
                    products_CommissionTier1 = i.find('CommissionTier1').text
                    products_CommissionTier2 = i.find('CommissionTier2').text
                    products_IsDiscountEnabled = i.find('IsDiscountEnabled').text
                    products_IsValid = i.find('IsValid').text
                    products_UseSalePrice = i.find('UseSalePrice').text
                    products_SalePrice = i.find('SalePrice').text
                    products_IsActive = i.find('IsActive').text

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
                        recurring_Id = i.find('Id').text
                        recurring_MerchantId = i.find('MerchantId').text
                        recurring_OrderId = i.find('OrderId').text
                        recurring_ClientId = i.find('ClientId').text
                        recurring_ProductId = i.find('ProductId').text
                        recurring_RecurringPrice = i.find('RecurringPrice').text
                        recurring_Quantity = i.find('Quantity').text
                        recurring_CurrentRecurring = i.find('CurrentRecurring').text
                        recurring_TotalRecurringCycles = i.find(
                            'TotalRecurringCycles').text
                        recurring_LastCharge = i.find('LastCharge').text
                        recurring_NextCharge = i.find('NextCharge').text
                        recurring_Status = i.find('Status').text
                        recurring_Attempts = i.find('Attempts').text
                        recurring_IsRetryable = i.find('IsRetryable').text
                        recurring_IsValid = i.find('IsValid').text
                        recurring_CreatedAt = i.find('CreatedAt').text
                        recurring_DaysCycle = i.find('DaysCycle').text
                        recurring_IsDateBased = i.find('IsDateBased').text
                        recurring_MonthlyBillingDate = i.find('MonthlyBillingDate').text

                        General_data = """INSERT INTO GeneralTable(orders_Id,orders_ClientId,orders_RecurringOrderId,orders_Comments,orders_GrandTotal,orders_OrderPaymentType,
                        orders_OrderChargeStatusType,orders_OrderStatusType,orders_PendingReasonType,orders_IsArchived,orders_OrderDate,orders_ModifiedAt,orders_OrderBundles,
                        orders_Discounts,orders_ShippingTrackingMethods,orders_ShippingTaxes,orders_OrderedAt,orders_BillingCyclesCharged,orders_CustomFields,
                        items_Id,items_OrderId,items_ProductId,items_Quantity,items_ProductName,
                        items_ProductType,items_UnitPrice,items_IsRecurring,items_IsTaxable,items_IsCommissionable,items_CreatedAt,
                        items_ModifiedAt,items_SelectedOptions,items_ProductTaxes,items_Discounts,items_LineItemAttributeValues,clients_Id,clients_Email,clients_FirstName,clients_LastName,
                        clients_Address1,clients_Address2,clients_City,clients_Zip,clients_StateName,clients_CountryName,clients_Phone,clients_CreatedAt,clients_IsValid,
                        products_Id,products_ProductName,products_ProductPrice,products_ShortDescription,products_ProductBasedShippingCost,
                        products_HasShippingCalculation,products_ProductWeight,products_IsCommissionable,products_IsTaxable,products_IsFeaturedProduct,products_ProductType,
                        products_IsAmemberProduct,products_CommissionTier1,products_CommissionTier2,products_IsDiscountEnabled,products_IsValid,products_UseSalePrice,products_SalePrice,products_IsActive,
                        recurring_Id, recurring_MerchantId, recurring_OrderId, recurring_ClientId, recurring_ProductId, recurring_RecurringPrice, recurring_Quantity,
                        recurring_CurrentRecurring, recurring_TotalRecurringCycles, recurring_LastCharge, recurring_NextCharge, recurring_Status, recurring_Attempts, recurring_IsRetryable, recurring_IsValid,
                        recurring_CreatedAt, recurring_DaysCycle, recurring_IsDateBased, recurring_MonthlyBillingDate)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s)"""

                        cursor.execute(General_data, (orders_Id,orders_ClientId,orders_RecurringOrderId,orders_Comments,orders_GrandTotal,orders_OrderPaymentType,
                        orders_OrderChargeStatusType,orders_OrderStatusType,orders_PendingReasonType,orders_IsArchived,orders_OrderDate,orders_ModifiedAt,orders_OrderBundles,
                        orders_Discounts,orders_ShippingTrackingMethods,orders_ShippingTaxes,orders_OrderedAt,orders_BillingCyclesCharged,orders_CustomFields,
                        items_Id,items_OrderId,items_ProductId,items_Quantity,items_ProductName,
                        items_ProductType,items_UnitPrice,items_IsRecurring,items_IsTaxable,items_IsCommissionable,items_CreatedAt,
                        items_ModifiedAt,items_SelectedOptions,items_ProductTaxes,items_Discounts,items_LineItemAttributeValues,clients_Id,clients_Email,clients_FirstName,clients_LastName,
                        clients_Address1,clients_Address2,clients_City,clients_Zip,clients_StateName,clients_CountryName,clients_Phone,clients_CreatedAt,clients_IsValid,
                        products_Id,products_ProductName,products_ProductPrice,products_ShortDescription,products_ProductBasedShippingCost,
                        products_HasShippingCalculation,products_ProductWeight,products_IsCommissionable,products_IsTaxable,products_IsFeaturedProduct,products_ProductType,
                        products_IsAmemberProduct,products_CommissionTier1,products_CommissionTier2,products_IsDiscountEnabled,products_IsValid,products_UseSalePrice,products_SalePrice,products_IsActive,
                        recurring_Id, recurring_MerchantId, recurring_OrderId, recurring_ClientId, recurring_ProductId, recurring_RecurringPrice, recurring_Quantity,
                        recurring_CurrentRecurring, recurring_TotalRecurringCycles, recurring_LastCharge, recurring_NextCharge, recurring_Status, recurring_Attempts, recurring_IsRetryable, recurring_IsValid,
                        recurring_CreatedAt, recurring_DaysCycle, recurring_IsDateBased, recurring_MonthlyBillingDate))

                        conn.commit()
                        print("Orders No-", orders_Id, " stored successfully")
                        print("Item No-", items_Id, " stored successfully")
                        print("Client No-", clients_Id, " stored successfully")
                        print("Product No-", products_Id, " stored successfully")
                        print("Recurring Order No-", recurring_Id, " stored successfully")
            conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        if conn.is_connected():
            conn.close()
