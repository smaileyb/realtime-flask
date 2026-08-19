from flask import Flask, jsonify
from repository.database import db
from db_models.payment import Payment

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
  return jsonify({'message': 'Pix payment has been created successfully!'}), 201

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_payment_pix():
  return jsonify({'message': 'Pix payment has been confirmed successfully!'}), 201

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
  return 'Pix payment'

if __name__ == '__main__':
  app.run(debug=True)