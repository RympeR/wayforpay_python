from datetime import date
from .utils import get_signature
from .invoice import *
from .payments import (
    generateWidgetScript,
    generatePaymentFormScript,
    generateWidgetObject,
)
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

    def generateWidget(self, data: dict) -> str:
        self.merchantSignature = self.getRequestSignature(data)
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_domain': self.merchant_domain
        }
        return generateWidgetScript(
            self.merchantSignature,
            account_data,
            data
        )

    def generateForm(self, data: dict) -> str:
        """[summary]
        Generate HTML form for WayForPay payment page
        Args:
            data (dict): order data

        Returns:
            str: form html <script> tag
        """
        self.merchantSignature = self.getRequestSignature(data)
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_domain': self.merchant_domain
        }
        return generatePaymentFormScript(
            self.merchantSignature,
            account_data,
            data
        )

    def generateWidgetJson(self, data: dict) -> dict:
        """[summary]
        Generate json object of payment widget
        Args:
            data (dict): order data

        Returns:
            dict: json object to generate payment widget
        """
        self.merchantSignature = self.getRequestSignature(data)
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_domain': self.merchant_domain
        }
        return generateWidgetObject(
            self.merchantSignature,
            account_data,
            data
        )

    def getRequestSignature(self, order_data: dict) -> str:
        """[summary]
        Generates request signature based on order data
        Args:
            order_data (dict)

        Returns:
            str: signature hash string
        """
        return get_signature(
            self.merchant_key,
            self.__SIGNATURE_SEPARATOR,
            {**self.options, **order_data},
            self.__signature__keys
        )

    def createInvoiceRequest(self, invoice_data: dict) -> dict:
        """[summary]
        Create user invoice

        Args:
            invoice_data (dict): 
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

        Returns:
            dict: wayforpay reponse object
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
        """[summary]
        Edit existing invoice

        Args:
            invoice_data (dict): 
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

        Returns:
            dict: wayforpay reponse object
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

    def statusInvoiceRequest(self, invoice_reference: str) -> dict:
        """[summary]
        check invoice status
        Args:
            invoice_reference (str): invoice id 

        Returns:
            dict: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=createInvoiceObject(
            account_data,
            invoice_reference
        ))
        return response.json()

    def pauseInvoiceRequest(self, invoice_reference: str) -> dict:
        """[summary]
        pause invoice
        Args:
            invoice_reference (str): invoice id 

        Returns:
            dict: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=pauseInvoiceObject(
            account_data,
            invoice_reference
        ))
        return response.json()

    def resumeInvoiceRequest(self, invoice_reference: str) -> dict:
        """[summary]
        resume invoice
        Args:
            invoice_reference (str): invoice id 

        Returns:
            dict: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=resumeInvoiceObject(
            account_data,
            invoice_reference
        ))
        return response.json()

    def removeInvoiceRequest(self, invoice_reference: str) -> dict:
        """[summary]
        remove invoice
        Args:
            invoice_reference (str): invoice id 

        Returns:
            dict: wayforpay reponse object
        """
        account_data = {
            'merchant_account': self.merchant_account,
            'merchant_password': self.merchant_password,
        }
        response = requests.post(INVOICE_URL, data=removeInvoiceObject(
            account_data,
            invoice_reference
        ))
        return response.json()
