# utils.py

import os
import qrcode
from reportlab.pdfgen import canvas
from django.conf import settings

def generate_pdf_with_qr(booking_details):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(booking_details)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    pdf_file = os.path.join(settings.MEDIA_ROOT, 'ticket.pdf')
    c = canvas.Canvas(pdf_file)
    c.drawString(100, 800, "Booking Details:")
    c.drawImage(qr_img, 100, 600)
    c.save()

    return pdf_file
