# WayForPay API python implementation

version 0.0.1

### -dependencies

* requests

## Project structure

#### wayforpaymodule.py

Create objects for invoice API section

#### invoice.py

Create objects for invoice API section

### Example
```python
    from invoice import statusInvoiceObject
    account_date = {
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