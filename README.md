# WayForPay API python implementation

version 0.0.1

## Installation

```
    pip install wayforpay-python
```
or add wayforpay-python to requirements.txt

## Project structure

#### wayforpaymodule.py

Made requests to WFP API

#### payments.py

Create objects for payment API section

#### invoice.py

Create objects for invoice API section

# USAGE
## Available methods sections

- Payment methods
    - Payment form ( html )
    - Payment widget ( html )
    - Payment widget ( json obj )
- Invoices
    - Create  invoice
    - Edit  invoice
    - Pause  invoice
    - Resume  invoice
    - Remove  invoice

You can create objects to made requests by yourself or lett lib make requests and return json response object

## Examples

#### Status invoice object
```python
    from invoice import statusInvoiceObject
    account_data = {
        'merchant_account': 'XXXXXXXXXXXXXXXXXXXXXX',
        'merchant_password': 'XXXXXXXXXXXXXXXXXXXXXX',
    }
    order_reference = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
    print(statusInvoiceObject(
        accound_data,
        order_reference
    ))
    """
        {
            "requestType": "STATUS",
            "merchantAccount": 'XXXXXXXXXXXXXXXXXXXXXX',
            "merchantPassword": 'XXXXXXXXXXXXXXXXXXXXXX',
            "orderReference": 'XXXXXXXXXXXXXXXXXXXXXX',
        }
    """
```
#### Create widget json object
```python
    from wayforpay import WayForPayAPI
    import calendar
    import time
    ts = calendar.timegm(time.gmtime())
    wp = WayForPayAPI(
            'XXXXXXXXXXXXX',
            'XXXXXXXXXXXXX',
            'XXXXXXXXXXXXX',
            'XXXXXXXXXXXXX'
    )
    names = ['value', 'value2']
    cost = ['1', '2']
    amount = ['1', '1']
    data = {
        'orderReference': ts,
        'orderDate': ts,
        'amount': '3',
        'currency': 'UAH',
        'productName': names,
        'productPrice': cost,
        'serviceUrl': 'http://127.0.0.1:8000/finish-order/',
        'returnUrl': 'http://127.0.0.1:8000/finish-order/',
        'productCount': amount,
        'straightWidget': True
    }
    print(wp.generateWidgetJson(data))
    """
        {
            'merchantAccount': 'XXXXXXXXXXXXX',
            'merchantDomainName': 'XXXXXXXXXXXXX',
            'merchantTransactionType': 'AUTO',
            'merchantTransactionSecureType': 'AUTO',
            'orderReference': '1234243234324',
            'orderDate': '1234243234324',
            'amount': '3',
            'authorizationType': 'SimpleSignature',
            'currency': 'USD',
            'productName':   ['value', 'value2'],
            'productPrice':  ['1', '2'],
            'productCount':  ['1', '1'],
            'merchantSignature': signature,
            'language': 'EN',
            'straightWidget': True
        }
    """
```
#### Create widget html script
```python
    from wayforpay import WayForPayAPI
    import calendar
    import time
    ts = calendar.timegm(time.gmtime())
    wp = WayForPayAPI(
            'XXXXXXXXXXXXX',
            'XXXXXXXXXXXXX',
            'XXXXXXXXXXXXX',
            'XXXXXXXXXXXXX'
    )
    names = ['value', 'value2']
    cost = ['1', '2']
    amount = ['1', '1']
    data = {
        'orderReference': ts,
        'orderDate': ts,
        'amount': '3',
        'currency': 'UAH',
        'productName': names,
        'productPrice': cost,
        'serviceUrl': 'http://127.0.0.1:8000/finish-order/',
        'returnUrl': 'http://127.0.0.1:8000/finish-order/',
        'productCount': amount,
        'straightWidget': True
    }
    widget = wp.generateWidget(data)
    print(widget)
    """
        
        <script type="text/javascript">
        function pay(){
            var payment = new Wayforpay();
                payment.run({
                    'merchantAccount': 'XXXXXXXXXXXXX',
                    'merchantDomainName': 'XXXXXXXXXXXXX',
                    'merchantTransactionType': 'AUTO',
                    'merchantTransactionSecureType': 'AUTO',
                    'orderReference': '1234243234324',
                    'orderDate': '1234243234324',
                    'amount': '3',
                    'authorizationType': 'SimpleSignature',
                    'currency': 'USD',
                    'productName':   ['value', 'value2'],
                    'productPrice':  ['1', '2'],
                    'productCount':  ['1', '1'],
                    'merchantSignature': signature,
                    'language': 'EN',
                    'straightWidget': True
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
```
#### Jinja
```html
<button onclick="pay()"><span style="color:white">Оплата</span></button>
<script id='widget-wfp-script' language='javascript' type='text/javascript' src='https://secure.wayforpay.com/server/pay-widget.js'></script>
{{ widget|safe }}
```