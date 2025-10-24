#!/usr/bin/env python3
"""
Create the new FieldTuner logo based on the provided design.
Features a shield/hexagon emblem with gear and sliders on a dark textured background.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_fieldtuner_logo(size=(512, 512), output_path="logo.png"):
    """Create the new FieldTuner logo."""
    
    # Create image with dark textured background
    img = Image.new('RGBA', size, (0x1a, 0x1a, 0x1a, 255))  # Dark charcoal background
    draw = ImageDraw.Draw(img)
    
    # Add subtle texture to background
    for i in range(0, size[0], 2):
        for j in range(0, size[1], 2):
            if (i + j) % 4 == 0:
                draw.point((i, j), fill=(0x20, 0x20, 0x20, 255))
    
    # Calculate positions
    center_x, center_y = size[0] // 2, size[1] // 2
    shield_size = int(size[0] * 0.4)  # Shield takes 40% of image
    
    # Create shield/hexagon emblem
    shield_points = [
        (center_x, center_y - shield_size//2),  # Top
        (center_x + shield_size//3, center_y - shield_size//4),  # Top right
        (center_x + shield_size//3, center_y + shield_size//4),  # Bottom right
        (center_x, center_y + shield_size//2),  # Bottom
        (center_x - shield_size//3, center_y + shield_size//4),  # Bottom left
        (center_x - shield_size//3, center_y - shield_size//4),  # Top left
    ]
    
    # Draw shield outline (thick beige/cream border)
    shield_color = (0xf5, 0xf5, 0xdc, 255)  # Beige/cream
    draw.polygon(shield_points, outline=shield_color, width=8)
    
    # Create gear icon at top of shield
    gear_center_x, gear_center_y = center_x, center_y - shield_size//3
    gear_radius = shield_size // 8
    
    # Draw gear (simplified)
    draw.ellipse([gear_center_x - gear_radius, gear_center_y - gear_radius,
                  gear_center_x + gear_radius, gear_center_y + gear_radius],
                 outline=shield_color, width=4)
    
    # Add gear teeth
    for angle in range(0, 360, 30):
        import math
        rad = math.radians(angle)
        x1 = gear_center_x + (gear_radius + 4) * math.cos(rad)
        y1 = gear_center_y + (gear_radius + 4) * math.sin(rad)
        x2 = gear_center_x + (gear_radius + 8) * math.cos(rad)
        y2 = gear_center_y + (gear_radius + 8) * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=shield_color, width=2)
    
    # Create three horizontal sliders/equalizer bars
    slider_y_start = center_y + shield_size//6
    slider_spacing = shield_size // 12
    slider_width = shield_size // 3
    slider_height = 6
    teal_color = (0x20, 0xb2, 0xaa, 255)  # Teal color for sliders
    
    # Top slider (knob left)
    slider_y = slider_y_start
    draw.rectangle([center_x - slider_width//2, slider_y - slider_height//2,
                   center_x + slider_width//2, slider_y + slider_height//2],
                  fill=teal_color)
    knob_x = center_x - slider_width//3
    draw.ellipse([knob_x - 4, slider_y - 4, knob_x + 4, slider_y + 4],
                fill=shield_color)
    
    # Middle slider (knob right)
    slider_y = slider_y_start + slider_spacing
    draw.rectangle([center_x - slider_width//2, slider_y - slider_height//2,
                   center_x + slider_width//2, slider_y + slider_height//2],
                  fill=teal_color)
    knob_x = center_x + slider_width//3
    draw.ellipse([knob_x - 4, slider_y - 4, knob_x + 4, slider_y + 4],
                fill=shield_color)
    
    # Bottom slider (knob left)
    slider_y = slider_y_start + slider_spacing * 2
    draw.rectangle([center_x - slider_width//2, slider_y - slider_height//2,
                   center_x + slider_width//2, slider_y + slider_height//2],
                  fill=teal_color)
    knob_x = center_x - slider_width//3
    draw.ellipse([knob_x - 4, slider_y - 4, knob_x + 4, slider_y + 4],
                fill=shield_color)
    
    # Add text "FIELD TUNER"
    try:
        # Try to use a bold font
        font_size = size[0] // 12
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    text = "FIELD TUNER"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = center_x - text_width // 2
    text_y = center_y + shield_size//2 + 20
    
    draw.text((text_x, text_y), text, fill=shield_color, font=font)
    
    # Save the image
    img.save(output_path, "PNG")
    print(f"Logo created: {output_path}")
    return img

def create_icon_variants():
    """Create various icon sizes for different uses."""
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        output_path = f"icon_{size}x{size}.png"
        create_fieldtuner_logo((size, size), output_path)
        print(f"Created {size}x{size} icon")

def create_banner():
    """Create a banner version of the logo."""
    banner_size = (1200, 400)
    img = Image.new('RGBA', banner_size, (0x1a, 0x1a, 0x1a, 255))
    draw = ImageDraw.Draw(img)
    
    # Add texture
    for i in range(0, banner_size[0], 3):
        for j in range(0, banner_size[1], 3):
            if (i + j) % 6 == 0:
                draw.point((i, j), fill=(0x20, 0x20, 0x20, 255))
    
    # Create larger shield for banner
    center_x, center_y = banner_size[0] // 2, banner_size[1] // 2
    shield_size = int(banner_size[1] * 0.6)
    
    # Shield points
    shield_points = [
        (center_x, center_y - shield_size//2),
        (center_x + shield_size//3, center_y - shield_size//4),
        (center_x + shield_size//3, center_y + shield_size//4),
        (center_x, center_y + shield_size//2),
        (center_x - shield_size//3, center_y + shield_size//4),
        (center_x - shield_size//3, center_y - shield_size//4),
    ]
    
    shield_color = (0xf5, 0xf5, 0xdc, 255)
    draw.polygon(shield_points, outline=shield_color, width=12)
    
    # Gear
    gear_center_x, gear_center_y = center_x, center_y - shield_size//3
    gear_radius = shield_size // 8
    draw.ellipse([gear_center_x - gear_radius, gear_center_y - gear_radius,
                  gear_center_x + gear_radius, gear_center_y + gear_radius],
                 outline=shield_color, width=6)
    
    # Sliders
    slider_y_start = center_y + shield_size//6
    slider_spacing = shield_size // 12
    slider_width = shield_size // 3
    slider_height = 8
    teal_color = (0x20, 0xb2, 0xaa, 255)
    
    for i, knob_offset in enumerate([-1, 1, -1]):  # Left, right, left
        slider_y = slider_y_start + slider_spacing * i
        draw.rectangle([center_x - slider_width//2, slider_y - slider_height//2,
                       center_x + slider_width//2, slider_y + slider_height//2],
                      fill=teal_color)
        knob_x = center_x + knob_offset * slider_width//3
        draw.ellipse([knob_x - 6, slider_y - 6, knob_x + 6, slider_y + 6],
                    fill=shield_color)
    
    # Text
    try:
        font_size = banner_size[0] // 20
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "FIELD TUNER"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = center_x - text_width // 2
    text_y = center_y + shield_size//2 + 30
    
    draw.text((text_x, text_y), text, fill=shield_color, font=font)
    
    img.save("banner.png", "PNG")
    print("Banner created: banner.png")

def create_ico():
    """Create Windows .ico file from the logo."""
    # Create 256x256 version first
    logo_256 = create_fieldtuner_logo((256, 256), "temp_logo_256.png")
    
    # Convert to ICO format
    logo_256.save("icon.ico", format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
    print("ICO file created: icon.ico")
    
    # Clean up temp file
    if os.path.exists("temp_logo_256.png"):
        os.remove("temp_logo_256.png")

if __name__ == "__main__":
    print("Creating FieldTuner logo assets...")
    
    # Create main logo
    create_fieldtuner_logo()
    
    # Create icon variants
    create_icon_variants()
    
    # Create banner
    create_banner()
    
    # Create ICO file
    create_ico()
    
    print("All logo assets created successfully!")
