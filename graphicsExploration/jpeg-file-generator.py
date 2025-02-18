#'jpeg-file-generator.py'
# written 2/18/2025
# GitHub Copilot
# Rich W.

from PIL import Image

def generate_jpeg(n, filename):
    # Create a new image with RGB mode
    image = Image.new('RGB', (n, n))
    
    # Pixel Data
    pixels = image.load()
    for y in range(n):
        for x in range(n):
            if (x + y) % 2 == 0:
                pixels[x, y] = (255, 255, 255)  # White pixel
            else:
                pixels[x, y] = (0, 0, 0)  # Black pixel
    
    # Save to file
    image.save(filename, 'JPEG')

# Example usage
generate_jpeg(256, 'output.jpg')
