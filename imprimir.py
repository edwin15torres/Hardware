import sys
import win32print
import win32ui
import win32con
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QDialog, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter
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
Gaseosa       1     2000
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

        btn_guardar_pdf = QPushButton("Guardar PDF")
        btn_guardar_pdf.clicked.connect(lambda: self.guardar_pdf(texto))
        layout.addWidget(btn_guardar_pdf)

    def imprimir_ticket(self, texto):
        try:
            printer_name = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Factura")
            hDC.StartPage()

            # Cargar y dibujar imagen PNG en modo GDI (vía PIL + ImageWin)
            # Intentar cargar logo_chorizos.png primero, luego logo.png
            logo_paths = [
                "logo_chorizos.png",  # En la carpeta Hardware
                "Hardware/logo_chorizos.png",
                "logo.png",
                "Hardware/logo.png"
            ]
            
            y = 10
            logo_encontrado = False
            for logo_path in logo_paths:
                try:
                    img = Image.open(logo_path).convert("RGB")
                    
                    # Escalar conservando proporción (max ancho 250)
                    max_width = 250
                    w_percent = max_width / float(img.width)
                    new_height = int((float(img.height) * float(w_percent)))
                    img = img.resize((max_width, new_height))

                    dib = ImageWin.Dib(img)
                    dib.draw(hDC.GetHandleOutput(), (25, 10, 25 + max_width, 10 + new_height))
                    y = 10 + new_height + 10  # Espacio para el texto
                    logo_encontrado = True
                    break
                except Exception as e:
                    print(f"Error al cargar logo desde {logo_path}: {e}")
                    continue
            
            if not logo_encontrado:
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
            QMessageBox.warning(self, "Error", f"Error al imprimir: {str(e)}")

    def guardar_pdf(self, texto):
        """
        Guarda la factura como PDF
        """
        # Diálogo para guardar archivo
        nombre_archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar factura como PDF",
            "Factura.pdf",
            "PDF Files (*.pdf)"
        )
        
        if nombre_archivo:
            try:
                # Crear printer para PDF
                printer = QPrinter(QPrinter.HighResolution)
                printer.setPageSize(QPrinter.A4)
                printer.setOrientation(QPrinter.Portrait)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(nombre_archivo)
                
                # Crear painter y renderizar
                painter = QPainter()
                painter.begin(printer)
                
                # Intentar cargar y dibujar logo
                logo_paths = [
                    "logo_chorizos.png",  # En la carpeta Hardware
                    "Hardware/logo_chorizos.png",
                    "logo.png",
                    "Hardware/logo.png"
                ]
                
                y = 10
                logo_encontrado = False
                for logo_path in logo_paths:
                    try:
                        img = Image.open(logo_path).convert("RGB")
                        
                        # Escalar conservando proporción (max ancho 250)
                        max_width = 250
                        w_percent = max_width / float(img.width)
                        new_height = int((float(img.height) * float(w_percent)))
                        img = img.resize((max_width, new_height))
                        
                        # Convertir PIL Image a QPixmap para PDF
                        from PyQt5.QtGui import QPixmap, QImage
                        import io
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        qimage = QImage()
                        qimage.loadFromData(img_bytes.read())
                        pixmap = QPixmap.fromImage(qimage)
                        
                        # Dibujar logo en el PDF
                        painter.drawPixmap(25, 10, max_width, new_height, pixmap)
                        y = 10 + new_height + 10
                        logo_encontrado = True
                        break
                    except Exception as e:
                        print(f"Error al cargar logo desde {logo_path}: {e}")
                        continue
                
                if not logo_encontrado:
                    y = 10
                
                # Configurar fuente para el texto
                from PyQt5.QtGui import QFont
                font = QFont("Courier New", 10)
                painter.setFont(font)
                
                # Imprimir texto línea por línea
                salto = 20
                for linea in texto.splitlines():
                    painter.drawText(10, y, linea.strip())
                    y += salto
                
                painter.end()
                
                QMessageBox.information(self, "Éxito", f"Factura guardada como PDF:\n{nombre_archivo}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al guardar PDF: {str(e)}")

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
