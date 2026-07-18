from flask import Flask

app = Flask(__name__)

# Esta es la página principal de tu dashboard
@app.route('/')
def home():
    return "<h1>¡Mi Dashboard de Discord!</h1><p>Aquí irá la info de mi bot.</p>"

# Esta línea asegura que si corres este archivo, el servidor se inicie
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Puerto 5000
