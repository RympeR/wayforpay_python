from  wayforpay.wayforpay import InvoiceRequests

invoice_requests = InvoiceRequests(
    merchant_account='XXXXXXXXXXXXXXXXXXXXXXXX',
    merchant_key='XXXXXXXXXXXXXXXXXXXXXXXX',
    merchant_domain='example.com',
)

invoice_data = {
    'reqularMode': 'monthly',
    'amount' : '10',
    'currency' : 'UAH',
    'dateNext' : '13.10.2021',
    'dateEnd' : '13.10.2022',
    'orderReference' : '123434234234',
    'email' : 'test@gmail.com',
}

print(invoice_requests.createInvoiceRequest(invoice_data))
print(invoice_requests.editInvoiceRequest(invoice_data))
print(invoice_requests.statusInvoiceRequest(invoice_data['orderReference']))
print(invoice_requests.pauseInvoiceRequest(invoice_data['orderReference']))
print(invoice_requests.resumeInvoiceRequest(invoice_data['orderReference']))
print(invoice_requests.removeInvoiceRequest(invoice_data['orderReference']))

