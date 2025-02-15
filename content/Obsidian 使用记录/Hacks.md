
**Transferring from Mac Notes to Obsidian**
- Straight copy-and-pasting frustratingly loses all formatting or creates extra line breaks, and images cannot be transferred
- To get around that, I first copy from Mac Notes and paste directly to the Bear App (free on AppStore), then export as markdown with the option "Export attachments", which creates a folder with the same name of the .md note file that contains all the images.
- Because in this exported .md note file all the images are linked by the folder name that is the note name, create in Obsidian a folder of that same name so that when you drag the note and all the images into that folder, it still recognizes which image is which.
- Check that the imported Obsidian note contains the images indeed, and with the 'automatically update internal links' option turned on, you can safely store them elsewhere(such as a dedicated `attachments` folder.

**Subtitles & Table of Contents**
Added `if (text.startsWith("–")) return` to `toc.ts` in `quartz/plugins` Ignore headings that start with "–" because I format all my subtitles like that.
![[Screenshot 2025-02-13 at 22.41.25.png]]

