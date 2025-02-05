```dataviewjs
const books = dv.pages('""')
  .where(b => b.Shelf)  // Only books with Shelf metadata
  .sort(b => b.Year, "desc"); // Sort by Year (newest first)

// Render a table manually
dv.table(["Cover", "Title", "Author", "Year", "Shelf", "Status"], 
  books.map(b => [
    `![Cover](${b.Cover})`,  // Show image correctly
    b.Title, 
    b.Author, 
    b.Year, 
    b.Shelf, 
    b.Status
  ])
);
```
