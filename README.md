# Realtime Flask

A small study project built with Python, Flask, Flask-SocketIO, and SQLite to explore how real-time payment flows can be implemented in a web application.

This app simulates a PIX payment flow where a user creates a payment, receives a QR code, and gets a real-time confirmation through a WebSocket event once the payment is confirmed.

## ✨ What this project does

The application demonstrates:

- Creating a payment with a value
- Generating a PIX-style QR code
- Serving the QR code image through Flask
- Confirming a payment through an API endpoint
- Broadcasting a real-time notification to the frontend using WebSockets
- Rendering the payment page with live confirmation updates

It is a practical example for learning:

- Python web development with Flask
- API design and request handling
- Database integration with SQLAlchemy
- Real-time communication with Flask-SocketIO
- HTML templates and frontend integration

## 🧩 Project structure

```text
realtime-flask/
├── app.py
├── pyproject.toml
├── README.md
├── request.http
├── db_models/
│   └── payment.py
├── payments/
│   └── pix.py
├── repository/
│   └── database.py
├── static/
│   ├── css/
│   ├── img/
│   └── template_img/
├── templates/
│   ├── 404.html
│   ├── confirmed_payment.html
│   └── payment.html
└── tests/
    └── test_pix.py
```

## ✅ Prerequisites

Before running the project, make sure you have:

- Python 3.12 or newer
- pip or uv
- Git

## 🚀 Clone the project

```bash
git clone https://github.com/your-username/realtime-flask.git
cd realtime-flask
```

## 📦 Install dependencies

This project uses `uv` for dependency management, as configured in `pyproject.toml`.

### With uv

```bash
uv sync
```

If you prefer using pip:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install flask flask-socketio flask-sqlalchemy pillow qrcode pytest
```

## ▶️ Run the application

Start the Flask server:

```bash
uv run python app.py
```

or, if using a virtual environment:

```bash
python app.py
```

The app will run on:

```text
http://localhost:5000
```

## 🧪 How it works

The flow is simple:

1. A client creates a PIX payment by calling the API.
2. The backend creates a payment record and generates a QR code image.
3. The payment page loads the QR code and listens for a WebSocket event.
4. A confirmation request updates the payment status to paid.
5. The server emits a Socket.IO event like `payment_confirmed_<id>`.
6. The frontend reloads automatically, showing a success state.

## 🔌 API endpoints

### Create a payment

```http
POST /payments/pix
Content-Type: application/json

{
  "value": 12000
}
```

Returns the created payment data and QR code metadata.

### Get the payment page

```http
GET /payments/pix/<payment_id>
```

This renders the page with the QR code and payment information.

### Confirm a payment

```http
POST /payments/pix/confirmation
Content-Type: application/json

{
  "value": 12000,
  "bank_payment_id": "your-payment-id"
}
```

If the data matches, the payment is marked as paid and a real-time event is emitted.

### Get the QR image

```http
GET /payments/pix/qr_code/<file_name>
```

## 🌐 WebSocket behavior

The app uses Flask-SocketIO to notify the payment page when a transaction is confirmed.

The frontend listens for a channel such as:

```javascript
socket.on('payment_confirmed_1', () => {
  location.reload()
})
```

This gives a simple example of real-time updates without polling.

## 🧾 Example usage

You can test the API with the included `request.http` file in VS Code or using curl:

```bash
curl -X POST http://localhost:5000/payments/pix \
  -H "Content-Type: application/json" \
  -d '{"value": 12000}'
```

Then confirm it:

```bash
curl -X POST http://localhost:5000/payments/pix/confirmation \
  -H "Content-Type: application/json" \
  -d '{"value": 12000, "bank_payment_id": "your-payment-id"}'
```

## 🛠️ Notes

- The database is SQLite and is stored in the project directory.
- The QR code is generated locally as an image file.
- This is a study project, so the payment flow is intentionally simplified and uses simulated data.

## 📚 Learning goals

This project is intended as a learning sandbox for:

- Python backend fundamentals
- Flask routing and MVC-style structure
- SQLAlchemy ORM with SQLite
- Real-time communication with Socket.IO
- Building a realistic mini payment UX

## License

This project is for educational purposes and is not intended for production financial use.
