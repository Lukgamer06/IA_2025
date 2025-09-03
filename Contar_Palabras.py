# Programa para contar la frecuencia de cada palabra en un documento PDF, excluyendo artículos y adjetivos

import PyPDF2
import re
from collections import Counter

# Lista básica de artículos y adjetivos comunes en español
ARTICULOS_Y_ADJETIVOS = {
    # Artículos definidos e indefinidos
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
    # Adjetivos comunes
    'bueno', 'buena', 'buenos', 'buenas', 'malo', 'mala', 'malos', 'malas',
    'grande', 'grandes', 'pequeño', 'pequeña', 'pequeños', 'pequeñas',
    'nuevo', 'nueva', 'nuevos', 'nuevas', 'viejo', 'vieja', 'viejos', 'viejas',
    'primer', 'primera', 'primeros', 'primeras', 'último', 'última', 'últimos', 'últimas',
    'otro', 'otra', 'otros', 'otras', 'mismo', 'misma', 'mismos', 'mismas',
    'mucho', 'mucha', 'muchos', 'muchas', 'poco', 'poca', 'pocos', 'pocas',
    'todo', 'toda', 'todos', 'todas', 'algún', 'alguna', 'algunos', 'algunas',
    'ningún', 'ninguna', 'ningunos', 'ningunas', 'cada', 'cualquier', 'cualquiera'
}

def extraer_texto_pdf(ruta_pdf):
    """Extrae el texto de todas las páginas de un archivo PDF."""
    texto = ""
    with open(ruta_pdf, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text() + " "
    return texto

def contar_palabras(texto):
    """Cuenta cuántas veces aparece cada palabra en el texto, excluyendo artículos y adjetivos."""
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in ARTICULOS_Y_ADJETIVOS]
    return Counter(palabras_filtradas)

if __name__ == "__main__":
    ruta_pdf = 'Los Estudiantes Universitarios Deberían Usar Inteligencia Artificial.pdf'
    texto = extraer_texto_pdf(ruta_pdf)
    frecuencias = contar_palabras(texto)
    
    print("Frecuencia de palabras (sin artículos ni adjetivos):")
    for palabra, cantidad in frecuencias.most_common():
        print(f"{palabra}: {cantidad}")
