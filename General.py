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
dictionary = xmltodict.parse(obj)
iter = dictionary['Response']['Orders']['Order']
parameter_key = {'key': API_KEY}
for value in iter:
    # Agregar metodos de error o try catch
    # Realizo un Request por cada linea de iter donde la URL esta en la clave: @xlink:href
    request_content = requests.get(value['@xlink:href'], params=parameter_key)
    content = request_content.content
    content = str(content)
    new_key = slice(40, (len(content)-1))
    var_content = content[new_key]

    try:
        conn = mysql.connector.connect(
            user=os.getenv('US'),
            port=os.getenv('PORT'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            database=os.getenv('DATABASE')
        )
        if conn.is_connected():

            cursor = conn.cursor()
            # reading xml file , file name is file.xml
            tree = ET.ElementTree(ET.fromstring(var_content))
            # in our xml file Orders is the root for all
        
            """ Order data """

            orders = tree.findall('OrderInfo')
            # retrieving the data and insert into table
            # order value for xml data 
            for order in orders:
                orders_Id = order.find('Id').text
                orders_ClientId = order.find('ClientId').text
                orders_RecurringOrderId = order.find('RecurringOrderId').text
                orders_Comments = order.find('Comments').text
                orders_GrandTotal = order.find('GrandTotal').text
                orders_OrderPaymentType = order.find('OrderPaymentType').text
                orders_OrderChargeStatusType = order.find('OrderChargeStatusType').text
                orders_OrderStatusType = order.find('OrderChargeStatusType').text
                orders_PendingReasonType = order.find('PendingReasonType').text
                orders_IsArchived = order.find('IsArchived').text
                orders_OrderDate = order.find('OrderDate').text
                orders_ModifiedAt = order.find('ModifiedAt').text
                orders_OrderBundles = order.find('OrderBundles').text
                orders_Discounts = order.find('Discounts').text
                orders_ShippingTrackingMethods = order.find('ShippingTrackingMethods').text
                orders_ShippingTaxes = order.find('ShippingTaxes').text
                orders_OrderedAt = order.find('OrderedAt').text
                orders_BillingCyclesCharged = order.find('BillingCyclesCharged').text
                orders_CustomFields = order.find('CustomFields').text

            """ Items data """

            items = tree.findall('.//OrderInfo/LineItems/LineItemInfo')
            # retrieving the data and insert into table
            # item value for xml data
            for item in items:
                items_Id = item.find('Id').text
                items_OrderId = item.find('OrderId').text
                items_ProductId = item.find('ProductId').text
                items_Quantity = item.find('Quantity').text
                items_ProductName = item.find('ProductName').text
                items_ProductType = item.find('ProductType').text
                items_UnitPrice = item.find('UnitPrice').text
                items_IsRecurring = item.find('IsRecurring').text
                items_IsTaxable = item.find('IsTaxable').text
                items_IsCommissionable = item.find('IsCommissionable').text
                items_CreatedAt = item.find('CreatedAt').text
                items_ModifiedAt = item.find('ModifiedAt').text
                items_SelectedOptions = item.find('SelectedOptions').text
                items_ProductTaxes = item.find('ProductTaxes').text
                items_Discounts = item.find('Discounts').text
                items_LineItemAttributeValues = item.find('LineItemAttributeValues').text

            """ Clients data """

            dictionary2 = xmltodict.parse(content)

            for value in dictionary2:
                client_id = dictionary2['Response']['OrderInfo']['ClientId']['@href']
                clients = requests.get(client_id, params=parameter_key)
                clients2 = clients.content
                clients3 = str(clients2)
                new_key = slice(40, (len(clients3)-1))
                clients4 = clients3[new_key]

                tree = ET.ElementTree(ET.fromstring(clients4))

                data_client = tree.findall('ClientInfo')

                for client in data_client:
                    clients_Id = client.find('Id').text
                    clients_Email = client.find('Email').text
                    clients_FirstName = client.find('FirstName').text
                    clients_LastName = client.find('LastName').text
                    clients_Address1 = client.find('Address1').text
                    clients_Address2 = client.find('Address2').text
                    clients_City = client.find('City').text
                    clients_Zip = client.find('Zip').text
                    clients_StateName = client.find('StateName').text
                    clients_CountryName = client.find('CountryName').text
                    clients_Phone = client.find('Phone').text
                    clients_CreatedAt = client.find('CreatedAt').text
                    clients_IsValid = client.find('IsValid').text

            """ Products data """

            for value in dictionary2:
                product_id = dictionary2['Response']['OrderInfo']['LineItems']['LineItemInfo']['ProductId']['@href']

                products = requests.get(product_id, params=parameter_key)
                products2 = products.content
                products3 = str(products2)
                new_key = slice(40, (len(products3)-1))
                products4 = products3[new_key]

                tree = ET.ElementTree(ET.fromstring(products4))

                products5 = tree.findall('ProductInfo')

                for product in products5:
                    products_Id = product.find('Id').text
                    products_ProductName = product.find('ProductName').text
                    products_ProductPrice = product.find('ProductPrice').text
                    products_ShortDescription = product.find('ShortDescription').text
                    products_ProductBasedShippingCost = product.find('ProductBasedShippingCost').text
                    products_HasShippingCalculation = product.find('HasShippingCalculation').text
                    products_ProductWeight = product.find('ProductWeight').text
                    products_IsCommissionable = product.find('IsCommissionable').text
                    products_IsTaxable = product.find('IsTaxable').text
                    products_IsFeaturedProduct = product.find('IsFeaturedProduct').text
                    products_ProductType = product.find('ProductType').text
                    products_IsAmemberProduct = product.find('IsAmemberProduct').text
                    products_CommissionTier1 = product.find('CommissionTier1').text
                    products_CommissionTier2 = product.find('CommissionTier2').text
                    products_IsDiscountEnabled = product.find('IsDiscountEnabled').text
                    products_IsValid = product.find('IsValid').text
                    products_UseSalePrice = product.find('UseSalePrice').text
                    products_SalePrice = product.find('SalePrice').text
                    products_IsActive = product.find('IsActive').text

            """ Recurring Orders data """

            for value in dictionary2:
                recurring_id = dictionary2['Response']['OrderInfo']['RecurringOrderId']
                recurring_id = str(recurring_id)
                if recurring_id == 'None':
                    print('No es recurrente')
                else:
                    parameter_key = {'key': API_KEY}
                    urlRI = '{}{}'.format(URL_RECURRING, recurring_id)

                    recurring = requests.get(urlRI, params=parameter_key)
                    recurring_content = recurring.content
                    r_content = str(recurring_content)
                    new_key = slice(40, (len(r_content)-1))
                    data_recurring = r_content[new_key]

                    tree = ET.ElementTree(ET.fromstring(data_recurring))
                    # in our xml file Orders is the root for all
                    # Order data.
                    recurring = tree.findall('RecurringOrderInfo')
                    for recurrence in recurring:
                        recurring_Id = recurrence.find('Id').text
                        recurring_MerchantId = recurrence.find('MerchantId').text
                        recurring_OrderId = recurrence.find('OrderId').text
                        recurring_ClientId = recurrence.find('ClientId').text
                        recurring_ProductId = recurrence.find('ProductId').text
                        recurring_RecurringPrice = recurrence.find('RecurringPrice').text
                        recurring_Quantity = recurrence.find('Quantity').text
                        recurring_CurrentRecurring = recurrence.find('CurrentRecurring').text
                        recurring_TotalRecurringCycles = recurrence.find(
                            'TotalRecurringCycles').text
                        recurring_LastCharge = recurrence.find('LastCharge').text
                        recurring_NextCharge = recurrence.find('NextCharge').text
                        recurring_Status = recurrence.find('Status').text
                        recurring_Attempts = recurrence.find('Attempts').text
                        recurring_IsRetryable = recurrence.find('IsRetryable').text
                        recurring_IsValid = recurrence.find('IsValid').text
                        recurring_CreatedAt = recurrence.find('CreatedAt').text
                        recurring_DaysCycle = recurrence.find('DaysCycle').text
                        recurring_IsDateBased = recurrence.find('IsDateBased').text
                        recurring_MonthlyBillingDate = recurrence.find('MonthlyBillingDate').text

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
                    """
                        print("Item No-", items_Id, " stored successfully")
                        print("Client No-", clients_Id, " stored successfully")
                        print("Product No-", products_Id, " stored successfully")
                        print("Recurring Order No-", recurring_Id, " stored successfully")
                    """
            conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        if conn.is_connected():
            conn.close()
