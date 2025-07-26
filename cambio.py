import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QVBoxLayout, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class VentanaCambio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Cambio")
        self.setFixedSize(300, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Formulario con campos
        form_layout = QFormLayout()

        self.input_valor_pagar = QLineEdit()
        self.input_valor_recibido = QLineEdit()
        self.label_cambio = QLabel("$ 0")

        # Alineación
        self.label_cambio.setAlignment(Qt.AlignCenter)
        self.label_cambio.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Conectar señales
        self.input_valor_pagar.textChanged.connect(self.calcular_cambio)
        self.input_valor_recibido.textChanged.connect(self.calcular_cambio)

        # Agregar al formulario
        form_layout.addRow("Valor a pagar:", self.input_valor_pagar)
        form_layout.addRow("Valor recibido:", self.input_valor_recibido)

        layout.addLayout(form_layout)
        layout.addWidget(QLabel("Cambio:"))
        layout.addWidget(self.label_cambio)

        self.setLayout(layout)

    def calcular_cambio(self):
        try:
            pagar = float(self.input_valor_pagar.text())
            recibido = float(self.input_valor_recibido.text())
            cambio = recibido - pagar
            self.label_cambio.setText(f"$ {cambio:,.2f}")
            if cambio < 0:
                self.label_cambio.setStyleSheet("color: red; font-weight: bold; font-size: 18px;")
            else:
                self.label_cambio.setStyleSheet("color: green; font-weight: bold; font-size: 18px;")
        except ValueError:
            self.label_cambio.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCambio()
    ventana.show()
    sys.exit(app.exec_())
