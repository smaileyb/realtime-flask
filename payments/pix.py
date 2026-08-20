import uuid
import qrcode

class Pix:
  def __init__(self):
    pass
  def create_payment(self, value):
    # create the payment in the financial institution
    bank_payment_id = str(uuid.uuid4())

    #simulate code for qr code generation
    hash_payment = f'hash_payment_{bank_payment_id}'

    # Generate QR code and save it as an image file
    qr_code_img = qrcode.make(hash_payment)
    qr_code_img.save(f'static/img/qr_code_payment_{bank_payment_id}.png')

    
    return {"bank_payment_id": bank_payment_id, 
            "qr_code_path": f'qr_code_payment_{bank_payment_id}'}