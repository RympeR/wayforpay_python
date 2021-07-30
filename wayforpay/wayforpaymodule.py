import hashlib
import hmac
from datetime import date
from .invoice import *
from .utils import get_signature
import requests

API_URL = "https://api.wayforpay.com/api"
PURCHASE_URL = "https://secure.wayforpay.com/pay"
INVOICE_URL = 'https://api.wayforpay.com/regularApi'
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

    def get_request_signature(self, options: dict) -> str:
        
        return get_signature(
            self.merchant_key,
            self.__SIGNATURE_SEPARATOR,
            options,
            self.__signature__keys
        )

    def createInvoiceRequest(self, invoice_data: dict) -> dict:
        """
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
            return: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=createInvoiceObject(
            account_data,
            invoice_data
        ))
        return response.json()

    def editInvoiceRequest(self, invoice_data: dict) -> dict:
        """
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
            return: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=editInvoiceObject(
            account_data,
            invoice_data
        ))
        return response.json()

    def statusInvoiceRequest(self, order_reference: str) -> dict:
        """
            param: orderReference : str
            return: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=createInvoiceObject(
            account_data,
            order_reference
        ))
        return response.json()

    def pauseInvoiceRequest(self, order_reference: str) -> dict:
        """
            param: orderReference : str
            return: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=pauseInvoiceObject(
            account_data,
            order_reference
        ))
        return response.json()

    def resumeInvoiceRequest(self, order_reference: str) -> dict:
        """
            param: orderReference : str
            return: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=resumeInvoiceObject(
            account_data,
            order_reference
        ))
        return response.json()

    def removeInvoiceRequest(self, order_reference: str) -> dict:
        """
            param: orderReference : str
            return: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=removeInvoiceObject(
            account_data,
            order_reference
        ))
        return response.json()
