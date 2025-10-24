#!/usr/bin/env python3
"""
Create FieldTuner application icon and branding assets
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a professional application icon."""
    # Create a 256x256 icon
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle with gradient effect
    margin = 20
    bg_rect = [margin, margin, size - margin, size - margin]
    
    # Draw background circle with gradient
    for i in range(0, 50):
        alpha = int(255 * (1 - i / 50))
        color = (74, 144, 226, alpha)  # Blue gradient
        draw.ellipse([bg_rect[0] + i, bg_rect[1] + i, bg_rect[2] - i, bg_rect[3] - i], fill=color)
    
    # Draw inner circle
    inner_margin = 40
    inner_rect = [margin + inner_margin, margin + inner_margin, 
                  size - margin - inner_margin, size - margin - inner_margin]
    draw.ellipse(inner_rect, fill=(42, 42, 42, 255))  # Dark background
    
    # Draw "FT" text
    try:
        # Try to use a system font
        font_size = 80
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw "FT" text
    text = "FT"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 10
    
    # Draw text with shadow
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Draw small "6" in corner
    small_font_size = 30
    try:
        small_font = ImageFont.truetype("arial.ttf", small_font_size)
    except:
        small_font = ImageFont.load_default()
    
    small_text = "6"
    small_bbox = draw.textbbox((0, 0), small_text, font=small_font)
    small_text_width = small_bbox[2] - small_bbox[0]
    small_text_height = small_bbox[3] - small_bbox[1]
    
    small_x = size - margin - small_text_width - 10
    small_y = margin + 10
    
    draw.text((small_x + 1, small_y + 1), small_text, fill=(0, 0, 0, 128), font=small_font)
    draw.text((small_x, small_y), small_text, fill=(74, 144, 226, 255), font=small_font)
    
    return img

def create_logo():
    """Create a horizontal logo for documentation."""
    width, height = 400, 100
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background
    draw.rounded_rectangle([0, 0, width, height], radius=10, fill=(42, 42, 42, 255))
    
    # Icon on the left
    icon_size = 60
    icon_img = create_icon()
    icon_img = icon_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon_img, (20, 20), icon_img)
    
    # Text
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        subtitle_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Title
    title_text = "FieldTuner"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    title_x = 100
    title_y = 20
    
    draw.text((title_x + 1, title_y + 1), title_text, fill=(0, 0, 0, 128), font=title_font)
    draw.text((title_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font)
    
    # Subtitle
    subtitle_text = "Battlefield 6 Configuration Tool"
    subtitle_x = 100
    subtitle_y = title_y + title_height + 5
    
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle_text, fill=(0, 0, 0, 128), font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=(136, 136, 136, 255), font=subtitle_font)
    
    return img

def create_banner():
    """Create a banner for GitHub and documentation."""
    width, height = 800, 200
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    for y in range(height):
        alpha = int(255 * (1 - y / height * 0.3))
        color = (74, 144, 226, alpha)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add some geometric elements
    for i in range(5):
        x = 50 + i * 150
        y = 50 + i * 20
        size = 30 - i * 5
        draw.ellipse([x, y, x + size, y + size], fill=(255, 255, 255, 50))
    
    # Logo
    logo_img = create_logo()
    logo_img = logo_img.resize((300, 75), Image.Resampling.LANCZOS)
    img.paste(logo_img, (50, 60), logo_img)
    
    # Tagline
    try:
        tagline_font = ImageFont.truetype("arial.ttf", 24)
    except:
        tagline_font = ImageFont.load_default()
    
    tagline_text = "World-Class Battlefield 6 Configuration Tool"
    tagline_bbox = draw.textbbox((0, 0), tagline_text, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    
    tagline_x = (width - tagline_width) // 2
    tagline_y = 150
    
    draw.text((tagline_x + 1, tagline_y + 1), tagline_text, fill=(0, 0, 0, 128), font=tagline_font)
    draw.text((tagline_x, tagline_y), tagline_text, fill=(255, 255, 255, 255), font=tagline_font)
    
    return img

def main():
    """Create all branding assets."""
    print("Creating FieldTuner branding assets...")
    
    # Create assets directory
    os.makedirs("assets", exist_ok=True)
    
    # Create icon
    print("Creating application icon...")
    icon = create_icon()
    icon.save("assets/icon.png", "PNG")
    icon.save("assets/icon.ico", "ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("   [OK] icon.png and icon.ico created")
    
    # Create logo
    print("Creating logo...")
    logo = create_logo()
    logo.save("assets/logo.png", "PNG")
    print("   [OK] logo.png created")
    
    # Create banner
    print("Creating banner...")
    banner = create_banner()
    banner.save("assets/banner.png", "PNG")
    print("   [OK] banner.png created")
    
    # Create different icon sizes
    sizes = [16, 32, 48, 64, 128, 256]
    for size in sizes:
        resized_icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized_icon.save(f"assets/icon_{size}x{size}.png", "PNG")
    
    print("   [OK] Multiple icon sizes created")
    
    print("\n[SUCCESS] All branding assets created successfully!")
    print("Assets created:")
    print("   [ICON] Application icon (icon.ico, icon.png)")
    print("   [LOGO] Logo (logo.png)")
    print("   [BANNER] Banner (banner.png)")
    print("   [SIZES] Multiple icon sizes")
    
    return True

if __name__ == "__main__":
    main()
