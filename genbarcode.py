import requests
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import os

# Define the API URL
api_url = 'https://api.inventory.oudommeng.tech/items'

# Create an output directory for barcodes
output_dir = "barcodes"
os.makedirs(output_dir, exist_ok=True)

# Font for the text (adjust path if necessary)
# Adjust this path for Windows/Mac
font_path = "font/KantumruyPro-Regular.ttf"
font_size = 16


def fetch_items(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []


def generate_barcode_with_name_and_code(item_name, item_code, output_dir, font_path, font_size):
    try:
        # Generate barcode
        barcode_class = barcode.get_barcode_class('code128')
        barcode_obj = barcode_class(item_code, writer=ImageWriter())
        barcode_image_path = os.path.join(
            output_dir, f"{item_code}_{item_name}")
        barcode_obj.save(barcode_image_path)

        # Load the generated barcode image
        barcode_image = Image.open(barcode_image_path)
        barcode_width, barcode_height = barcode_image.size

        # Prepare to add text (item code and name)
        font = ImageFont.truetype(font_path, font_size)
        code_width, code_height = font.getsize(item_code)
        name_width, name_height = font.getsize(item_name)

        total_height = barcode_height + code_height + name_height + 20  # 20px padding

        # Create a new image with extra space for text
        combined_image = Image.new(
            "RGB", (barcode_width, total_height), "white")
        draw = ImageDraw.Draw(combined_image)

        # Paste the barcode in the image
        combined_image.paste(barcode_image, (0, 0))

        # Draw the item code below the barcode
        code_x = (barcode_width - code_width) // 2
        code_y = barcode_height + 5
        draw.text((code_x, code_y), item_code, font=font, fill="black")

        # Draw the item name below the item code
        name_x = (barcode_width - name_width) // 2
        name_y = code_y + code_height + 5
        draw.text((name_x, name_y), item_name, font=font, fill="black")

        # Save the final image
        final_image_path = os.path.join(output_dir, f"{item_code}.png")
        combined_image.save(final_image_path)
        print(f"Barcode with name and code saved: {final_image_path}")

        # Remove the temporary barcode image
        os.remove(barcode_image_path)
    except Exception as e:
        print(f"Error generating barcode for {item_code}: {e}")


def main():
    # Fetch items from API
    items = fetch_items(api_url)
    if not items:
        print("No items fetched from the API.")
        return

    # Generate barcodes for each item
    for item in items:
        item_name = item.get('item_name', 'UNKNOWN')
        item_code = item.get('code', 'UNKNOWN')
        generate_barcode_with_name_and_code(
            item_name, item_code, output_dir, font_path, font_size)


if __name__ == "__main__":
    main()
