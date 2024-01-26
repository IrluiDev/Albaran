from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from openpyxl import Workbook, load_workbook
import os
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_albaran', methods=['POST'])
def generar_albaran():
    # Obtener datos del formulario
    cliente = request.form.get('cliente')
    productos = request.form.get('productos')
    date = datetime.now().strftime("%Y-%m-%d")

    # Crear PDF
    pdf_filename = f'albaran_{cliente}_{date}.pdf'
    pdf_path = os.path.join(app.static_folder, pdf_filename)

    # with open(pdf_path, 'wb') as pdf_file:
    #     c = canvas.Canvas(pdf_file)
    #     c.drawString(100, 820, f'Fecha: {date}')
    #     c.drawString(100, 800, f'Cliente: {cliente}')
    #     c.drawString(100, 780, f'Productos: {productos}')
    #     c.showPage()
    #     c.save()
        
        # Configuración del canvas
    c = canvas.Canvas(pdf_path, pagesize=(400, 600))
    
    # Logo (reemplaza 'path_al_logo' con la ruta a tu archivo de imagen)
    path_al_logo = 'static/logo.jpg'
    c.drawInlineImage(path_al_logo, 20, 550, width=80, height=80)

    # Encabezado
    c.setFont("Helvetica-Bold", 14)
    c.drawString(120, 550, "Albarán")

    # Información del cliente
    c.setFont("Helvetica", 12)
    c.drawString(20, 520, f'Fecha: {date}')
    c.drawString(20, 500, f'Cliente: {cliente}')

    # Línea de separación
    c.line(20, 480, 380, 480)

    # Detalles de productos
    c.drawString(20, 460, 'Productos:')
    productos = productos.split('\n')  # Suponiendo que los productos se ingresan en líneas separadas
    y_position = 440
    for producto in productos:
        c.drawString(40, y_position, producto)
        y_position -= 20

    # Guardar el PDF
    c.showPage()
    c.save()

 
    # Crear o actualizar archivo CSV
    csv_filename = 'datos.csv'
    csv_path = os.path.join(app.static_folder, csv_filename)

    with open(csv_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not os.path.isfile(csv_path):
            csv_writer.writerow(['Fecha','Cliente', 'Productos'])
        csv_writer.writerow([date,cliente, productos])

    return render_template('resultado.html', pdf=pdf_filename, csv=csv_filename)

@app.route('/descargar/<filename>')
def descargar(filename):
    return send_file(os.path.join(app.static_folder, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
