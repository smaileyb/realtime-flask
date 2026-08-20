from flask import Flask, jsonify, request, send_file
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

# Create the Flask application instance.
# This object represents the web app and is used to register routes and configure settings.
app = Flask(__name__)

# Configure the database connection for the app.
# SQLite database file stored in the project directory as 'payments.db'.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'

# Set a secret key used by Flask for session management and security-related features.
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

# Initialize SQLAlchemy with this Flask app so database models can be used.
# This binds the database extension to the application instance.
db.init_app(app)

#Routes
# Define payment route using PIX
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  data = request.get_json()
  #validation
  if 'value' not in data:
    return jsonify({'error': 'Value is required'}), 400
  expiration_date = datetime.now() + timedelta(minutes=30)
  new_payment = Payment(value=data['value'], 
                        expiration_date=expiration_date)
  pix_obj = Pix()
  data_payment_pix = pix_obj.create_payment(data['value'])
  new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
  new_payment.qr_code = data_payment_pix['qr_code_path']

  db.session.add(new_payment)
  db.session.commit()

  return jsonify({'message': 'Pix payment has been created successfully!',
                  'payment': new_payment.to_dict()}), 201

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name):
  return send_file(f'static/img/{file_name}.png', mimetype='image/png')

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_payment_pix():
  return jsonify({'message': 'Pix payment has been confirmed successfully!'}), 201

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
  return 'Pix payment'

if __name__ == '__main__':
  app.run(debug=True)