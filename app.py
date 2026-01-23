from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Szia! Az AMP Python AppRunner mukodik!</h1><p>A toolkit alapja keszen all.</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=42401)