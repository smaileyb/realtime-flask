from flask import Flask, jsonify, request, send_file, render_template
from flask_socketio import SocketIO
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
socketio = SocketIO(app)

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
  data = request.get_json()

  # validations
  if "bank_payment_id" not in data and "value" not in data:
    return jsonify({'error': 'Invalid payment data'}), 400

# payment
  payment = Payment.query.filter_by(bank_payment_id=data.get('bank_payment_id')).first()
  if not payment or payment.paid:
    return jsonify({'error': 'Payment not found'}), 404

  if data.get('value') != payment.value:
    return jsonify({'error': 'Payment value does not match'}), 400

  payment.paid = True
  db.session.commit()
  socketio.emit(f'payment_confirmed_{payment.id}', {'message': 'Payment confirmed successfully!'})
  return jsonify({'message': 'Pix payment has been confirmed successfully!'}), 201

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
  payment = db.session.get(Payment, payment_id)

  if not payment:
    return render_template('404.html')
  if payment.paid:
    return render_template('confirmed_payment.html',
                           payment_id=payment.id, 
                           payment_value=payment.value)
  return render_template('payment.html', 
                         payment_id=payment.id, 
                         payment_value=payment.value, 
                         host='http://localhost:5000', 
                         qr_code=payment.qr_code)

## Websockets
@socketio.on('connect')
def handle_connect():
  print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
  print('Client disconnected')

if __name__ == '__main__':
  socketio.run(app, debug=True)