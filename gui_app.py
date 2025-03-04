import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from example import read_image, process_image, apply_filter

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador de Imágenes")
        self.root.geometry("800x600")
        
        # Theme configurations
        self.themes = {
            'light': {
                'bg': 'white',
                'fg': 'black',
                'text_bg': 'white',
                'text_fg': 'black',
                'button_bg': '#f0f0f0'
            },
            'dark': {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'text_bg': '#3b3b3b',
                'text_fg': '#ffffff',
                'button_bg': '#404040'
            }
        }
        self.current_theme = 'light'
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W))
        
        # Buttons
        self.btn_load = ttk.Button(self.button_frame, text="Cargar Imagen", command=self.load_image)
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_theme = ttk.Button(self.button_frame, text="🌓 Cambiar Tema", command=self.toggle_theme)
        self.btn_theme.grid(row=0, column=1, padx=5, pady=5)
        
        # Add filter controls after the load button
        self.filter_label = ttk.Label(self.button_frame, text="Filtro:")
        self.filter_label.grid(row=0, column=2, padx=5, pady=5)
        
        self.filter_var = tk.StringVar(value="None")
        self.filter_combo = ttk.Combobox(
            self.button_frame, 
            textvariable=self.filter_var,
            values=["None", 
                   "--- Efectos ---",
                   "Blur", "Sharpen", "Edge Detect", "Grayscale", "Sepia", 
                   "Invert", "Sketch", "HDR", "Emboss", "Watercolor", 
                   "Cartoon", "Winter", "Summer",
                   "--- Limpieza de Ruido ---",
                   "Denoise-Normal", "Denoise-Strong", "Median Blur",
                   "Bilateral", "Conservative"],
            state="readonly",
            width=15)
        self.filter_combo.grid(row=0, column=3, padx=5, pady=5)
        
        self.btn_apply = ttk.Button(self.button_frame, text="Aplicar Filtro", 
                                   command=self.apply_selected_filter)
        self.btn_apply.grid(row=0, column=4, padx=5, pady=5)
        
        # Store original image
        self.original_image = None
        
        # Image display
        self.image_label = ttk.Label(self.main_frame)
        self.image_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Metadata display
        self.metadata_frame = ttk.LabelFrame(self.main_frame, text="Metadatos", padding="5")
        self.metadata_frame.grid(row=1, column=2, padx=5, pady=5, sticky="n")
        
        self.metadata_text = tk.Text(self.metadata_frame, width=40, height=15)
        self.metadata_text.pack()
        
        self.current_image = None
        self.apply_theme()

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = self.themes[self.current_theme]
        
        # Configure root window
        self.root.configure(bg=theme['bg'])
        
        # Configure text widget
        self.metadata_text.configure(
            bg=theme['text_bg'],
            fg=theme['text_fg'],
            insertbackground=theme['fg']  # cursor color
        )
        
        # Configure style for ttk widgets
        style = ttk.Style()
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabelframe', background=theme['bg'])
        style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', background=theme['button_bg'])

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            img = read_image(file_path)
            if img is not None:
                self.original_image = img.copy()  # Store original
                self.current_image = img
                self.update_display(img)
                self.filter_var.set("None")  # Reset filter selection

    def apply_selected_filter(self):
        if self.original_image is not None:
            filtered_img = apply_filter(self.original_image.copy(), 
                                      self.filter_var.get())
            self.current_image = filtered_img
            self.update_display(filtered_img)

    def update_display(self, img):
        """Update image display and metadata"""
        processed_img, metadata = process_image(img)
        
        # Convert to PIL format for display
        img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Resize to fit window (keeping aspect ratio)
        display_size = (600, 400)
        img_pil.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Display image
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk
        
        # Update metadata display
        self.metadata_text.delete(1.0, tk.END)
        self.metadata_text.insert(tk.END, f"📏 Dimensiones: {metadata['shape']}\n")
        self.metadata_text.insert(tk.END, f"💾 Tamaño: {metadata['size_mb']} MB\n")
        self.metadata_text.insert(tk.END, f"🎨 Color promedio (BGR): {metadata['mean_color']}\n")
        self.metadata_text.insert(tk.END, f"📊 Rango de valores:\n")
        self.metadata_text.insert(tk.END, f"   Min: {metadata['min_value']}\n")
        self.metadata_text.insert(tk.END, f"   Max: {metadata['max_value']}\n")
        self.metadata_text.insert(tk.END, f"📈 Desviación estándar: {metadata['std_dev']}\n")
        self.metadata_text.insert(tk.END, f"🔢 Tipo de datos: {metadata['dtype']}\n")

        self.apply_theme()

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
