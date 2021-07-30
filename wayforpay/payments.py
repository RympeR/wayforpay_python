def generateWidgetObject(signature: str, account_data: dict, data: dict) -> str:
    return {
        'merchantAccount': account_data['merchant_account'],
        'merchantDomainName': account_data['merchant_domain'],
        'merchantTransactionType': 'AUTO',
        'merchantTransactionSecureType': 'AUTO',
        'orderReference': data['orderReference'],
        'orderDate': data['orderDate'],
        'amount': data["amount"],
        'authorizationType': 'SimpleSignature',
        'currency': data['currency'],
        'productName':   list(map(str, data['productName'])),
        'productPrice':  list(map(str, data['productPrice'])),
        'productCount':  list(map(str, data['productCount'])),
        'merchantSignature': signature,
        'language': data['language'],
        'straightWidget': data['straightWidget']
    }


def generateWidgetScript(signature: str, account_data: dict, data: dict) -> str:
    request_form = r"""
        <script type="text/javascript"> 
        function pay(){
            var payment = new Wayforpay();
                payment.run({""" + f"""
                    merchantAccount: '{account_data['merchant_account']}',
                    merchantDomainName: '{account_data['merchant_domain']}',
                    merchantTransactionType: 'AUTO',
                    merchantTransactionSecureType: 'AUTO',
                    orderReference: '{data['orderReference']}',
                    orderDate: '{data['orderDate']}',
                    amount: '{data["amount"]}',
                    authorizationType: 'SimpleSignature',
                    currency: '{data['currency']}',
                    productName:   {list(map(str,data['productName']))},
                    productPrice:  {list(map(str,data['productPrice']))},
                    productCount:  {list(map(str,data['productCount']))},		
                    merchantSignature: '{signature}',
                    language: '{data['language']}',
                    straightWidget: {data['straightWidget']}
                """ + r"""},
                function (response) {
                    window.location.href='"""+data["returnUrl"]+r"""';				
                } , 			
                function (response) {
                    console.log('dude1');			
                    window.reload()
                },
                function (response) {
                    window.reload()
                } 
            );
        }
        window.addEventListener("message", function () {
            if (event.data == 'WfpWidgetEventClose') {
                
                location.reload()
            }
        }, false);
        </script>
        
    """
    return request_form


def generatePaymentFormScript(purchase_url: str, signature: str, account_data: dict, data: dict) -> str:
    """[summary]
    Creates object for from site chargment request
    Args:
        signature (str): signature hash string
        account_data (dict): merchant_account: str
                            merchant_domain: str
        data (dict): order_data
    """
    request_form = f"""
        <script defer src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script defer id='widget-wfp-script' language='javascript' type='text/javascript' src='https://secure.wayforpay.com/server/pay-widget.js'></script>   
        <form method="post" action="{purchase_url}" hidden accept-charset="utf-8">
            <input name="merchantAccount" value="{account_data['merchant_account']}">
            <input name="merchantAuthType" value="SimpleSignature">
            <input name="merchantDomainName" value="{account_data['merchant_domain']}">
            <input name="orderReference" value="{data['orderReference']}">
            <input name="orderDate" value="{data['orderDate']}">
            <input name="amount" value="{data["amount"]}">
            <input name="serviceUrl" value="{data["serviceUrl"]}">
            <input name="returnUrl" value="{data["returnUrl"]}">
            <input name="currency" value="{data["currency"]}">
            <input name="language" value="{data["language"]}">
            <input name="orderTimeout" value="49000">"""
    for item in data['productName']:
        request_form += f'''<input name="productName[]" value="{item}">\n'''
    for item in data['productPrice']:
        request_form += f'''<input name="productPrice[]" value="{item}">\n'''
    for item in data['productCount']:
        request_form += f'''<input name="productCount[]" value="{item}">\n'''
    request_form += f"""
        <input name="defaultPaymentSystem" value="card">
        <input name="merchantSignature" value="{signature}">
        <input type="submit" id="subm" value="Test">
    </form>
        
    """
    return request_form

def generateFromSitePaymentObject(signature: str, account_data: dict, data: dict)->dict:
    """[summary]
    Creates object for from site chargment request
    Args:
        signature (str): signature hash string
        account_data (dict): merchant_account: str
                            merchant_domain: str
        data (dict): order + personal data to create charge
            orderReference (str): timestamp
            amount (float): order total amount
            currency (str): 'USD', 'UAH', 'RUB'
            card (str): user card number
            expMonth (str): card expires month
            expYear (str): card expires year
            cardCvv (str): card cvv
            cardHolder (str): full name of card holder "Test test"
            productName (list[str]): product names list
            productPrice (list[float]): product price list
            productCount (list[int]): product count list
            clientFirstName (str): client first name
            clientLastName (str): client last name
            clientCountry (str): client country
            clientEmail (str): client email
            clientPhone (str): client phone
    Returns:
        dict: [description]
    """    
    return {
        "transactionType":"CHARGE",
        'merchantAccount': account_data['merchant_account'],
        "merchantAuthType":"SimpleSignature",
        'merchantDomainName': account_data['merchant_domain'],
        "merchantTransactionType":"AUTH",
        "merchantTransactionSecureType": "NON3DS",
        'merchantSignature': signature,
        "apiVersion":1,
        'orderReference': str(data['orderReference']),
        'orderDate': str(data['orderReference']),
        "amount":data["amount"],
        'currency': data['currency'],
        "card":data['card'],
        "expMonth":data['expMonth'],
        "expYear":data['expYear'],
        "cardCvv":data['cardCvv'],
        "cardHolder":data['cardHolder'],
        'productName':   list(map(str, data['productName'])),
        'productPrice':  list(map(float, data['productPrice'])),
        'productCount':  list(map(int, data['productCount'])),
        "clientFirstName":data['clientFirstName'],
        "clientLastName":data['clientLastName'],
        "clientCountry":data['clientCountry'],
        "clientEmail":data['clientEmail'],
        "clientPhone":data['clientPhone'],
    }