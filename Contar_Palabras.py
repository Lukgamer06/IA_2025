import PyPDF2
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

ELIMINAR = {
    # Artículos
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'lo', 'al', 'del',
    'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'aquel', 'aquella', 'aquellos', 'aquellas',
    'mi', 'mis', 'tu', 'tus', 'su', 'sus', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras',
    'me', 'te', 'se', 'nos', 'os', 'le', 'les', 'lo',
    # Adjetivos
    'bueno', 'buena', 'buenos', 'buenas', 'malo', 'mala', 'malos', 'malas',
    'grande', 'grandes', 'pequeño', 'pequeña', 'pequeños', 'pequeñas',
    'nuevo', 'nueva', 'nuevos', 'nuevas', 'viejo', 'vieja', 'viejos', 'viejas',
    'primer', 'primera', 'primeros', 'primeras', 'último', 'última', 'últimos', 'últimas',
    'otro', 'otra', 'otros', 'otras', 'mismo', 'misma', 'mismos', 'mismas',
    'mucho', 'mucha', 'muchos', 'muchas', 'poco', 'poca', 'pocos', 'pocas',
    'todo', 'toda', 'todos', 'todas', 'algún', 'alguna', 'algunos', 'algunas',
    'ningún', 'ninguna', 'ningunos', 'ningunas', 'cada', 'cualquier', 'cualquiera', 'cualesquiera',
    'varios', 'varias', 'demasiado', 'demasiada', 'demasiados', 'demasiadas',
    'siguiente', 'siguientes', 'anterior', 'anteriores',
    'diferente', 'diferentes',
    'similar', 'similares', 'propio', 'propia', 'propios', 'propias',
    'cierto', 'cierta', 'ciertos', 'ciertas', 'seguro', 'segura', 'seguros', 'seguras',
    'importante', 'importantes', 'fácil', 'fáciles', 'difícil', 'difíciles',
    'rápido', 'rápida', 'rápidos', 'rápidas', 'lento', 'lenta', 'lentos', 'lentas',
    'alto', 'alta', 'altos', 'altas', 'bajo', 'baja', 'bajos', 'bajas',
    'claro', 'clara', 'claros', 'claras', 'oscuro', 'oscura', 'oscuros', 'oscuras',
    'fuerte', 'fuertes', 'débil', 'débiles', 'rico', 'rica', 'ricos', 'ricas', 'pobre', 'pobres',
    'feliz', 'felices', 'triste', 'tristes', 'joven', 'jóvenes', 'antiguo', 'antigua', 'antiguos', 'antiguas',
    'moderno', 'moderna', 'modernos', 'modernas', 'clásico', 'clásica', 'clásicos', 'clásicas',
    'famoso', 'famosa', 'famosos', 'famosas', 'desconocido', 'desconocida', 'desconocidos', 'desconocidas',
    'simple', 'simples', 'complejo', 'compleja', 'complejos', 'complejas',
    'barato', 'barata', 'baratos', 'baratas', 'caro', 'cara', 'caros', 'caras',
    # Adverbios
    'muy', 'más', 'menos', 'bien', 'mal', 'aquí', 'allí', 'ahí', 'allá', 'acá',
    'siempre', 'nunca', 'jamás', 'pronto', 'tarde', 'temprano', 'ayer', 'hoy', 'mañana',
    'todavía', 'aún', 'ya', 'después', 'antes', 'luego', 'entonces', 'así',
    'quizá', 'quizás', 'tal vez', 'casi', 'apenas', 'bastante', 'demasiado',
    'sólo', 'solamente', 'junto', 'lejos', 'cerca', 'encima', 'debajo', 'dentro', 'fuera',
    'arriba', 'abajo', 'adelante', 'atrás', 'alrededor', 'adentro', 'afuera',
    # Conectores y otros
    'y', 'o', 'pero', 'porque', 'aunque', 'si', 'cuando', 'mientras', 'como', 'donde',
    'que', 'de', 'a', 'en', 'con', 'por', 'para', 'sin', 'sobre', 'entre', 'hasta', 'desde',
    'tras', 'durante', 'según', 'contra', 'mediante', 'excepto', 'salvo', 'incluso', 'además', 'sino',
    'luego', 'entonces', 'así', 'así que', 'de hecho', 'en fin', 'en resumen', 'en conclusión', 'por lo tanto',
    'es decir', 'o sea', 'por ejemplo', 'en cambio', 'sin embargo', 'no obstante', 'a pesar de',
    'mientras tanto', 'al mismo tiempo', 'de repente', 'de nuevo', 'en seguida', 'por fin', 'a continuación', 'a propósito', 'aun así',
    'en realidad', 'de hecho', 'en general', 'en particular', 'en serio', 'a menudo', 'de vez en cuando', 'a veces', 'frecuentemente', 'constantemente', 'regularmente',
    'rápidamente', 'lentamente', 'cuidadosamente', 'fácilmente', 'difícilmente', 'claramente', 'obviamente', 'seguramente', 'probablemente', 'posiblemente', 'definitivamente',
    'especialmente', 'particularmente', 'generalmente', 'normalmente', 'habitualmente', 'usualmente',
    'finalmente', 'eventualmente', 'temporalmente', 'permanentemente', 'momentáneamente', 'provisionalmente',
    'actualmente', 'recientemente', 'anteriormente', 'previamente', 'posteriormente', 'ultimamente',
    'anteayer', 'pasado', 'próximo', 'futuro', 'presente',
    'delante', 'detrás', 'separado', 'alejado'
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
    """Cuenta cuántas veces aparece cada palabra en el texto, excluyendo artículos, adjetivos y adverbios."""
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in ELIMINAR]
    return Counter(palabras_filtradas)

def graficar_top_palabras(frecuencias, top_n):
    """Grafica el top N palabras más repetidas en una gráfica de barras."""
    top = frecuencias.most_common(top_n)
    palabras = [p for p, _ in top]
    cantidades = [c for _, c in top]
    plt.figure(figsize=(10, 6))
    plt.bar(palabras, cantidades, color='skyblue')
    plt.xlabel('Palabra')
    plt.ylabel('Frecuencia')
    plt.title(f'Top {top_n} palabras más repetidas')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def crear_wordcloud(frecuencias, top_n):
    """Crea y muestra una WordCloud con el top N palabras más repetidas."""
    top = dict(frecuencias.most_common(top_n))
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'WordCloud Top {top_n} palabras más repetidas')
    plt.show()

if __name__ == "__main__":
    ruta_pdf = 'Los Estudiantes Universitarios Deberían Usar Inteligencia Artificial.pdf'
    texto = extraer_texto_pdf(ruta_pdf)
    frecuencias = contar_palabras(texto)

    top_n = 50
    graficar_top_palabras(frecuencias, top_n)
    crear_wordcloud(frecuencias, top_n)
