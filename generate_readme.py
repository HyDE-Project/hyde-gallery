#!/bin/env python3
""" "This is a script to generate a Markdown table and theme previews for the README.md file"""

import os
import json
from pathlib import Path

# Load JSON data from file
with open("hyde-themes.json", "r", encoding="utf-8") as file:
    content = file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: parse multiple JSON objects in the file
        data = []
        decoder = json.JSONDecoder()
        idx = 0
        content = content.lstrip()
        while idx < len(content):
            try:
                obj, idx_new = decoder.raw_decode(content[idx:])
                data.append(obj)
                idx += idx_new
                # Skip whitespace between objects
                while idx < len(content) and content[idx] in ["\n", "\r", " ", "\t"]:
                    idx += 1
            except json.JSONDecodeError:
                break

# Sort the data list based on theme name
# data.sort(key=lambda theme: theme.get("THEME", "N/A"))
# Sort the data list based on the first element of COLORSCHEME


def hex_to_intensity(hex_color):
    """Convert hex color to intensity"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b


data.sort(
    key=lambda theme: hex_to_intensity(
        theme.get("COLORSCHEME", ["#000000"])[0]
        if isinstance(theme.get("COLORSCHEME"), list)
        and len(theme.get("COLORSCHEME")) > 0
        else "#000000"
    )
)

# Initialize the Markdown table
MD_TABLE = "| Theme | Description | Author |\n"
MD_TABLE += "| --- | --- | --- |\n"

# Iterate through the sorted JSON data and populate the table
for theme in data:
    theme_name = theme.get("THEME", "N/A")
    description = theme.get("DESCRIPTION", "N/A")
    author = theme.get("OWNER", "N/A").split("/")[-1]
    link = theme.get("LINK", "#")
    colorscheme = theme.get("COLORSCHEME", ["#000000", "#FFFFFF"])

    # Generate the image link
    BASE_URL = "https://placehold.co/180x50"
    color1 = colorscheme[0][1:]
    color2 = colorscheme[1][1:]
    text = theme_name.replace(" ", "+")
    IMAGE_LINK = f"{BASE_URL}/{color1}/{color2}?text={text}&font=Oswald"
    # Create anchor link for the theme name (replacing spaces with hyphens)
    anchor_name = theme_name.replace(" ", "-")

    # Add the row to the table with anchor link to the gallery section
    MD_TABLE += (
        f"| [![{theme_name}]({IMAGE_LINK})](#{anchor_name.lower()}) | "
        f"{description} | "
        f"[{author}]({theme.get('OWNER', '#')}) |\n"
    )

# Just close the table, we'll add the end marker when inserting into README
MD_TABLE += "\n"

# Generate theme preview cards
PREVIEW_START = "<!-- GALLERY_START -->"
PREVIEW_END = "<!-- GALLERY_END -->"


# Function to find preview images in theme directories
def find_preview_image(theme_name):
    # Try different directory naming conventions
    possible_dirs = [
        theme_name,  # Exact match
        theme_name.replace(" ", "-"),  # Replace spaces with hyphens
        theme_name.replace(" ", "_"),  # Replace spaces with underscores
        theme_name.replace("-", " "),  # Replace hyphens with spaces
        theme_name.replace("_", " "),  # Replace underscores with spaces
    ]

    for dir_name in possible_dirs:
        theme_path = Path(dir_name)

        if not theme_path.exists() or not theme_path.is_dir():
            continue

        # Look for image files with common patterns
        image_patterns = [
            "preview.*",
            "Preview.*",
            "*screenshot*",
            "*.png",
            "*.jpg",
            "*.gif",
            "*.jpeg",
        ]

        for pattern in image_patterns:
            images = list(theme_path.glob(pattern))
            if images:
                # Return the first image found
                return str(images[0])

    # If no match found, let's try a more flexible approach by searching all directories
    all_dirs = [
        d for d in Path(".").iterdir() if d.is_dir() and not d.name.startswith(".")
    ]
    theme_name_lower = theme_name.lower()

    for directory in all_dirs:
        # Check if directory name contains the theme name (case-insensitive)
        if (
            theme_name_lower in directory.name.lower()
            or directory.name.lower() in theme_name_lower
        ):
            # Found a potential match, look for images
            for pattern in ["preview.*", "*.png", "*.jpg", "*.jpeg"]:
                images = list(directory.glob(pattern))
                if images:
                    return str(images[0])

    return None


# Generate preview cards for themes
THEME_CARDS = ""

# Get count of themes with preview images
themes_with_previews = []
for theme in data:
    if "THEME" in theme:
        theme_name = theme.get("THEME", "N/A")
        preview_image = find_preview_image(theme_name)
        if preview_image:
            themes_with_previews.append(theme_name)

# Add a title for the preview section
THEME_CARDS += (
    f"\n# Explore {len(themes_with_previews)} worlds of color and imagination 🪄.\n\n"
)

# Sort the gallery data alphabetically by theme name
alphabetical_data = sorted(
    [theme for theme in data if "THEME" in theme],
    key=lambda theme: theme.get("THEME", "").lower(),
)

# Create a list to store themes with preview images
valid_themes = []

# Collect all themes with preview images
for theme in alphabetical_data:
    theme_name = theme.get("THEME", "N/A")
    preview_image = find_preview_image(theme_name)

    if preview_image:
        valid_themes.append(theme)

# Add theme cards with numbering
for index, theme in enumerate(valid_themes, 1):
    theme_name = theme.get("THEME", "N/A")
    description = theme.get("DESCRIPTION", "N/A")
    author = theme.get("OWNER", "N/A").split("/")[-1] if "OWNER" in theme else "Unknown"
    link = theme.get("LINK", "#")

    # Find preview image
    preview_image = find_preview_image(theme_name)

    # Create anchor tag for the theme (replacing spaces with hyphens)
    anchor_name = theme_name.replace(" ", "-").lower()

    # Create a card for the theme with numbering and anchor
    THEME_CARDS += f'<a id="{anchor_name}"></a>\n'
    THEME_CARDS += f"### {index}. {theme_name}\n\n"
    THEME_CARDS += f"**By:** [{author}]({theme.get('OWNER', '#')})\n\n"
    THEME_CARDS += f"**Description:** {description}\n\n"

    # URL-encode spaces and special characters in the image path for markdown compatibility
    # First, split the path to encode directory and file parts separately
    import urllib.parse

    path_parts = preview_image.split("/")
    encoded_parts = [urllib.parse.quote(part) for part in path_parts]
    encoded_path = "/".join(encoded_parts)

    # Add preview with back-to-top button using theme colors
    colorscheme = theme.get("COLORSCHEME", ["#000000", "#FFFFFF"])
    bg_color = colorscheme[0].lstrip("#")
    fg_color = colorscheme[1].lstrip("#")
    THEME_CARDS += f"[![{theme_name} Preview]({encoded_path})]({link}) "
    THEME_CARDS += f'<a href="#theme-gallery" title="Back to top"><img src="https://img.shields.io/badge/↑-Back_to_Top-{fg_color}?style=flat&labelColor={bg_color}&color={bg_color}" alt="Back to Top" style="vertical-align: middle;"></a>\n\n'
    THEME_CARDS += "---\n\n"

# Add the end marker
THEME_CARDS += PREVIEW_END

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as readme_file:
    readme_content = readme_file.read()

# Define the markers for all sections
START_MARK = "<!-- TABLE_START -->"
END_MARK = "<!-- TABLE_END -->"

# Handle table content insertion
if START_MARK in readme_content and END_MARK in readme_content:
    # Split the content into parts and make sure we don't duplicate the end marker
    parts = readme_content.split(START_MARK)
    before_table = parts[0] + START_MARK

    # Get everything after the first END_MARK
    remaining = readme_content.split(END_MARK, 1)[1]

    # Update readme with new table content
    readme_with_table = before_table + "\n" + MD_TABLE + END_MARK + remaining
else:
    # Add new table if it doesn't exist
    readme_with_table = (
        readme_content + "\n# Theme Gallery\n" + START_MARK + "\n" + MD_TABLE + END_MARK
    )

# Handle gallery insertion (should be at the bottom)
if PREVIEW_START in readme_with_table and PREVIEW_END in readme_with_table:
    # Split the content into parts to avoid marker duplication
    parts = readme_with_table.split(PREVIEW_START)
    before_gallery = parts[0] + PREVIEW_START

    # Get everything after the first PREVIEW_END
    after_gallery = readme_with_table.split(PREVIEW_END, 1)[1]

    # Update readme with new gallery content
    updated_readme_content = before_gallery + "\n" + THEME_CARDS + after_gallery
else:
    # Add new gallery section at the end
    updated_readme_content = (
        readme_with_table + "\n\n" + PREVIEW_START + "\n" + THEME_CARDS + "\n"
    )

if not os.path.exists("README.md"):
    os.chmod("README.md", 0o666)

# Check if the script has write permissions for README.md
if os.access("README.md", os.W_OK):
    # Write the updated content back to README.md
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(updated_readme_content)
    print("README.md has been updated with the generated Markdown table.")
else:
    print("Permission denied: 'README.md'. Please check the file permissions.")
