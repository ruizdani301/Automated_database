# Automated_database
An API is consulted and the data is transformed to automate the update of a database, a process carried out with python

- the program makes the request to the API and extracts the necessary information, as well as from each URL found in the request, inserting this information into a single table of the database, which was created on an external server.

# General.py

contains the general program, in this file the search process is unified and the insertion of information to the database.


    Example:
    for y in dictionary2:
                ri_id = dictionary2['Response']['OrderInfo']['RecurringOrderId']
                ri_id2 = str(ri_id)
                if ri_id2 == 'None':
                    print('No es recurrente')
                else:
                    parametro3 = {'key': API_KEY}
                    urlRI = '{}{}'.format(URL_RECURRING, ri_id2)

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

# tools:
mysql 3.8.1 located in Digital Ocean server
python 3.8


Create Docker file
Docker images

docker run -v /home/daniel/python/Automated_database:/app -it 94fb3cc064e8