CREATE TABLE TESTINSSPIRA.GeneralTable (
	orders_Id INT UNIQUE NOT NULL,
	orders_ClientId varchar(100) DEFAULT NULL,
	orders_RecurringOrderId varchar(100) DEFAULT NULL,
	orders_Comments TEXT DEFAULT NULL,
	orders_GrandTotal varchar(100) DEFAULT NULL,
	orders_OrderPaymentType varchar(100) DEFAULT NULL,
	orders_OrderChargeStatusType varchar(100) DEFAULT NULL,
	orders_OrderStatusType varchar(100) DEFAULT NULL,
	orders_PendingReasonType varchar(100) DEFAULT NULL,
	orders_IsArchived varchar(100) DEFAULT NULL,
	orders_OrderDate DATE DEFAULT NULL,
	orders_ModifiedAt DATE DEFAULT NULL,
	orders_OrderBundles varchar(100) DEFAULT NULL,
	orders_Discounts varchar(100) DEFAULT NULL,
	orders_ShippingTrackingMethods varchar(100) DEFAULT NULL,
	orders_ShippingTaxes varchar(100) DEFAULT NULL,
	orders_OrderedAt varchar(100) DEFAULT NULL,
	orders_BillingCyclesCharged varchar(100) DEFAULT NULL,
	orders_CustomFields TEXT DEFAULT NULL,
	items_Id INT DEFAULT NULL,
	items_OrderId INT DEFAULT NULL,
	items_ProductId INT DEFAULT NULL,
	items_Quantity INT DEFAULT NULL,
	items_ProductName varchar(100) DEFAULT NULL,
	items_ProductType varchar(100) DEFAULT NULL,
	items_UnitPrice varchar(100) DEFAULT NULL,
	items_IsRecurring varchar(100) DEFAULT NULL,
	items_IsTaxable varchar(100) DEFAULT NULL,
	items_IsCommissionable varchar(100) DEFAULT NULL,
	items_CreatedAt DATE DEFAULT NULL,
	items_ModifiedAt DATE DEFAULT NULL,
	items_SelectedOptions varchar(100) DEFAULT NULL,
	items_ProductTaxes varchar(100) DEFAULT NULL,
	items_Discounts varchar(100) DEFAULT NULL,
	items_LineItemAttributeValues TEXT DEFAULT NULL,
	clients_Id INT DEFAULT NULL,
	clients_Email varchar(100) DEFAULT NULL,
	clients_FirstName varchar(100) DEFAULT NULL,
	clients_LastName varchar(100) DEFAULT NULL,
	clients_Address1 varchar(100) DEFAULT NULL,
	clients_Address2 varchar(100) DEFAULT NULL,
	clients_City varchar(100) DEFAULT NULL,
	clients_Zip varchar(100) DEFAULT NULL,
	clients_StateName varchar(100) DEFAULT NULL,
	clients_CountryName varchar(100) DEFAULT NULL,
	clients_Phone INT DEFAULT NULL,
	clients_CreatedAt DATE DEFAULT NULL,
	clients_IsValid varchar(100) DEFAULT NULL,
	products_Id INT DEFAULT NULL,
	products_ProductName varchar(100) DEFAULT NULL,
    products_ProductPrice INT DEFAULT NULL,
    products_ShortDescription TEXT DEFAULT NULL,
    products_ProductBasedShippingCost varchar(100) DEFAULT NULL,
    products_HasShippingCalculation varchar(100) DEFAULT NULL,
    products_ProductWeight varchar(100) DEFAULT NULL,
    products_IsCommissionable varchar(100) DEFAULT NULL,
    products_IsTaxable varchar(100) DEFAULT NULL,
    products_IsFeaturedProduct varchar(100) DEFAULT NULL,
    products_ProductType varchar(100) DEFAULT NULL,
    products_IsAmemberProduct varchar(100) DEFAULT NULL,
    products_CommissionTier1 varchar(100) DEFAULT NULL,
    products_CommissionTier2 varchar(100) DEFAULT NULL,
    products_IsDiscountEnabled varchar(100) DEFAULT NULL,
    products_IsValid varchar(100) DEFAULT NULL,
    products_UseSalePrice varchar(100) DEFAULT NULL,
    products_SalePrice INT DEFAULT NULL,
    products_IsActive varchar(100) DEFAULT NULL,
    recurring_Id INT DEFAULT NULL,
    recurring_MerchantId INT DEFAULT NULL,
    recurring_OrderId INT DEFAULT NULL,
    recurring_ClientId INT DEFAULT NULL,
    recurring_ProductId INT DEFAULT NULL,
    recurring_RecurringPrice INT DEFAULT NULL,
    recurring_Quantity INT DEFAULT NULL,
    recurring_CurrentRecurring varchar(100) DEFAULT NULL,
    recurring_TotalRecurringCycles varchar(100) DEFAULT NULL,
    recurring_LastCharge DATE DEFAULT NULL,
    recurring_NextCharge DATE DEFAULT NULL,
    recurring_Status varchar(100) DEFAULT NULL,
    recurring_Attempts varchar(100) DEFAULT NULL,
    recurring_IsRetryable varchar(100) DEFAULT NULL,
    recurring_IsValid varchar(100) DEFAULT NULL,
    recurring_CreatedAt DATE DEFAULT NULL,
    recurring_DaysCycle varchar(100) DEFAULT NULL,
    recurring_IsDateBased varchar(100) DEFAULT NULL,
    recurring_MonthlyBillingDate varchar(100) DEFAULT NULL
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;