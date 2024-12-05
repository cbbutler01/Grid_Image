from PIL import Image, ImageDraw

def create_grid_image(grid_data, cell_size=50, colors=None):
    # Set default colors if not provided
    if colors is None:
        colors = {
            0: (255, 255, 255),  # White for 0
            1: (0, 0, 0),        # Black for 1
            # Add more mappings if needed
        }

    # Get dimensions
    rows = len(grid_data)
    cols = len(grid_data[0])

    # Create an image
    img_width = cols * cell_size
    img_height = rows * cell_size
    image = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            cell_value = grid_data[row][col]
            color = colors.get(cell_value, (200, 200, 200))  # Default gray for undefined
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            draw.rectangle([x0, y0, x1, y1], fill=color)

    return image

def parse_document_with_images(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            image_path = parts[0]  # Image file name
            row, col = map(int, parts[1:])  # Coordinates
            coordinates.append((image_path, row, col))
    return coordinates
