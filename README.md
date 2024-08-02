# Text Clean
## Librería de Limpieza de Texto en Español para Procesamiento de Lenguaje Natural (NLP)

Esta es una librería de Python diseñada para facilitar la limpieza de texto en español para aplicaciones de Procesamiento de Lenguaje Natural (NLP). Proporciona una serie de funciones y utilidades para preprocesar y limpiar texto en español, lo que puede mejorar la calidad y el rendimiento de los modelos de NLP.

## Características principales

- Eliminación de caracteres especiales y puntuación.
- Conversión de texto a minúsculas.
- Eliminación de stopwords en español.
- Normalización de palabras mediante lematización.
- Eliminación de números y símbolos.
- Tokenización de texto en palabras individuales.

## Instalación

Puedes instalar esta librería utilizando pip:

```
pip install git+https://github.com/gerickt/text_clean.git   
```

## Uso

A continuación se muestra un ejemplo básico de cómo utilizar la librería:

```python
import text_clean as tc

# Cargar stopwords personalizadas y diccionario de correcciones
custom_stopwords = tc.load_stopwords('ruta/a/custom_stopwords.txt')
corrections_dict = tc.load_corrections('ruta/a/corrections.json')

# Combinar stopwords personalizadas con las por defecto
stopwords_set = tc.default_stopwords.union(custom_stopwords)

# Asumiendo que 'df' es tu DataFrame y 'title' la columna de texto a limpiar
df = tc.process_text_column(df, 'title', corrections_dict, stopwords_set)
```

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.
