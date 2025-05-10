from flask import Flask, request, render_template, send_file
import json, os
import matplotlib.pyplot as plt

app = Flask(__name__)
ARCHIVO_PEDIDOS = 'pedidos.json'

@app.route('/')
def formulario():
    return render_template('form.html')

@app.route('/guardar_pedido', methods=['POST'])
def guardar_pedido():
    datos = request.get_json()

    if os.path.exists(ARCHIVO_PEDIDOS):
        with open(ARCHIVO_PEDIDOS, 'r') as f:
            pedidos = json.load(f)
    else:
        pedidos = []

    pedidos.append(datos)

    with open(ARCHIVO_PEDIDOS, 'w') as f:
        json.dump(pedidos, f, indent=4)

    return {'mensaje': 'Pedido guardado'}

@app.route('/grafica-pedidos')
def grafica_pedidos():
    if not os.path.exists(ARCHIVO_PEDIDOS):
        return "No hay datos aún."

    with open(ARCHIVO_PEDIDOS, 'r') as f:
        pedidos = json.load(f)

    tipos = {}
    for p in pedidos:
        tipo = p['tipo']
        tipos[tipo] = tipos.get(tipo, 0) + 1

    plt.figure(figsize=(8, 6))
    plt.bar(tipos.keys(), tipos.values(), color='salmon')
    plt.xlabel("Tipo de Producto")
    plt.ylabel("Cantidad de Pedidos")
    plt.title("Pedidos por Tipo de Producto")
    plt.tight_layout()
    plt.savefig('grafica_pedidos.png')

    return send_file('grafica_pedidos.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)