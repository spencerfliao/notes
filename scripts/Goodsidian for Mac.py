#!/usr/bin/env python3

import urllib.request
import os
import xml.etree.ElementTree as ET

# Define shelves and their respective vault paths
shelves = {
    "biographies": "/Users/SFL/notes/content/Other Genres/Biographies",
    "business": "/Users/SFL/notes/content/Other Genres/Business",
    "fiction": "/Users/SFL/notes/content/Other Genres/Fiction",
    "humanities": "/Users/SFL/notes/content/Other Genres/Humanities",
    "personal": "/Users/SFL/notes/content/Self-help",
    "sciences": "/Users/SFL/notes/content/Natural & Social Sciences"
}

# Goodreads RSS URL template
rss_url_template = "https://www.goodreads.com/review/list_rss/56197581?key=cFzeoclEvdAOefh4RT7IodHnm3fI7hhI88CLXTDWxZz6AwrW&shelf={}"

# Function to fetch and parse RSS data
def fetch_books(shelf, folder):
    url = rss_url_template.format(shelf)
    response = urllib.request.urlopen(url)
    feed = response.read().decode("utf-8")
    info = ET.fromstring(feed)
    
    for item in info.findall(".//item"):
        title_element = item.find("title")
        full_title = title_element.text.strip() if title_element is not None else "Unknown Title"
        short_title = full_title.split(":")[0].strip().split("(")[0].strip()
        subtitle = ""
        if ":" in full_title:
            subtitle += full_title.split(":")[1].strip()
        elif "(" in full_title and ")" in full_title:
            subtitle += f" ({full_title.split('(')[1].split(')')[0].strip()})"
        author = item.find("author_name").text if item.find("author_name") is not None else "Unknown Author"
        year = item.find("book_published").text if item.find("book_published") is not None else "Unknown Year"
        cover = item.find("book_large_image_url").text if item.find("book_large_image_url") is not None else ""
        status = item.find("user_read_at").text
        
        if status:
            status = "Read"
        elif item.find("user_started_at"):
            status = "Currently Reading"
        else:
            status = "Want to Read"
        
        filename = os.path.join(folder, f"{short_title.replace('/', '-')}.md")
        
        content = f"""---
Title: "{short_title}"
Full Title: "{full_title}"
Subtitle: "{subtitle}"
Cover: "{cover}"
Author: "{author}"
Year: "{year}"
Shelf: "{shelf}"
Status: "{status}"
---
"""
        if subtitle.strip():  # Check if subtitle is not empty
            content += f"""
## — {subtitle}
"""
            
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

# Iterate through each shelf and process books
for shelf, folder in shelves.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    fetch_books(shelf, folder)

print('All book were synced to Obsidian!')