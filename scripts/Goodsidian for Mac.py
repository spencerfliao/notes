# import urllib.request
# import os
# import subprocess
# import xml.etree.ElementTree as ET

# # URL for RSS of shelf:
# url = "https://www.goodreads.com/review/list_rss/56197581?key=nWY09T6mRBlqowTLnFbs3DP0WqroPuPiNsO_cjgCw9sa1wQ2&shelf=tech"

# # Enter the path to that shelf in your Vault
# vaultpath = '/Users/SFL/notes/content/Natural & Social Sciences'

# # Fetch the data from rss feed and decode
# response = urllib.request.urlopen(url)
# feed = response.read().decode("utf-8")
# info = ET.fromstring(feed)

# # Define the elements to be extracted

# bookamount = 0
# id = ""
# title = ""
# shorttitle = ""
# image = ""
# author = ""
# year = ""
# shelf = ""

# # Extract and display content for each element
# for root in info.findall(".//item"):  # This will find all <item> elements at any level

#     id_element = root.find(".//book_id")
#     if id_element is not None:
#         id = id_element.text.strip()

#     title_element = root.find(".//title")
#     if title_element is not None:
#         title = title_element.text.strip()
#         shorttitle = title

#         # Find title up to the first colon as note name
#         colon_index = title.find(":")
#         if colon_index != -1:
#             shorttitle = title[:colon_index].strip()

#     if os.path.exists(f"{vaultpath}/{shorttitle}.md"):
#         continue
#     bookamount = bookamount + 1

#     image_element = root.find(".//book_large_image_url")
#     if image_element is not None:
#         image = image_element.text.strip()

#     author_element = root.find(".//author_name")
#     if author_element is not None:
#         author = author_element.text.strip()

#     year_element = root.find(".//book_published")
#     if year_element is not None:
#         if year_element.text is not None:
#             year = year_element.text.strip()

#     shelf_element = root.find(".//user_shelves")
#     if shelf_element is not None:
#         shelf = shelf_element.text.strip()
#     list = [tag.strip() for tag in shelf.split(',')]
#     front = []
#     back = []
#     for tag in list:
#         if tag in ["to-read", "read", "currently-reading"]:
#             back.append(f"#{tag}")
#         else:
#             front.append(f"#{tag}")
#         combined = front + back
#         shelf = ' '.join(combined)

#     note_content = f'''![]({image})

# **Title:** {title}
# **Author:** {author}
# **Year:** {year}
# **Shelf:** {shelf}
# '''

#     note_path = os.path.join(vaultpath, f'{shorttitle}.md')
#     with open(note_path, 'w') as note_file:
#         note_file.write(note_content)

# if bookamount == 0:
#     subprocess.run(["osascript", "-e", 'display notification "No new books found." with title "Currently-reading: No update"'])

# else:
#     subprocess.run(["osascript", "-e", f'display notification "{bookamount} Booknote(s) created!" with title "{title}"'])

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
        title = item.find("title").text if item.find("title") is not None else "Unknown Title"
        author = item.find("author_name").text if item.find("author_name") is not None else "Unknown Author"
        year = item.find("publication_year").text if item.find("publication_year") is not None else "Unknown Year"
        cover = item.find("book_large_image_url").text if item.find("book_large_image_url") is not None else ""
        status = item.find("user_read_at").text
        
        if status:
            status = "Read"
        elif item.find("user_started_at"):
            status = "Currently Reading"
        else:
            status = "Want to Read"
        
        filename = os.path.join(folder, f"{title.replace('/', '-')}.md")
        
        content = f"""---
Title: "{title}"
Cover: "{cover}"
Author: "{author}"
Year: "{year}"
Shelf: "{shelf}"
Status: "{status}"
---
"""
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {filename}")

# Iterate through each shelf and process books
for shelf, folder in shelves.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    fetch_books(shelf, folder)