import numpy as np
import cv2
from typing import Optional, Tuple

def read_image(path: str) -> Optional[np.ndarray]:
    """
    Lee una imagen desde la ruta especificada.
    
    Args:
        path: Ruta al archivo de imagen
        
    Returns:
        Imagen como array de numpy o None si la lectura falla
    """
    return cv2.imread(path)

def process_image(image: np.ndarray) -> Tuple[np.ndarray, dict]:
    """
    Procesa la imagen de entrada y devuelve la imagen procesada con metadatos.
    
    Args:
        image: Imagen de entrada como array de numpy
        
    Returns:
        Tupla de imagen procesada y diccionario de metadatos
    """
    # Calculate additional image statistics
    metadata = {
        'shape': image.shape,
        'dtype': str(image.dtype),
        'size_mb': round(image.nbytes / (1024 * 1024), 2),
        'mean_color': tuple(map(round, cv2.mean(image)[:3])),
        'min_value': int(np.min(image)),
        'max_value': int(np.max(image)),
        'std_dev': round(float(np.std(image)), 2),
    }
    
    # Calculate histogram data
    hist_b = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([image], [2], None, [256], [0, 256])
    
    metadata['histogram'] = {
        'blue': hist_b.flatten().tolist(),
        'green': hist_g.flatten().tolist(),
        'red': hist_r.flatten().tolist()
    }
    
    return image, metadata

def apply_filter(image: np.ndarray, filter_name: str) -> np.ndarray:
    """
    Aplica un filtro específico a la imagen.
    
    Args:
        image: Imagen de entrada
        filter_name: Nombre del filtro a aplicar
        
    Returns:
        Imagen con el filtro aplicado
    """
    filters = {
        'Blur': lambda img: cv2.GaussianBlur(img, (5, 5), 0),
        'Sharpen': lambda img: cv2.filter2D(img, -1, np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])),
        'Edge Detect': lambda img: cv2.Canny(img, 100, 200),
        'Grayscale': lambda img: cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR),
        'Sepia': lambda img: cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                                          [0.349, 0.686, 0.168],
                                                          [0.393, 0.769, 0.189]])),
        'Invert': lambda img: cv2.bitwise_not(img),
        'Sketch': lambda img: cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)[0],
        'HDR': lambda img: cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15),
        'Emboss': lambda img: cv2.filter2D(img, -1, np.array([[-2,-1,0], [-1,1,1], [0,1,2]])),
        'Watercolor': lambda img: cv2.stylization(img, sigma_s=60, sigma_r=0.6),
        'Cartoon': lambda img: cv2.stylization(img, sigma_s=150, sigma_r=0.25),
        'Winter': lambda img: cv2.addWeighted(img, 1.3, cv2.cvtColor(np.zeros(img.shape, np.uint8), 
                                            cv2.COLOR_GRAY2BGR), 0, -30),
        'Summer': lambda img: cv2.addWeighted(img, 1.2, cv2.cvtColor(np.full(img.shape, 255, np.uint8), 
                                            cv2.COLOR_GRAY2BGR), 0.1, 0),
        'Denoise-Normal': lambda img: cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21),
        'Denoise-Strong': lambda img: cv2.fastNlMeansDenoisingColored(img, None, 20, 20, 7, 21),
        'Median Blur': lambda img: cv2.medianBlur(img, 5),
        'Bilateral': lambda img: cv2.bilateralFilter(img, 9, 75, 75),
        'None': lambda img: img
    }
    
    return filters.get(filter_name, filters['None'])(image)

def display_image(image: np.ndarray, window_name: str = "Image") -> None:
    """
    Muestra una imagen en una ventana.
    
    Args:
        image: Imagen para mostrar
        window_name: Nombre de la ventana
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Prueba del pipeline de procesamiento de imagen
    image_path = "test_image.jpg"  # Reemplazar con tu ruta de imagen
    
    # Leer imagen
    img = read_image(image_path)
    if img is None:
        print(f"Error: No se pudo leer la imagen de {image_path}")
        exit(1)
    
    # Procesar imagen
    processed_img, meta = process_image(img)
    print("Metadatos de la imagen:", meta)
    
    # Mostrar resultados
    display_image(processed_img)
