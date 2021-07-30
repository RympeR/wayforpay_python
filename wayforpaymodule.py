import hashlib
import hmac
from datetime import date
from .payments import *
from .invoice import *

API_URL = "https://api.wayforpay.com/api"
PURCHASE_URL = "https://secure.wayforpay.com/pay"
API_VERSION = 1
today = date.today()


class WayForPayAPI:
    __signature__keys = [
        'merchantAccount',
        'merchantDomainName',
        'orderReference',
        'orderDate',
        'amount',
        'currency',
        'productName',
        'productCount',
        'productPrice'
    ]
    __ORDER_APPROVED = 'Approved'
    __ORDER_REFUNDED = 'Refunded'
    __SIGNATURE_SEPARATOR = ';'
    __ORDER_SEPARATOR = ":"

    def __init__(self, merchant_account: str, merchant_key: str, merchant_domain: str, merchant_password: str = ''):
        self.id = 'wayforpay'
        self.method_title = 'WayForPay'
        self.merchant_account = merchant_account
        self.merchant_key = merchant_key
        self.merchant_domain = merchant_domain
        self.merchant_password = merchant_password
        self.options = {
            'merchantAccount': self.merchant_account,
            'merchantAuthType': 'simpleSignature',
            'merchantDomainName': self.merchant_domain,
            'merchantTransactionSecureType': 'AUTO',
        }

    def generate_widget(self, data: dict) -> str:
        self.merchantSignature = self.get_request_signature(
            {**self.options, **data})
        request_form = r"""
            <script type="text/javascript"> 
            function pay(){
                var payment = new Wayforpay();
                    payment.run({""" + f"""
                        merchantAccount: '{self.merchant_account}',
                        merchantDomainName: '{self.merchant_domain}',
                        merchantTransactionType: 'AUTO',
                        merchantTransactionSecureType: 'AUTO',
                        orderReference: '{data['orderReference']}',
                        orderDate: '{data['orderDate']}',
                        amount: '{data["amount"]}',
                        authorizationType: 'SimpleSignature',
                        currency: 'UAH',
                        productName:   {list(map(str,data['productName']))},
                        productPrice:  {list(map(str,data['productPrice']))},
                        productCount:  {list(map(str,data['productCount']))},		
                        merchantSignature: '{self.merchantSignature}',
                        language: 'RU',
                        straightWidget: true
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

    def generate_payment_form(self, data: dict) -> str:
        self.merchantSignature = self.get_request_signature(
            {**self.options, **data})
        request_form = f"""
            <script defer src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script defer id='widget-wfp-script' language='javascript' type='text/javascript' src='https://secure.wayforpay.com/server/pay-widget.js'></script>   
            <form method="post" action="{PURCHASE_URL}" hidden accept-charset="utf-8">
                <input name="merchantAccount" value="{self.merchant_account}">
                <input name="merchantAuthType" value="SimpleSignature">
                <input name="merchantDomainName" value="{self.merchant_domain}">
                <input name="orderReference" value="{data['orderReference']}">
                <input name="orderDate" value="{data['orderDate']}">
                <input name="amount" value="{data["amount"]}">
                <input name="serviceUrl" value="{data["serviceUrl"]}">
                <input name="returnUrl" value="{data["returnUrl"]}">
                <input name="currency" value="UAH">
                <input name="orderTimeout" value="49000">"""
        for item in data['productName']:
            request_form += f'''<input name="productName[]" value="{item}">\n'''
        for item in data['productPrice']:
            request_form += f'''<input name="productPrice[]" value="{item}">\n'''
        for item in data['productCount']:
            request_form += f'''<input name="productCount[]" value="{item}">\n'''
        request_form += f"""
            <input name="defaultPaymentSystem" value="card">
            <input name="merchantSignature" value="{self.merchantSignature}">
            <input type="submit" id="subm" value="Test">
        </form>
            
        """
        return request_form
        
    def generate_widget_object(self, data: dict) -> dict:
        return {
            'merchantAccount': self.merchant_account,
            'merchantDomainName': self.merchant_domain,
            'merchantTransactionType': 'AUTO',
            'merchantTransactionSecureType': 'AUTO',
            'orderReference': f'{data["orderReference"]}',
            'orderDate': f'{data["orderDate"]}',
            'amount': f'{data["amount"]}',
            'authorizationType': 'SimpleSignature',
            'currency': 'UAH',
            'productName':   {list(map(str, data['productName']))},
            'productPrice':  {list(map(str, data['productPrice']))},
            'productCount':  {list(map(str, data['productCount']))},
            'merchantSignature': self.merchantSignature,
            'language': 'RU',
            'straightWidget': True
        }

    def get_signature(self, options: dict, keys: list) -> str:
        hash_str = list()
        for datakey in keys:
            if not options.get(datakey, None):
                continue
            if isinstance(options[datakey], list):
                for _ in options[datakey]:
                    hash_str.append(str(_))
            else:
                hash_str.append(str(options[datakey]))
        hash_str = ';'.join(hash_str)
        self.merchant_key_encoded = bytes(str.encode(self.merchant_key))
        _hash = hmac.new(self.merchant_key_encoded, hash_str.encode(
            "utf-8"), hashlib.md5).hexdigest()
        return _hash

    def get_request_signature(self, options: dict) -> str:
        return self.get_signature(options, self.__signature__keys)

    

    
