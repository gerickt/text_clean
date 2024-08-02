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
pip install git+https://github.com/gerickt/text-clean.git   
```

## Uso

A continuación se muestra un ejemplo básico de cómo utilizar la librería:

```python
import text_clean

# Crear una instancia del limpiador de texto
cleaner = text_clean.TextCleaner()

# Limpiar un texto de ejemplo
text = "¡Hola! Este es un ejemplo de texto en español."
clean_text = cleaner.clean(text)

print(clean_text)
# Output: "hola ejemplo texto español"
```

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.
