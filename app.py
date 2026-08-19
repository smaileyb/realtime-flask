from flask import Flask, jsonify

app = Flask(__name__)

# Define payment route using PIX
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  return jsonify({'message': 'Pix payment has been created successfully!'}), 201

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_payment_pix():
  return jsonify({'message': 'Pix payment has been confirmed successfully!'}), 201

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
  return 'Pix payment'

if __name__ == '__main__':
  app.run(debug=True)