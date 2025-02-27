```dataviewjs
const books = dv.pages("")
    .where(p => p.Cover && p.Title)
    .sort(p => p.file.mtime, "desc")
    .limit(3);

let table = "| Cover | Title | Author | Year |\n|---|---|---|---|\n";

for (let book of books) {
    let cover = `<img src="${book.Cover}" width="100"/>`;
    table += `| ${cover} | [[${book.Title}]] | ${book.Author} | ${book.Year} |\n`;
}

dv.paragraph("Copy this Markdown table and paste it before publishing:");
dv.paragraph("```markdown\n" + table + "```");
```
