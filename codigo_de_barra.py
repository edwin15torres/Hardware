import barcode
from barcode.writer import ImageWriter

def generar_codigos_ean13(lista_numeros):
    ean = barcode.get_barcode_class('ean13')

    for numero in lista_numeros:
        numero_str = str(numero).zfill(12)  # EAN-13 requiere 12 dígitos, el 13 lo calcula automáticamente
        try:
            codigo = ean(numero_str, writer=ImageWriter())
            nombre_archivo = codigo.save(numero_str)
            print(f"Código de barras generado: {nombre_archivo}.png")
        except Exception as e:
            print(f"Error con el número {numero_str}: {e}")

if __name__ == "__main__":
    # Puedes modificar esta lista con los códigos que desees
    codigos_a_generar = [
        770123456789,  # sin el dígito verificador
        770987654321,
        770112233445
    ]

    generar_codigos_ean13(codigos_a_generar)


