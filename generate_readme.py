#!/usr/bin/env python3
"""
This script generates a Markdown table for the README.md file based on the JSON data.
"""

import json

# Load JSON data from file
with open('hyde-themes.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Sort the data list based on theme name
data.sort(key=lambda theme: theme.get("THEME", "N/A"))

# Initialize the Markdown table
MARKDOWN_TABLE = "| Theme | Description | Author |\n"
MARKDOWN_TABLE += "| --- | --- | --- |\n"

# Iterate through the sorted JSON data and populate the table
for theme in data:
    theme_name = theme.get("THEME", "N/A")
    description = theme.get("DESCRIPTION", "N/A")
    author = theme.get("OWNER", "N/A").split('/')[-1]
    link = theme.get("LINK", "#")
    colorscheme = theme.get("COLORSCHEME", ["#000000", "#FFFFFF"])

    # Generate the image link
    image_link = f"https://placehold.co/180x50/{colorscheme[0][1:]}/{
        colorscheme[1][1:]}?text={theme_name.replace(' ', '+')}&font=Oswald"

    # Add the row to the table
    MARKDOWN_TABLE += f"| [![{theme_name}]({image_link})]({link}) | {
        description} | [{author}]({theme.get('OWNER', '#')}) |\n"

# Add the footer note and end marker
MARKDOWN_TABLE += "\n<!-- TABLE_END -->"

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme_content = readme_file.read()

# Define the markers where the table content will be inserted
START_MARK = "<!-- TABLE_START -->"
END_MARK = "<!-- TABLE_END -->"

# Insert the table content between the markers
if START_MARK in readme_content and END_MARK in readme_content:
    before_table = readme_content.split(START_MARK)[0] + START_MARK
    after_table = readme_content.split(END_MARK)[1]
    updated_readme_content = before_table + "\n" + MARKDOWN_TABLE + after_table
else:
    updated_readme_content = readme_content + "\n" + \
        "# Theme Gallery\n" + "<!-- TABLE_START -->\n" + MARKDOWN_TABLE

# Write the updated content back to README.md
with open('README.md', 'w', encoding='utf-8') as readme_file:
    readme_file.write(updated_readme_content)

print("README.md has been updated with the generated Markdown table.")
