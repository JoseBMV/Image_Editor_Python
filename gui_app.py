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
        self.root.geometry("1024x768")  # Larger initial size
        
        # Modern theme configurations
        self.themes = {
            'light': {
                'bg': '#f0f2f5',
                'fg': '#2e2e2e',
                'text_bg': '#ffffff',
                'text_fg': '#2e2e2e',
                'button_bg': '#ffffff',
                'button_fg': '#2e2e2e',
                'accent': '#007bff',
                'hover': '#e2e6ea',
                'frame_bg': '#ffffff',
                'select_bg': '#0d6efd',
                'select_fg': '#ffffff'
            },
            'dark': {
                'bg': '#1a1a1a',
                'fg': '#ffffff',
                'text_bg': '#2d2d2d',
                'text_fg': '#ffffff',
                'button_bg': '#333333',
                'button_fg': '#ffffff',
                'accent': '#0d6efd',
                'hover': '#404040',
                'frame_bg': '#2d2d2d',
                'select_bg': '#0d6efd',
                'select_fg': '#ffffff'
            }
        }
        
        # Configure weight for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main frame configuration
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=3)  # Image column
        self.main_frame.grid_columnconfigure(1, weight=1)  # Controls column
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Modern style configuration
        self.style = ttk.Style()
        self.style.configure('Modern.TButton',
                           padding=10,
                           font=('Segoe UI', 9))
        self.style.configure('Modern.TFrame',
                           background='#f0f2f5')
        self.style.configure('Modern.TLabelframe',
                           padding=10)
        self.style.configure('Modern.TLabelframe.Label',
                           font=('Segoe UI', 9, 'bold'))
        
        # Update button frame with modern layout
        self.button_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.button_frame.grid_columnconfigure(6, weight=1)  # Make last column expandable
        
        # Modern buttons with icons
        self.btn_load = ttk.Button(self.button_frame, text="📂 Cargar", 
                                  style='Modern.TButton', command=self.load_image)
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_save = ttk.Button(self.button_frame, text="💾 Guardar", 
                                  style='Modern.TButton', command=self.save_image)
        self.btn_save.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_theme = ttk.Button(self.button_frame, text="🌓 Tema", 
                                   style='Modern.TButton', command=self.toggle_theme)
        self.btn_theme.grid(row=0, column=2, padx=5, pady=5)
        
        # Filter controls with modern style
        filter_frame = ttk.LabelFrame(self.button_frame, text="Filtros", 
                                    style='Modern.TLabelframe')
        filter_frame.grid(row=0, column=3, padx=5, pady=5)
        
        self.filter_var = tk.StringVar(value="None")
        self.filter_combo = ttk.Combobox(
            filter_frame, 
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
        self.filter_combo.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_apply = ttk.Button(filter_frame, text="✨ Aplicar", 
                                   style='Modern.TButton', command=self.apply_selected_filter)
        self.btn_apply.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Image frame with border and shadow effect
        self.image_frame = ttk.LabelFrame(self.main_frame, text="Imagen", 
                                        style='Modern.TLabelframe')
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create container for image and navigation
        self.image_container = ttk.Frame(self.image_frame)
        self.image_container.pack(expand=True, fill="both")
        
        self.image_label = ttk.Label(self.image_container)
        self.image_label.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Navigation panel at the bottom of image frame
        self.nav_frame = ttk.Frame(self.image_container, style='Modern.TFrame')
        self.nav_frame.pack(side=tk.BOTTOM, fill="x", padx=5, pady=5)
        
        # Left side: zoom controls
        self.zoom_controls = ttk.Frame(self.nav_frame, style='Modern.TFrame')
        self.zoom_controls.pack(side=tk.LEFT, padx=5)
        
        self.btn_zoom_in = ttk.Button(self.zoom_controls, text="🔍+", 
                                     style='Modern.TButton', command=self.zoom_in)
        self.btn_zoom_in.pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = ttk.Label(self.zoom_controls, text="100%",
                                   font=('Segoe UI', 9))
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        self.btn_zoom_out = ttk.Button(self.zoom_controls, text="🔍-", 
                                      style='Modern.TButton', command=self.zoom_out)
        self.btn_zoom_out.pack(side=tk.LEFT, padx=2)
        
        self.btn_reset = ttk.Button(self.zoom_controls, text="↺", 
                                   style='Modern.TButton', command=self.reset_view)
        self.btn_reset.pack(side=tk.LEFT, padx=2)
        
        # Right side: thumbnail
        self.thumbnail_frame = ttk.Frame(self.nav_frame, style='Modern.TFrame')
        self.thumbnail_frame.pack(side=tk.RIGHT, padx=5)
        self.thumbnail_label = ttk.Label(self.thumbnail_frame)
        self.thumbnail_label.pack()

        # Right side panel (only metadata)
        self.side_panel = ttk.Frame(self.main_frame, style='Modern.TFrame')
        self.side_panel.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Metadata panel
        self.metadata_frame = ttk.LabelFrame(self.side_panel, text="Metadatos", 
                                           style='Modern.TLabelframe')
        self.metadata_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.metadata_text = tk.Text(self.metadata_frame, width=30, height=10,
                                   font=('Segoe UI', 9))
        self.metadata_text.pack(expand=True, fill="both", padx=5, pady=5)

        # Initialize other attributes
        self.current_theme = 'light'
        self.original_image = None
        self.current_image = None
        self.apply_theme()

        # Configuración de zoom y navegación
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        self.pan_x = 0
        self.pan_y = 0
        self.is_panning = False
        
        # Add display size configuration
        self.display_area = (600, 400)  # Default display area size
        self.thumbnail_size = (100, 100)  # Smaller thumbnail

        # Eventos de mouse y teclado
        self.image_label.bind('<ButtonPress-1>', self.start_pan)
        self.image_label.bind('<B1-Motion>', self.pan)
        self.image_label.bind('<ButtonRelease-1>', self.stop_pan)
        self.image_label.bind('<MouseWheel>', self.mouse_wheel)
        
        # Atajos de teclado
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_view())
        
        # Selección de área para zoom
        self.image_label.bind('<Control-Button-1>', self.start_area_selection)
        self.selection_rect = None
        self.start_x = None
        self.start_y = None

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme with modern styling"""
        theme = self.themes[self.current_theme]
        
        # Configure root window
        self.root.configure(bg=theme['bg'])
        
        # Configure text widget with modern font and colors
        self.metadata_text.configure(
            bg=theme['text_bg'],
            fg=theme['text_fg'],
            insertbackground=theme['fg'],
            selectbackground=theme['select_bg'],
            selectforeground=theme['select_fg'],
            font=('Segoe UI', 9),
            relief="flat",
            borderwidth=0
        )
        
        # Update ttk styles with modern colors
        self.style.configure('Modern.TFrame', 
                           background=theme['bg'])
        self.style.configure('Modern.TLabelframe', 
                           background=theme['bg'])
        self.style.configure('Modern.TLabelframe.Label', 
                           foreground=theme['fg'],
                           background=theme['bg'])
        self.style.configure('Modern.TButton', 
                           background=theme['button_bg'],
                           foreground=theme['button_fg'])
        self.style.configure('TCombobox', 
                           fieldbackground=theme['text_bg'],
                           background=theme['button_bg'],
                           foreground=theme['text_fg'])
        self.style.configure('TLabel', 
                           background=theme['bg'],
                           foreground=theme['fg'])
        
        # Configure hover effects
        self.style.map('Modern.TButton',
                      background=[('active', theme['hover'])],
                      foreground=[('active', theme['fg'])])
        self.style.map('TCombobox',
                      fieldbackground=[('readonly', theme['text_bg'])],
                      selectbackground=[('readonly', theme['select_bg'])],
                      selectforeground=[('readonly', theme['select_fg'])])
        
        # Update frame backgrounds
        for frame in [self.main_frame, self.button_frame, self.side_panel, 
                     self.nav_frame, self.metadata_frame, self.image_frame]:
            frame.configure(style='Modern.TFrame')
        
        # Update image label background
        self.image_label.configure(style='TLabel')
        
        # Update combobox colors
        self.filter_combo.configure(style='TCombobox')
        
        # Force update of all widgets
        self.root.update_idletasks()

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

    def save_image(self):
        """Save the current filtered image"""
        if self.current_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                cv2.imwrite(file_path, self.current_image)

    def calculate_display_size(self, img_width, img_height):
        """Calculate the display size maintaining aspect ratio"""
        display_width, display_height = self.display_area
        
        # Calculate aspect ratios
        img_aspect = img_width / img_height
        display_aspect = display_width / display_height
        
        if img_aspect > display_aspect:
            # Image is wider than display area
            new_width = display_width
            new_height = int(display_width / img_aspect)
        else:
            # Image is taller than display area
            new_height = display_height
            new_width = int(display_height * img_aspect)
            
        return (new_width, new_height)

    def update_display(self, img):
        if img is None:
            return
            
        processed_img, metadata = process_image(img)
        img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Get original image dimensions
        orig_width, orig_height = img_pil.size
        
        # Calculate display size maintaining aspect ratio
        display_size = self.calculate_display_size(orig_width, orig_height)
        
        # Apply zoom to the calculated display size
        zoomed_size = (int(display_size[0] * self.zoom_factor), 
                      int(display_size[1] * self.zoom_factor))
        
        # Resize image
        zoomed_img = img_pil.resize(zoomed_size, Image.Resampling.LANCZOS)
        
        # Create canvas centered
        canvas = Image.new('RGB', self.display_area, self.themes[self.current_theme]['bg'])
        
        # Calculate centering offset
        paste_x = (self.display_area[0] - zoomed_size[0]) // 2 + self.pan_x
        paste_y = (self.display_area[1] - zoomed_size[1]) // 2 + self.pan_y
        
        # Adjust pasting coordinates to keep image visible
        paste_x = max(min(paste_x, self.display_area[0]), -zoomed_size[0])
        paste_y = max(min(paste_y, self.display_area[1]), -zoomed_size[1])
        
        # Paste image onto canvas
        canvas.paste(zoomed_img, (int(paste_x), int(paste_y)))
        
        # Convert to PhotoImage and display
        img_tk = ImageTk.PhotoImage(canvas)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk
        
        # Update thumbnail
        thumbnail = img_pil.copy()
        thumbnail.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
        
        # Center thumbnail in its frame
        thumb_canvas = Image.new('RGB', self.thumbnail_size, self.themes[self.current_theme]['bg'])
        thumb_x = (self.thumbnail_size[0] - thumbnail.width) // 2
        thumb_y = (self.thumbnail_size[1] - thumbnail.height) // 2
        thumb_canvas.paste(thumbnail, (thumb_x, thumb_y))
        
        thumb_tk = ImageTk.PhotoImage(thumb_canvas)
        self.thumbnail_label.configure(image=thumb_tk)
        self.thumbnail_label.image = thumb_tk
        
        # Update metadata
        self.update_metadata(metadata)

    def update_metadata(self, metadata):
        """Update the metadata display with the given metadata"""
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

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor *= 1.2
            self.update_zoom_label()
            self.update_display(self.current_image)
    
    def zoom_out(self):
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor /= 1.2
            self.update_zoom_label()
            self.update_display(self.current_image)
    
    def reset_view(self):
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.update_zoom_label()
        self.update_display(self.current_image)
    
    def update_zoom_label(self):
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_label.configure(text=f"{zoom_percent}%")
    
    def start_pan(self, event):
        if not event.state & 4:  # No Control pressed
            self.is_panning = True
            self.last_x = event.x
            self.last_y = event.y
    
    def pan(self, event):
        if self.is_panning:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.pan_x += dx
            self.pan_y += dy
            self.last_x = event.x
            self.last_y = event.y
            self.update_display(self.current_image)
    
    def stop_pan(self, event):
        self.is_panning = False
    
    def mouse_wheel(self, event):
        if event.state & 4:  # Control pressed
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out
    
    def start_area_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.selection_rect:
            self.image_label.delete(self.selection_rect)
        self.selection_rect = None
        self.image_label.bind('<B1-Motion>', self.update_selection)
        self.image_label.bind('<ButtonRelease-1>', self.end_area_selection)
    
    def update_selection(self, event):
        if self.selection_rect:
            self.image_label.delete(self.selection_rect)
        self.selection_rect = self.image_label.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )
    
    def end_area_selection(self, event):
        if self.selection_rect:
            # Calcular zoom basado en el área seleccionada
            width = abs(event.x - self.start_x)
            height = abs(event.y - self.start_y)
            if width > 10 and height > 10:  # Mínimo tamaño de selección
                zoom_x = self.image_label.winfo_width() / width
                zoom_y = self.image_label.winfo_height() / height
                self.zoom_factor = min(zoom_x, zoom_y, self.max_zoom)
                self.pan_x = -(self.start_x + event.x) / 2
                self.pan_y = -(self.start_y + event.y) / 2
                self.update_zoom_label()
                self.update_display(self.current_image)
            
            self.image_label.delete(self.selection_rect)
            self.selection_rect = None
        
        self.image_label.bind('<B1-Motion>', self.pan)
        self.image_label.bind('<ButtonRelease-1>', self.stop_pan)

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
