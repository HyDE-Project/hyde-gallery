#!/bin/env python3
""""This is a script to generate a Markdown table for the README.md file"""
import json

# Load JSON data from file
with open("hyde-themes.json", "r", encoding="utf-8") as file:
    data = json.load(file)

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
    # Add the row to the table
    MD_TABLE += (
        f"| [![{theme_name}]({IMAGE_LINK})]({link}) | "
        f"{description} | "
        f"[{author}]({theme.get('OWNER', '#')}) |\n"
    )

# Add the footer note and end marker
MD_TABLE += "\n<!-- TABLE_END -->"

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as readme_file:
    readme_content = readme_file.read()

# Define the markers where the table content will be inserted
START_MARK = "<!-- TABLE_START -->"
END_MARK = "<!-- TABLE_END -->"

# Insert the table content between the markers
if START_MARK in readme_content and END_MARK in readme_content:
    before_table = readme_content.split(START_MARK)[0] + START_MARK
    after_table = readme_content.split(END_MARK)[1]
    updated_readme_content = before_table + "\n" + MD_TABLE + after_table
else:
    updated_readme_content = (
        readme_content
        + "\n"
        + "# Theme Gallery\n"
        + "<!-- TABLE_START -->\n"
        + MD_TABLE
    )

import os

# Check if the script has write permissions for README.md
if os.access("README.md", os.W_OK):
    # Write the updated content back to README.md
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(updated_readme_content)
    print("README.md has been updated with the generated Markdown table.")
else:
    print("Permission denied: 'README.md'. Please check the file permissions.")

print("README.md has been updated with the generated Markdown table.")
