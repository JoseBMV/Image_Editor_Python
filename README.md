# Procesador de Imágenes con Python

Una aplicación moderna de procesamiento de imágenes con interfaz gráfica desarrollada en Python.

![Vista previa de la aplicación](./docs/preview.png)

## 🚀 Características

- Interfaz gráfica moderna y responsive
- Temas claro y oscuro
- Múltiples filtros de imagen:
  - Efectos básicos (Blur, Sharpen, Edge Detect)
  - Efectos artísticos (Sepia, Sketch, HDR, Watercolor)
  - Efectos de color (Grayscale, Invert)
  - Limpieza de ruido (Denoise, Median Blur, Bilateral)
- Herramientas de navegación:
  - Zoom con rueda del ratón
  - Pan con click y arrastre
  - Selección de área para zoom
  - Vista en miniatura
- Metadatos de imagen en tiempo real
- Guardado de imágenes procesadas

## 📋 Requisitos

```bash
Python 3.8 o superior
opencv-python
numpy
Pillow
tkinter (incluido en Python)
```

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/camera_vision_python.git
cd camera_vision_python
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

Para iniciar la aplicación:
```bash
python gui_app.py
```

### Atajos de Teclado

- `Ctrl + +`: Aumentar zoom
- `Ctrl + -`: Disminuir zoom
- `Ctrl + 0`: Restablecer zoom
- `Ctrl + Click`: Seleccionar área para zoom

### Navegación

- Click y arrastre para mover la imagen
- Rueda del ratón con Ctrl para zoom
- Miniatura para vista general
- Botones de zoom para control preciso

## 🛠️ Filtros Disponibles

### Efectos
- Blur (Desenfoque)
- Sharpen (Nitidez)
- Edge Detect (Detección de bordes)
- Grayscale (Escala de grises)
- Sepia
- Invert (Inversión)
- Sketch (Dibujo)
- HDR
- Emboss (Relieve)
- Watercolor (Acuarela)
- Cartoon (Caricatura)
- Winter (Efecto invierno)
- Summer (Efecto verano)

### Limpieza de Ruido
- Denoise Normal
- Denoise Strong
- Median Blur
- Bilateral
- Conservative

## 📊 Metadatos

La aplicación muestra información detallada de la imagen:
- Dimensiones
- Tamaño en MB
- Color promedio
- Rango de valores
- Desviación estándar
- Tipo de datos

## 🎨 Temas

- Tema Claro: Diseño moderno con fondo claro
- Tema Oscuro: Modo nocturno con contraste optimizado

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee las directrices de contribución antes de enviar un pull request.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ✨ Agradecimientos

- OpenCV por las herramientas de procesamiento de imágenes
- Pillow por el manejo de imágenes
- Tkinter por la interfaz gráfica
