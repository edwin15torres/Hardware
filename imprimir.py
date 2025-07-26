from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import QSizeF
import sys

class VentanaFactura(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factura")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout(self)
        self.btn_previsualizar = QPushButton("Previsualizar e Imprimir/Guardar como PDF")
        self.btn_previsualizar.clicked.connect(self.mostrar_vista_previa)
        layout.addWidget(self.btn_previsualizar)

    def generar_html_factura(self):
        return """
        <h2 style='text-align:center;'>Factura de Venta</h2>
        <p><strong>Cliente:</strong> Juan Pérez</p>
        <p><strong>Fecha:</strong> 25/07/2025</p>
        <table border='1' cellspacing='0' cellpadding='4' width='100%'>
            <tr><th>Producto</th><th>Cantidad</th><th>Precio</th></tr>
            <tr><td>Salchicha</td><td>2</td><td>$8.000</td></tr>
            <tr><td>Gaseosa</td><td>1</td><td>$2.000</td></tr>
        </table>
        <p style='text-align:right;'><strong>Total:</strong> $10.000</p>
        """

    def mostrar_vista_previa(self):
        documento = QTextDocument()
        documento.setHtml(self.generar_html_factura())

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.Custom)
        printer.setPaperSize(QSizeF(58, 297), QPrinter.Millimeter)
        printer.setFullPage(True)

        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Vista previa de la factura")
        preview.paintRequested.connect(documento.print_)
        preview.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaFactura()
    ventana.show()
    sys.exit(app.exec_())
