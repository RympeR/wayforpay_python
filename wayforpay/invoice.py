def createInvoiceObject(account_data: dict, invoice_data: dict) -> dict:
    """
        example: https://wiki.wayforpay.com/view/852498
        param: account_data: dict
                merchant_account: str
                merchant_password: str
        param: invoice_data
            reqularMode -> one of [
                'once', 
                'daily',
                'weekly',
                'quartenly',
                'monthly',
                'halfyearly',
                'yearly'
            ]
            merchantPassword : str
            amount : str
            currency : str
            dateNext -> dd.mm.yyyy : str
            dateEnd -> dd.mm.yyyy : str
            orderReference -> timestamp : str
            email -> client email to notify
        return: object for invoice creation
    """
    return {
        "requestType": "CREATE",
        "merchantAccount": account_data['merchant_account'],
        "merchantPassword": account_data['merchant_password'],
        "regularMode": invoice_data['regularMode'],
        "amount": str(invoice_data['currency']),
        "currency": invoice_data['currency'],
        "dateBegin": invoice_data['dateBegin'],
        "dateEnd": invoice_data['dateEnd'],
        "orderReference": str(invoice_data['orderReference']),
        "email": invoice_data['email']
    }


def statusInvoiceObject(account_data: dict, order_reference: str) -> dict:
    """
        example: https://wiki.wayforpay.com/view/852526
        param: account_data: dict
                merchant_account: str
                merchant_password: str
        param: order_reference : str
    """
    return {
        "requestType": "STATUS",
        "merchantAccount": account_data['merchant_account'],
        "merchantPassword": account_data['merchant_password'],
        "orderReference": order_reference,
    }


def editInvoiceObject(account_data: dict, invoice_data: dict) -> dict:
    """
        example: https://wiki.wayforpay.com/view/13271051
        param: account_data: dict
                merchant_account: str
                merchant_password: str
        param: invoice_data
            reqularMode -> one of [
                'once', 
                'daily',
                'weekly',
                'quartenly',
                'monthly',
                'halfyearly',
                'yearly'
            ]
            merchantPassword : str
            amount : str
            currency : str
            dateNext -> dd.mm.yyyy : str
            dateEnd -> dd.mm.yyyy : str
            orderReference -> timestamp : str
            email -> client email to notify
        return: object for invoice creation
    """
    return {
        "requestType": "CHANGE",
        "merchantAccount": account_data['merchant_account'],
        "merchantPassword": account_data['merchant_password'],
        "regularMode": invoice_data['regularMode'],
        "amount": str(invoice_data['currency']),
        "currency": invoice_data['currency'],
        "dateBegin": invoice_data['dateBegin'],
        "dateEnd": invoice_data['dateEnd'],
        "orderReference": str(invoice_data['orderReference']),
        "email": invoice_data['email']
    }


def pauseInvoiceObject(account_data: dict, order_reference: str) -> dict:
    """
        example: https://wiki.wayforpay.com/view/852506
        param: account_data: dict
                merchant_account: str
                merchant_password: str
        param: order_reference: str
    """
    return {
        "requestType": "SUSPEND",
        "merchantAccount": account_data['merchant_account'],
        "merchantPassword": account_data['merchant_password'],
        "orderReference": order_reference,
    }


def resumeInvoiceObject(account_data: dict, order_reference: str) -> dict:
    """
        example: https://wiki.wayforpay.com/view/852513
        param: account_data: dict
                merchant_account: str
                merchant_password: str
        param: order_reference: str
    """
    return {
        "requestType": "RESUME",
        "merchantAccount": account_data['merchant_account'],
        "merchantPassword": account_data['merchant_password'],
        "orderReference": order_reference,
    }


def removeInvoiceObject(account_data: dict, order_reference: str) -> dict:
    """
        example: https://wiki.wayforpay.com/view/852521
        param: account_data: dict
                merchant_account: str
                merchant_password: str
        param: order_reference: str
    """
    return {
        "requestType": "REMOVE",
        "merchantAccount": account_data['merchant_account'],
        "merchantPassword": account_data['merchant_password'],
        "orderReference": order_reference,
    }
