import sys
import win32print
import win32ui
import win32con
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QDialog
)
from PIL import Image, ImageWin

# -------------------------------
# Generador de texto de facturaimg
# -------------------------------
def generar_texto_factura():
    return """\
        FACTURA DE VENTA
Cliente: Juan Pérez
Fecha: 25/07/2025

Item         Cant   Precio
----------------------------
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Gaseosa       1     2000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
Salchicha     2     8000
----------------------------
TOTAL:             $10.000

¡Gracias por su compra!
Vuelva pronto :)
"""

# -------------------------------
# Vista previa en PyQt
# -------------------------------
class VistaPreviaFactura(QDialog):
    def __init__(self, texto):
        super().__init__()
        self.setWindowTitle("Vista previa de factura térmica")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(texto)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        btn_imprimir = QPushButton("Imprimir en impresora térmica")
        btn_imprimir.clicked.connect(lambda: self.imprimir_ticket(texto))
        layout.addWidget(btn_imprimir)

    def imprimir_ticket(self, texto):
        try:
            printer_name = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Factura")
            hDC.StartPage()

            # Cargar y dibujar imagen PNG en modo GDI (vía PIL + ImageWin)
            try:
                img = Image.open("logo.png").convert("RGB")

                # Escalar conservando proporción (max ancho 250)
                max_width = 250
                w_percent = max_width / float(img.width)
                new_height = int((float(img.height) * float(w_percent)))
                img = img.resize((max_width, new_height))

                dib = ImageWin.Dib(img)
                dib.draw(hDC.GetHandleOutput(), (25, 10, 25 + max_width, 10 + new_height))
                y = 10 + new_height + 10  # Espacio para el texto

            except Exception as e:
                print("Error al cargar logo:", e)
                y = 10

            # Fuente
            font = win32ui.CreateFont({
                "name": "Courier New",
                "height": 25,
                "weight": 400
            })
            hDC.SelectObject(font)

            salto = 20
            for linea in texto.splitlines():
                hDC.TextOut(10, y, linea.strip())
                y += salto

            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            self.accept()
        except Exception as e:
            print("Error al imprimir:", e)

# -------------------------------
# Ventana principal
# -------------------------------
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factura Térmica")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        btn_previsualizar = QPushButton("Previsualizar Factura")
        btn_previsualizar.clicked.connect(self.mostrar_previsualizacion)
        layout.addWidget(btn_previsualizar)

    def mostrar_previsualizacion(self):
        texto = generar_texto_factura()
        vista = VistaPreviaFactura(texto)
        vista.exec_()

# -------------------------------
# Inicio de la app
# -------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
