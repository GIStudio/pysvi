# street_view/utils/photo.py
from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import messagebox
import pysolar.solar as Sun
import datetime
import pytz

class Photo:

    def __init__(self, file_path=None, description="", longitude=None, latitude=None, capture_time=None):
        self.file_path = file_path
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.capture_time = capture_time
        self.image = None

        if capture_time and capture_time.tzinfo is None:
            # Add UTC timezone if no timezone is provided
            self.capture_time = capture_time.replace(tzinfo=datetime.timezone.utc)

        if file_path:
            self.read_image(file_path)
    
    def read_image(self, file_path):
        """Read an image from a file path."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such file: '{file_path}'")
        
        self.image = Image.open(file_path)
        print(f"Image {file_path} read successfully.")
    
    def show_image(self):
        """Display the image in a pop-up window with resizing."""
        if self.image:
            # Resize image to 1024x768
            max_width, max_height = 1024, 768
            img_width, img_height = self.image.size

            if img_width > max_width or img_height > max_height:
                # Calculate the new size preserving the aspect ratio
                aspect_ratio = img_width / img_height
                if aspect_ratio > 1:
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
                
                self.image = self.image.resize((new_width, new_height), Image.ANTIALIAS)

            # Create a Tkinter window to display the image
            root = tk.Tk()
            root.title("Image Viewer")
            img = ImageTk.PhotoImage(self.image)
            panel = tk.Label(root, image=img)
            panel.pack(side="top", fill="both", expand="yes")

            # Run the Tkinter event loop
            root.mainloop()
        else:
            print("No image to display.")
            
    def __repr__(self):
        if self.image:
            size = self.get_image_size()
            file_size = self.get_file_size()
            return (f"Photo(file_path={self.file_path}, "
                    f"description={self.description}, "
                    f"longitude={self.longitude}, "
                    f"latitude={self.latitude}, "
                    f"capture_time={self.capture_time}, "
                    f"size={size}, file_size={file_size} bytes)")
        else:
            return (f"Photo(file_path={self.file_path}, "
                    f"description={self.description}, "
                    f"longitude={self.longitude}, "
                    f"latitude={self.latitude}, "
                    f"capture_time={self.capture_time})")
    
    def get_image_aspect_ratio(self):
        """Get the aspect_ratio"""
        # 计算宽高比
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.aspect_ratio = self.width / self.height
        print(f'width: {self.width}, height: {self.height}')
        print(f"图像的宽高比为: {self.aspect_ratio}")
        return self.aspect_ratio
    
    def get_image_size(self):
        """Get the size (width, height) of the image."""
        if self.image:
            return self.image.size
        else:
            raise ValueError("No image loaded.")
    
    def get_file_size(self):
        """Get the file size of the image in bytes."""
        if self.file_path:
            return os.path.getsize(self.file_path)
        else:
            raise ValueError("No file path provided.")
    
    def get_sun_altitude_azimuth(self):
        """Get the sun's altitude and azimuth at the specified time and location."""
        if self.latitude is None or self.longitude is None or self.capture_time is None:
            raise ValueError("Latitude, longitude, and capture time must be provided.")
        
        sun_altitude = Sun.get_altitude(self.latitude, self.longitude, self.capture_time)
        sun_azimuth = Sun.get_azimuth(self.latitude, self.longitude, self.capture_time)
        return sun_altitude, sun_azimuth
    
    def update_attributes(self, file_path=None, description=None, longitude=None, latitude=None, capture_time=None):
        """Update the attributes of the Photo object."""
        if file_path is not None:
            self.file_path = file_path
            self.read_image(file_path)  # Re-read the image if file_path is updated
        if description is not None:
            self.description = description
        if longitude is not None:
            self.longitude = longitude
        if latitude is not None:
            self.latitude = latitude
        if capture_time is not None:
            if capture_time.tzinfo is None:
                # Add UTC timezone if no timezone is provided
                capture_time = capture_time.replace(tzinfo=datetime.timezone.utc)
            self.capture_time = capture_time