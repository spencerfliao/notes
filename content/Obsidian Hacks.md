
**Transferring from Mac Notes to Obsidian**
- Straight copy-and-pasting frustratingly loses all formatting or creates extra line breaks, and images cannot be transferred
- To get around that, I first copy from Mac Notes and paste directly to the Bear App (free on AppStore), then export as markdown with the option "Export attachments", which creates a folder with the same name of the .md note file that contains all the images.
- Because in this exported .md note file all the images are linked by the folder name that is the note name, create in Obsidian a folder of that same name so that when you drag the note and all the images into that folder, it still recognizes which image is which.
- Check that the imported Obsidian note contains the images indeed, and with the 'automatically update internal links' option turned on, you can safely store them elsewhere(such as a dedicated `attachments` folder.

**Subtitles & Table of Contents**
Added `if (text.startsWith("–")) return` to `toc.ts` in `quartz/plugins` Ignore headings that start with "–" because I format all my subtitles like that.


**Syncing Quartz Every Hour When Changes Exist**
I set up a Cron Job for updating the quartz site every hour but only if changes exist.
In Terminal:
```
crontab -e
0 * * * * cd /path/to//quartz-repo && if [ -n "$(git status --porcelain)" ]; then git add . && git commit -m "Auto-sync notes from iCloud" && git push origin v4; fi
```
- if you're using mac terminal, save and exit by pressing the escape button and entering `:wq`
- `git status --porcelain` checks if there are uncommitted changes.
- the sync only runs if changes exist, which ensures no unnecessary commits!


网站上还可以放：
- 我的愿望清单（商品链接）
- 支持我的梦想（房车，帆船）
- report a bug
- comments

If my writing means something to you or has brightened your life, consider:
- Donating to __
- Leaving me a nice email or an anonymous compliment!
I prefer messages over donations.