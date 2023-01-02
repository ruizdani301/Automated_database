# Automated_database
An API is consulted and the data is transformed to automate the update of a database, a process carried out with python

- the program makes the request to the API and extracts the necessary information, as well as from each URL found in the request, inserting this information into a single table of the database, which was created on an external server.

# General.py

contains the general program, in this file the search process is unified and the insertion of information to the database.


### Example:

   for value in iter:
    
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

# tools:
mysql 3.8.1 located in Digital Ocean server
python 3.8


Create Docker file
Docker images

docker run -v /home/daniel/python/Automated_database:/app -it 94fb3cc064e8
