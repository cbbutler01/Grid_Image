import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

def scrape_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table
    table = soup.find('table')
    if not table:
        raise ValueError("No table found on the page")

    data = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all('td')
        if len(cells) == 3:
            x = int(cells[0].text.strip())
            char = cells[1].text.strip()
            y = int(cells[2].text.strip())
            data.append((x, char, y))
    return data

def create_character_grid(table_data, grid_size, cell_size=50):
    """
    table_data: List of tuples (x, char, y)
    grid_size: (width, height) in cells
    cell_size: Pixel size of each cell
    """
    width, height = grid_size
    canvas_width = width * cell_size
    canvas_height = height * cell_size

    # Create a blank canvas
    image = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Use a default font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Place characters on the grid
    for x, char, y in table_data:
        x_pixel = x * cell_size
        y_pixel = y * cell_size

        # Center text in the cell
        text_width, text_height = draw.textsize(char, font=font)
        text_x = x_pixel + (cell_size - text_width) // 2
        text_y = y_pixel + (cell_size - text_height) // 2

        draw.text((text_x, text_y), char, fill="black", font=font)

    return image

# Main workflow
google_docs_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYHYEzeNJklb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

# Step 1: Scrape the table data
table_data = scrape_table_data(google_docs_url)

# Step 2: Define the grid size
grid_size = (10, 10)  # Adjust as per the range of x and y coordinates

# Step 3: Create the grid image
character_grid_image = create_character_grid(table_data, grid_size)

# Step 4: Save or display the image
output_path = "character_grid.png"
character_grid_image.save(output_path)
character_grid_image.show()

