#!/bin/env python3

import json

# Load JSON data from file
with open('hyde-themes.json', 'r') as file:
    data = json.load(file)

#Sort the data list based on theme name
# data.sort(key=lambda theme: theme.get("THEME", "N/A"))
# Sort the data list based on the first element of COLORSCHEME
data.sort(key=lambda theme: theme.get("COLORSCHEME", ["#000000"])[0])


# Initialize the Markdown table
markdown_table = "| Theme | Description | Author |\n"
markdown_table += "| --- | --- | --- |\n"

# Iterate through the sorted JSON data and populate the table
for theme in data:
    theme_name = theme.get("THEME", "N/A")
    description = theme.get("DESCRIPTION", "N/A")
    author = theme.get("OWNER", "N/A").split('/')[-1]
    link = theme.get("LINK", "#")
    colorscheme = theme.get("COLORSCHEME", ["#000000", "#FFFFFF"])
    
    # Generate the image link
    image_link = f"https://placehold.co/180x50/{colorscheme[0][1:]}/{colorscheme[1][1:]}?text={theme_name.replace(' ', '+')}&font=Oswald"
    
    # Add the row to the table
    markdown_table += f"| [![{theme_name}]({image_link})]({link}) | {description} | [{author}]({theme.get('OWNER', '#')}) |\n"

# Add the footer note and end marker
markdown_table += "\n<!-- TABLE_END -->"

# Read the contents of README.md
with open('README.md', 'r') as readme_file:
    readme_content = readme_file.read()

# Define the markers where the table content will be inserted
start_marker = "<!-- TABLE_START -->"
end_marker = "<!-- TABLE_END -->"

# Insert the table content between the markers
if start_marker in readme_content and end_marker in readme_content:
    before_table = readme_content.split(start_marker)[0] + start_marker
    after_table = readme_content.split(end_marker)[1]
    updated_readme_content = before_table + "\n" + markdown_table  + after_table
else:
    updated_readme_content = readme_content + "\n" + "# Theme Gallery\n" + "<!-- TABLE_START -->\n" + markdown_table

# Write the updated content back to README.md
with open('README.md', 'w') as readme_file:
    readme_file.write(updated_readme_content)

print("README.md has been updated with the generated Markdown table.")
