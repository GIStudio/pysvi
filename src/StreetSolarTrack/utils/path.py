from .photo import Photo
import datetime

class Path:
    def __init__(self, path_id, description=""):
        self.path_id = path_id
        self.description = description
        self.photos = []

    def add_photo(self, photo):
        """Add a photo to the path."""
        if isinstance(photo, Photo):
            self.photos.append(photo)
        else:
            raise ValueError("The provided object is not an instance of Photo.")

    def find_all_photos(self):
        """Find all photos associated with this path and sort them by capture time."""
        self.photos.sort(key=lambda photo: photo.capture_time)
        return self.photos

    def calculate_light_variation(self):
        """Calculate the light variation based on the sun's altitude and azimuth for each photo."""
        for photo in self.photos:
            sun_altitude, sun_azimuth = photo.get_sun_altitude_azimuth()
            print(f"Photo at {photo.capture_time}: Sun Altitude={sun_altitude}, Sun Azimuth={sun_azimuth}")

    def __repr__(self):
        return f"Path(path_id={self.path_id}, description={self.description}, photos_count={len(self.photos)})"

# Example usage:
if __name__ == "__main__":
    path = Path(path_id=1, description="Example Path")

    photo1 = Photo(file_path="path/to/photo1.jpg", longitude=12.34, latitude=56.78, capture_time=datetime.datetime(2023, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc))
    photo2 = Photo(file_path="path/to/photo2.jpg", longitude=12.34, latitude=56.78, capture_time=datetime.datetime(2023, 1, 1, 11, 0, 0, tzinfo=datetime.timezone.utc))

    path.add_photo(photo1)
    path.add_photo(photo2)

    all_photos = path.find_all_photos()
    print(f"All photos in path: {all_photos}")

    path.calculate_light_variation()