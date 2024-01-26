import xlwt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def crear_nota_entrega(self, cliente, productos):
    self.cliente = cliente
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Crear el objeto PDF
    pdf_filename = f"Nota_Entrega_{self.cliente}_{fecha_actual.replace('/', '_').replace(' ', '_').replace(':', '')}.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)

    # Crear el objeto Excel
    xls_filename = f"Nota_Entrega_{self.cliente}_{fecha_actual.replace('/', '_').replace(' ', '_').replace(':', '')}.xls"
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("Nota de Entrega")

    # Configurar la fuente para el PDF
    pdf.setFont("Helvetica", 12)

    # Información de la nota de entrega en el PDF
    pdf.drawString(100, 750, "Nota de Entrega")
    pdf.drawString(100, 730, f"Fecha: {fecha_actual}")
    pdf.drawString(100, 710, f"Cliente: {self.cliente}")

    # Información de la nota de entrega en el Excel
    worksheet.write(0, 0, "Nota de Entrega")
    worksheet.write(1, 0, f"Fecha: {fecha_actual}")
    worksheet.write(2, 0, f"Cliente: {self.cliente}")

    # Detalles de los productos
    y_pdf = 690
    y_excel = 3  # Fila en el Excel
    for producto in productos:
        # Detalles en el PDF
        pdf.drawString(100, y_pdf, f"Producto: {producto['nombre']}")
        pdf.drawString(250, y_pdf, f"Cantidad: {producto['cantidad']}")
        pdf.drawString(400, y_pdf, f"Precio Unitario: ${producto['precio_unitario']}")
        pdf.drawString(550, y_pdf, f"Total: ${producto['cantidad'] * producto['precio_unitario']}")
        
        # Detalles en el Excel
        worksheet.write(y_excel, 0, f"Producto: {producto['nombre']}")
        worksheet.write(y_excel, 1, f"Cantidad: {producto['cantidad']}")
        worksheet.write(y_excel, 2, f"Precio Unitario: ${producto['precio_unitario']}")
        worksheet.write(y_excel, 3, f"Total: ${producto['cantidad'] * producto['precio_unitario']}")
        
        y_pdf -= 20
        y_excel += 1

    # Total general
    total_general = sum(p['cantidad'] * p['precio_unitario'] for p in productos)
    pdf.drawString(400, y_pdf - 20, f"Total General: ${total_general}")

    # Guardar el PDF
    pdf.save()

    # Guardar el Excel
    workbook.save(xls_filename)

    print(f"Nota de entrega y archivo Excel creados con éxito: {pdf_filename}, {xls_filename}")

# Ejemplo de uso
cliente = "Cliente Ejemplo"
productos = [
    {"nombre": "Producto 1", "cantidad": 2, "precio_unitario": 10},
    {"nombre": "Producto 2", "cantidad": 3, "precio_unitario": 15},
    # Agrega más productos según sea necesario
]

crear_nota_entrega(cliente, productos)
