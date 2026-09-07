# Product Search

A tiny static site that lets you search a product catalog by **any** field and see each
product's image. No build step, no framework — just `index.html`, a JSON file, and a folder
of images. Hosts cleanly on GitHub Pages.

## Repo layout

```
.
├── index.html        the whole app (HTML + CSS + JS in one file)
├── build.py          converts products.xlsx → products.json
├── products.xlsx     your spreadsheet (you provide)
├── products.json     generated from the xlsx
├── images/           your product images
│   ├── ABC-123.jpg
│   ├── ABC-123_1.jpg      (optional extra images: _1 .. _5)
│   └── ...
└── README.md
```

## Generate `products.json` from Excel

Whenever you update `products.xlsx`:

```bash
pip install openpyxl        # once
python build.py             # reads products.xlsx, writes products.json
```

Flags:

- `--input path.xlsx` / `-i` — input file (default `products.xlsx`)
- `--output path.json` / `-o` — output file (default `products.json`)
- `--sheet "Sheet Name"` / `-s` — pick a specific sheet (default: first sheet)

Notes on the conversion:

- Row 1 is used as column headers **verbatim**. No column is hard-coded.
- `=HYPERLINK("url", "label")` cells are resolved to the URL.
- Native cell hyperlinks are resolved to their target URL.
- Every column is preserved as-is.

## Image naming rule

Image filenames must equal the value of the "code column" you pick in the app,
plus one of these extensions (tried in order):

```
.jpg  .jpeg  .png  .webp  .gif
```

Examples: if the code column contains `SKU-1234`, the app will look for
`images/SKU-1234.jpg`, then `.jpeg`, then `.png`, etc.

Extra images per product are supported by appending `_1` … `_5`:

```
images/SKU-1234.jpg      # main
images/SKU-1234_1.jpg    # extra
images/SKU-1234_2.png    # extra
```

Extras show as a thumbnail strip in the modal.

## First-run setup

Open the site and pick:

1. **Code column** — the column whose value matches image filenames.
2. **Primary display columns** (1–3) — shown on each card (title, subtitle, badge).

The choice is saved in your browser's `localStorage`. Use the **change columns**
link in the header to reopen the panel.

## Features

- Case-insensitive substring search across every column
- "X of N products" live count next to the search box
- Click a card → modal with the full image, thumbnails of extra images, and every
  field as a definition list (URL values render as clickable links)
- Esc or clicking the backdrop closes the modal
- Responsive, mobile-friendly, no external CSS/JS

## Deploy to GitHub Pages

1. Push this repo to GitHub (make sure `products.json` and `images/` are committed).
2. In the repo on GitHub: **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Set **Branch** to `main` and folder to `/ (root)`, then **Save**.
5. Wait a minute — your site will be at `https://<user>.github.io/<repo>/`.

That's it. To publish changes, regenerate `products.json`, commit, and push.
