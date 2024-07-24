from PIL import Image, ImageDraw
import os
import math

def create_gradient(size, colors, angle):
    width, height = size
    # Create a larger canvas to accommodate the rotation
    diagonal = int(math.ceil(math.sqrt(width**2 + height**2)))
    extended_size = (diagonal, diagonal)
    
    base = Image.new('RGB', extended_size, colors[0])
    draw = ImageDraw.Draw(base)

    # Calculate gradient steps
    gradient_steps = diagonal

    # Draw the gradient
    for i in range(gradient_steps):
        ratio = i / gradient_steps
        if ratio < 0.46:
            r = int(colors[0][0] * (1 - ratio / 0.46) + colors[1][0] * (ratio / 0.46))
            g = int(colors[0][1] * (1 - ratio / 0.46) + colors[1][1] * (ratio / 0.46))
            b = int(colors[0][2] * (1 - ratio / 0.46) + colors[1][2] * (ratio / 0.46))
        else:
            r = int(colors[1][0] * (1 - (ratio - 0.46) / 0.54) + colors[2][0] * ((ratio - 0.46) / 0.54))
            g = int(colors[1][1] * (1 - (ratio - 0.46) / 0.54) + colors[2][1] * ((ratio - 0.46) / 0.54))
            b = int(colors[1][2] * (1 - (ratio - 0.46) / 0.54) + colors[2][2] * ((ratio - 0.46) / 0.54))

        draw.line([(i, 0), (i, extended_size[1])], fill=(r, g, b))

    # Rotate the gradient image
    base = base.rotate(angle, expand=True)

    # Crop the rotated image to the desired size
    center_x, center_y = base.size[0] // 2, base.size[1] // 2
    left = center_x - width // 2
    top = center_y - height // 2
    right = left + width
    bottom = top + height
    base = base.crop((left, top, right, bottom))

    return base

def add_rounded_corners(image, radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.width, image.height), radius, fill=255)
    image.putalpha(mask)
    return image

def place_image_on_gradient(background, image_path, padding=40, corner_radius=20, scale=1.0):
    image = Image.open(image_path).convert('RGBA')

    # Apply the specified scale to the image
    scaled_width = int(image.width * scale)
    scaled_height = int(image.height * scale)
    image = image.resize((scaled_width, scaled_height), Image.LANCZOS)

    # Calculate the maximum size preserving the aspect ratio and accounting for padding
    max_width = background.width - 2 * padding
    max_height = background.height - 2 * padding

    # Scale down if the image exceeds the maximum dimensions
    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height), Image.LANCZOS)

    # Add rounded corners
    image = add_rounded_corners(image, corner_radius)

    image_position = (
        (background.width - image.width) // 2,
        (background.height - image.height) // 2
    )

    background.paste(image, image_position, image)

    # Create the output file path
    base_name = os.path.splitext(image_path)[0]
    ext = os.path.splitext(image_path)[1]
    output_path = f"{base_name}_beautified{ext}"

    background.save(output_path)
    return output_path

# Parameters
background_size = (1920, 1080)  # Full HD resolution
gradient_colors = [(65, 88, 208), (200, 80, 192), (255, 204, 112)]  # Colors for gradient
gradient_angle = 43  # Angle for the gradient
image_path = '/Users/duc/Downloads/test.png'
image_scale = 1.0  # Default scale

# Create gradient background
gradient_background = create_gradient(background_size, gradient_colors, gradient_angle)

# Place image on gradient background with padding and rounded corners
output_path = place_image_on_gradient(gradient_background, image_path, scale=image_scale)

print(f"Image saved to {output_path}")
