import struct

def generate_bitmap(n, filename):
    # BMP Header
    file_size = 14 + 40 + n * n * 3
    bmp_header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, 54)
    
    # DIB Header (BITMAPINFOHEADER)
    dib_header = struct.pack('<IIIHHIIIIII', 40, n, n, 1, 24, 0, n * n * 3, 2835, 2835, 0, 0)
    
    # Pixel Data
    pixel_data = bytearray()
    for y in range(n):
        for x in range(n):
            if (x + y) % 2 == 0:
                pixel_data.extend([255, 255, 255])  # White pixel
            else:
                pixel_data.extend([0, 0, 0])  # Black pixel
    
    # Write to file
    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header)
        f.write(pixel_data)

# Example usage
generate_bitmap(256, 'output.bmp')
