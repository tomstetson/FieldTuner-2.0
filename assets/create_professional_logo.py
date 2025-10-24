#!/usr/bin/env python3
"""
Create Professional FieldTuner Logo Assets
Generates all necessary logo variations for the application
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

def create_hexagon_mask(size):
    """Create a hexagonal mask for the logo."""
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    # Calculate hexagon points
    center_x, center_y = size // 2, size // 2
    radius = size // 2 - 2
    
    points = []
    for i in range(6):
        angle = math.radians(i * 60)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, fill=255)
    return mask

def create_soldier_silhouette(size):
    """Create a tactical soldier silhouette."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Soldier silhouette (simplified)
    # Head/helmet
    head_center = (size // 2, size // 3)
    head_radius = size // 8
    draw.ellipse([head_center[0] - head_radius, head_center[1] - head_radius,
                  head_center[0] + head_radius, head_center[1] + head_radius], 
                 fill=(77, 208, 225, 255))  # Light teal
    
    # Body
    body_width = size // 4
    body_height = size // 3
    body_x = head_center[0] - body_width // 2
    body_y = head_center[1] + head_radius
    draw.rectangle([body_x, body_y, body_x + body_width, body_y + body_height],
                   fill=(77, 208, 225, 255))
    
    # Rifle
    rifle_width = size // 20
    rifle_height = size // 3
    rifle_x = body_x + body_width - rifle_width
    rifle_y = body_y + body_height // 4
    draw.rectangle([rifle_x, rifle_y, rifle_x + rifle_width, rifle_y + rifle_height],
                   fill=(77, 208, 225, 255))
    
    return img

def create_sliders(size):
    """Create configuration sliders."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Three horizontal sliders
    slider_width = size * 3 // 4
    slider_height = size // 20
    slider_y_start = size // 2
    
    for i in range(3):
        y = slider_y_start + i * (slider_height * 3)
        
        # Slider track
        track_color = (26, 54, 59, 255)  # Dark teal
        draw.rectangle([size // 8, y, size * 7 // 8, y + slider_height],
                       fill=track_color)
        
        # Slider knob
        knob_size = slider_height * 2
        knob_x = size // 8 + (slider_width * (2 - i) // 3)  # Different positions
        knob_y = y - knob_size // 4
        draw.ellipse([knob_x, knob_y, knob_x + knob_size, knob_y + knob_size],
                     fill=(245, 245, 245, 255))  # Off-white
    
    return img

def create_professional_logo(size=512):
    """Create the main professional logo."""
    # Create base image with dark teal background
    img = Image.new('RGBA', (size, size), (26, 54, 59, 255))  # Dark teal background
    
    # Add subtle texture
    for y in range(size):
        for x in range(size):
            noise = (hash((x, y)) % 10) - 5
            r, g, b, a = img.getpixel((x, y))
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            img.putpixel((x, y), (r, g, b, a))
    
    # Create hexagonal mask
    mask = create_hexagon_mask(size)
    
    # Create shield background
    shield = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    shield_draw = ImageDraw.Draw(shield)
    
    # Draw shield border
    border_width = size // 20
    center_x, center_y = size // 2, size // 2
    radius = size // 2 - border_width
    
    # Create hexagon border
    points = []
    for i in range(6):
        angle = math.radians(i * 60)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    shield_draw.polygon(points, outline=(245, 245, 245, 255), width=border_width)
    
    # Add soldier silhouette
    soldier = create_soldier_silhouette(size)
    shield.paste(soldier, (0, 0), soldier)
    
    # Add sliders
    sliders = create_sliders(size)
    shield.paste(sliders, (0, 0), sliders)
    
    # Apply mask
    img.paste(shield, (0, 0), mask)
    
    return img

def create_app_icon(size=256):
    """Create application icon version."""
    logo = create_professional_logo(size)
    
    # Add "6" in corner for Battlefield 6
    draw = ImageDraw.Draw(logo)
    try:
        font = ImageFont.truetype("arial.ttf", size // 8)
    except:
        font = ImageFont.load_default()
    
    text = "6"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = size - text_width - size // 20
    text_y = size // 20
    
    # Draw text with shadow
    draw.text((text_x + 1, text_y + 1), text, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), text, fill=(77, 208, 225, 255), font=font)
    
    return logo

def create_banner(width=800, height=200):
    """Create banner for GitHub and documentation."""
    img = Image.new('RGBA', (width, height), (26, 54, 59, 255))
    draw = ImageDraw.Draw(img)
    
    # Add logo on the left
    logo_size = height - 40
    logo = create_professional_logo(logo_size)
    img.paste(logo, (20, 20), logo)
    
    # Add text
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Title
    title_text = "FIELDTUNER"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    title_x = logo_size + 40
    title_y = 40
    
    draw.text((title_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 128), font=title_font)
    draw.text((title_x, title_y), title_text, fill=(245, 245, 245, 255), font=title_font)
    
    # Subtitle
    subtitle_text = "Battlefield 6 Configuration Tool"
    subtitle_x = title_x
    subtitle_y = title_y + title_height + 10
    
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle_text, fill=(0, 0, 0, 128), font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=(77, 208, 225, 255), font=subtitle_font)
    
    # Tagline
    tagline_text = "World-Class Gaming Configuration"
    tagline_x = title_x
    tagline_y = subtitle_y + 30
    
    draw.text((tagline_x + 1, tagline_y + 1), tagline_text, fill=(0, 0, 0, 128), font=subtitle_font)
    draw.text((tagline_x, tagline_y), tagline_text, fill=(245, 245, 245, 200), font=subtitle_font)
    
    return img

def create_social_media_assets():
    """Create social media ready assets."""
    assets = {}
    
    # GitHub social preview (1200x630)
    github_preview = Image.new('RGBA', (1200, 630), (26, 54, 59, 255))
    draw = ImageDraw.Draw(github_preview)
    
    # Large logo
    logo = create_professional_logo(400)
    github_preview.paste(logo, (400, 115), logo)
    
    # Title
    try:
        font = ImageFont.truetype("arial.ttf", 72)
    except:
        font = ImageFont.load_default()
    
    title_text = "FIELDTUNER"
    title_bbox = draw.textbbox((0, 0), title_text, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    
    title_x = (1200 - title_width) // 2
    title_y = 50
    
    draw.text((title_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 128), font=font)
    draw.text((title_x, title_y), title_text, fill=(245, 245, 245, 255), font=font)
    
    # Subtitle
    try:
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
    except:
        subtitle_font = ImageFont.load_default()
    
    subtitle_text = "Battlefield 6 Configuration Tool"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    subtitle_x = (1200 - subtitle_width) // 2
    subtitle_y = 550
    
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle_text, fill=(0, 0, 0, 128), font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=(77, 208, 225, 255), font=subtitle_font)
    
    assets['github_social'] = github_preview
    
    return assets

def main():
    """Create all professional logo assets."""
    print("Creating Professional FieldTuner Logo Assets")
    print("=" * 50)
    
    # Create assets directory
    os.makedirs("assets", exist_ok=True)
    
    # Create main logo
    print("Creating main logo...")
    logo = create_professional_logo(512)
    logo.save("assets/logo_professional.png", "PNG")
    print("   [OK] logo_professional.png created")
    
    # Create app icon
    print("Creating application icon...")
    icon = create_app_icon(256)
    icon.save("assets/icon_professional.png", "PNG")
    icon.save("assets/icon_professional.ico", "ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("   [OK] icon_professional.png and .ico created")
    
    # Create banner
    print("Creating banner...")
    banner = create_banner(800, 200)
    banner.save("assets/banner_professional.png", "PNG")
    print("   [OK] banner_professional.png created")
    
    # Create social media assets
    print("Creating social media assets...")
    social_assets = create_social_media_assets()
    for name, asset in social_assets.items():
        asset.save(f"assets/{name}.png", "PNG")
        print(f"   [OK] {name}.png created")
    
    # Create different icon sizes
    sizes = [16, 32, 48, 64, 128, 256, 512]
    for size in sizes:
        resized_icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized_icon.save(f"assets/icon_professional_{size}x{size}.png", "PNG")
    
    print("   [OK] Multiple icon sizes created")
    
    print("\n[SUCCESS] Professional logo assets created successfully!")
    print("Assets created:")
    print("   [LOGO] Professional logo (logo_professional.png)")
    print("   [ICON] Application icon (icon_professional.ico, .png)")
    print("   [BANNER] GitHub banner (banner_professional.png)")
    print("   [SOCIAL] Social media assets")
    print("   [SIZES] Multiple icon sizes")
    
    return True

if __name__ == "__main__":
    main()
