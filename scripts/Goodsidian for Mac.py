import urllib.request
import os
import re
import xml.etree.ElementTree as ET

# Define shelves and their respective vault paths

shelves = {
    "biographies": '/Users/SFL/notes/content/Books 阅读笔记/Other Genres 其他/Biographies 传记',
    "personal": '/Users/SFL/notes/content/Books 阅读笔记/Self-help 自我提升/Personal Development 成长',
    "business": '/Users/SFL/notes/content/Books 阅读笔记/Self-help 自我提升/Business Thinking 商业',
    "fiction": '/Users/SFL/notes/content/Books 阅读笔记/Other Genres 其他/Fiction 小说',
    "humanities": '/Users/SFL/notes/content/Books 阅读笔记/Other Genres 其他/Humanities 人文',
    "sciences": '/Users/SFL/notes/content/Books 阅读笔记/Natural & Social Sciences 科学'
}

WHITELIST_BOOKS = {
    "The Art of Loving",
    "Real Happy Pill"
}

# Goodreads RSS URL template
rss_url_template = "https://www.goodreads.com/review/list_rss/56197581?key=cFzeoclEvdAOefh4RT7IodHnm3fI7hhI88CLXTDWxZz6AwrW&shelf={}"

def extract_existing_content(filename, subtitle):
    """Extracts manually written content and detects existing subtitles."""
    if not os.path.exists(filename):
        return "", None  # If file doesn't exist, return empty content and no subtitle

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Split YAML frontmatter from the body
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            content = parts[2].strip()  # Extract the body content only

    # Detect subtitle line
    subtitle_pattern = re.compile(r"^## — .+", re.MULTILINE)
    matches = subtitle_pattern.findall(content)

    if matches:
        # Extract the first subtitle and preserve content after it
        subtitle_pos = content.find(matches[0])
        existing_subtitle = matches[0].replace("## — ", "").strip()  # Remove markdown syntax
        preserved_content = content[subtitle_pos + len(matches[0]):].strip()
        return preserved_content, existing_subtitle
    else:
        # If no subtitle exists, preserve the entire content
        return content.strip(), None

def fetch_books(shelf, folder):
    """Fetches and updates book notes while preserving manually written content."""
    url = rss_url_template.format(urllib.parse.quote(shelf))
    response = urllib.request.urlopen(url)
    feed = response.read().decode("utf-8")
    info = ET.fromstring(feed)

    processed_books = set()
    
    for item in info.findall(".//item"):
        title_element = item.find("title")
        full_title = title_element.text.strip() if title_element is not None else "Unknown Title"
        short_title = full_title.split(":")[0].strip().split("(")[0].strip()

        # only imported whitelisted
        if short_title not in WHITELIST_BOOKS:
            continue

        processed_books.add(short_title)
        print(f"Processing: {short_title} (from shelf: {shelf})")

        subtitle = ""
        if ":" in full_title:
            subtitle += full_title.split(":")[1].strip()
        elif "(" in full_title and ")" in full_title:
            subtitle += full_title.split("(")[1].split(")")[0].strip()

        # Clean up subtitle and short title
        subtitle = re.sub(r"[#()]", "", subtitle).strip()
        short_title = re.sub(r"[#()]", "", short_title).strip()

        # Other metadata
        author = item.find("author_name").text if item.find("author_name") is not None else "Unknown Author"
        year = item.find("book_published").text if item.find("book_published") is not None else "Unknown Year"
        cover = item.find("book_large_image_url").text if item.find("book_large_image_url") is not None else ""
        
        filename = os.path.join(folder, f"{short_title.replace('/', '-')}.md")
        
        # Extract existing content and subtitle
        preserved_content, existing_subtitle = extract_existing_content(filename, subtitle)

        # Status (preserve manually 'read' because Goodreads has lag)
        status = item.find("user_read_at").text
        if status:
            status = "Read"
        elif item.find("user_started_at"):
            status = "Currently Reading"
        else:
            status = "Want to Read"
        
        existing_status = None
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                existing_content = f.read()
            status_match = re.search(r'Status:\s*"?(.*?)"?$', existing_content, re.MULTILINE)
            if status_match:
                existing_status = status_match.group(1).strip()

        if existing_status == "Read" and status == "Want to Read":
            # print(filename)
            status = "Read"
        
        # Subfields (preserving manually added content)
        existing_sub = ""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                existing_content = f.read()
            status_match = re.search(r'Subfield:\s*"?(.*?)"?$', existing_content, re.MULTILINE)
            if status_match:
                existing_sub = status_match.group(1).strip()

        # Use existing subtitle if Goodreads provides no subtitle
        if not subtitle and existing_subtitle:
            subtitle = existing_subtitle

        # Construct the new note content
        content = f"""---
Title: "{short_title}"
Full Title: "{full_title}"
Subtitle: "{subtitle}"
Cover: "{cover}"
Author: "{author}"
Year: "{year}"
Field: "{shelves[shelf].split('/')[-1]}"
Subfield: "{existing_sub}"
Status: "{status}"
---
"""

        # Add the subtitle if it is non-empty
        if subtitle.strip():
            content += f"\n## — {subtitle}\n"

        # Append preserved content
        if preserved_content:
            content += f"\n{preserved_content}\n"

        # Write the updated content back to the note
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
    return processed_books


# for shelf, folder in shelves.items():
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     fetch_books(shelf, folder)

# print('All book notes were updated in Obsidian!')


all_processed_books = set()
for shelf, folder in shelves.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    processed = fetch_books(shelf, folder)
    all_processed_books.update(processed)

# Print summary
print("\n=== Import Summary ===")
print(f"Successfully processed {len(all_processed_books)} books:")
for book in sorted(all_processed_books):
    print(f"✓ {book}")

missing_books = WHITELIST_BOOKS - all_processed_books
if missing_books:
    print(f"\nNot found ({len(missing_books)} books):")
    for book in sorted(missing_books):
        print(f"✗ {book}")

print('\nBook notes update completed!')