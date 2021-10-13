def create_qr_object(signature: str, account_data: dict, data: dict) -> dict:
    """[summary]
    create object for qr generating request
    Args:
        signature (str): hash for authenticate
        account_data (dict): 
            merchant_account
            merchant_domain
        data (dict):
            orderReference (str)
            orderDate (str)
            amount (str)
            currency (str)
            productName (List[str])
            productPrice (List[float])
            productCount (List[float])
            client_first_name (str)
            client_last_name (str)
            client_email (str)
            client_phone (str)

    Returns:
        dict: qr generating object
    """    
    return {
        "TRANSACTIONTYPE": "CREATE_QR",
        "MERCHANTACCOUNT": account_data['merchant_account'],
        "MERCHANTAUTHTYPE": "SIMPLESIGNATURE",
        "MERCHANTDOMAINNAME": account_data['merchant_domain'],
        "MERCHANTSIGNATURE": signature,
        "APIVERSION": 1,
        "SERVICEURL": account_data['merchant_domain'],
        "ORDERREFERENCE": data['orderReference'],
        "ORDERDATE": data['orderDate'],
        "AMOUNT": data["amount"],
        "CURRENCY": data['currency'],
        "ORDERTIMEOUT": 86400,
        "PRODUCTNAME": list(map(str, data['productName'])),
        "PRODUCTPRICE": list(map(float, data['productPrice'])),
        "PRODUCTCOUNT": list(map(float, data['productCount'])),
        "CLIENTFIRSTNAME": data['client_first_name'],
        "CLIENTLASTNAME": data['client_last_name'],
        "CLIENTEMAIL": data['client_email'],
        "CLIENTPHONE": data['client_phone']
    }
