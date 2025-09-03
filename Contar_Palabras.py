# Programa para contar la frecuencia de cada palabra en un documento PDF

import PyPDF2
import re
from collections import Counter

def extraer_texto_pdf(ruta_pdf):
    """Extrae el texto de todas las páginas de un archivo PDF."""
    texto = ""
    with open(ruta_pdf, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text() + " "
    return texto

def contar_palabras(texto):
    """Cuenta cuántas veces aparece cada palabra en el texto."""
    # Elimina signos de puntuación y convierte a minúsculas
    palabras = re.findall(r'\b\w+\b', texto.lower())
    return Counter(palabras)

if __name__ == "__main__":
    ruta_pdf = 'Los Estudiantes Universitarios Deberían Usar Inteligencia Artificial.pdf'
    texto = extraer_texto_pdf(ruta_pdf)
    frecuencias = contar_palabras(texto)
    
    print("Frecuencia de palabras:")
    for palabra, cantidad in frecuencias.most_common():
        print(f"{palabra}: {cantidad}")
