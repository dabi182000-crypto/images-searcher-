# Product Finder (GitHub Pages)

A static product search page that works with any Excel sheet and an image folder. The site has no server, framework, or build tooling. The only preparation step is converting the workbook to `products.json`.

## Private browser upload

Use **Add Excel & images** in the website to choose an `.xlsx` workbook and its image folder directly from your computer. This is useful when the product data must not be public: the files stay in your browser session and are not uploaded to GitHub.

Choose the **Image filename / Oracle code column** in the setup panel, then search or scan a supplier reference. The site finds that reference in Excel and uses the Oracle-code value from the same row to display the correct local image.

## Repository layout

```
index.html        The complete static website
build.py          Converts the Excel workbook to JSON
products.xlsx     Your workbook (add this at the repository root)
products.json     Generated file used by the website
images/           Product images
  SKU-1234.jpg
  SKU-1234_1.jpg
```

## Generate the product data

Install Python 3 and the Excel reader once:

```bash
pip install openpyxl
```

Put your workbook at the repository root as `products.xlsx`, then run:

```bash
python build.py
```

This reads the first sheet and uses the first row as the headers exactly as written. To select a different sheet:

```bash
python build.py --sheet "Sheet name"
```

Run `python build.py` again whenever the Excel file changes, then commit and push the updated `products.json`.

Formula cells written as `=HYPERLINK("url","label")` are stored as the URL so they open normally in the product modal.

## Image naming rule

When opening the site for the first time, choose the **Image filename / Oracle code column**: the column whose values match image filenames. The image filename base must be the exact value in that chosen column:

```
images/SKU-1234.jpg
images/HH0006901_1.png
```

The card checks `jpg`, `jpeg`, `png`, `webp`, then `gif`. The optional extra images use `_1` through `_5` (for example `SKU-1234_1.jpg` and `SKU-1234_2.jpg`) and appear as thumbnails after opening a product. The selected columns are saved in the browser, and **Change columns** lets you update them later. This means you can search a supplier reference, while the site uses the Oracle-code value in the same Excel row to locate its image.

You can search by typing a reference number, or use **Scan reference** to scan a barcode containing that reference number with a phone camera. Camera barcode scanning works in supported modern browsers; a printed reference with no barcode should be typed into the search box.

## Publish with GitHub Pages

1. Create a GitHub repository and upload `index.html`, `build.py`, `products.xlsx`, generated `products.json`, and the `images` folder.
2. Commit and push them to the `main` branch.
3. In GitHub, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select branch **main**, folder **/(root)**, then click **Save**.
6. After GitHub finishes deploying, open the Pages URL shown on that screen.

For local testing, use a small local server rather than opening `index.html` directly, because browsers block JSON requests from local files:

```bash
python -m http.server
```

Then visit `http://localhost:8000`.
