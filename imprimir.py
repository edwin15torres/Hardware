from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument

import sys

class VentanaFactura(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factura")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout(self)

        # Botón para mostrar vista previa
        self.btn_previsualizar = QPushButton("Previsualizar e Imprimir Factura")
        self.btn_previsualizar.clicked.connect(self.mostrar_vista_previa)

        layout.addWidget(self.btn_previsualizar)

    def generar_html_factura(self):
        return """
        <h2 style='text-align:center;'>Factura de Venta</h2>
        <p><strong>Cliente:</strong> Juan Pérez</p>
        <p><strong>Fecha:</strong> 25/07/2025</p>
        <table border='1' cellspacing='0' cellpadding='5' width='100%'>
            <tr>
                <th>Producto</th><th>Cantidad</th><th>Precio Unitario</th><th>Total</th>
            </tr>
            <tr>
                <td>Pollo Asado</td><td>2</td><td>$15.000</td><td>$30.000</td>
            </tr>
            <tr>
                <td>Cerveza</td><td>3</td><td>$5.000</td><td>$15.000</td>
            </tr>
            <tr>
                <td colspan='3' align='right'><strong>Total a Pagar:</strong></td>
                <td><strong>$45.000</strong></td>
            </tr>
        </table>
        """

    def mostrar_vista_previa(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialogo_vista_previa = QPrintPreviewDialog(printer, self)
        dialogo_vista_previa.paintRequested.connect(self.imprimir_factura)
        dialogo_vista_previa.exec_()

    def imprimir_factura(self, printer):
        doc = QTextDocument()
        doc.setHtml(self.generar_html_factura())
        doc.print_(printer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaFactura()
    ventana.show()
    sys.exit(app.exec_())
