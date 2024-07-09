

from django.core.mail import send_mail
from django.conf import settings

def check_restock_level(product):
    if product.stock_quantity <= product.reorder_level:
        send_restock_email(product)

def send_restock_email(product):
    subject = f"RESTOCK ALERT FOR {product.name}"
    message = f"The stock level for {product.name} has dropped to {product.stock_quantity}. Please restock it."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['iannethegamer2@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
