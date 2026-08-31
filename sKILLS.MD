---
name: book-generator
description: >-
  End-to-end book generation workflow. Takes a user's book concept (topic, title,
  chapter outline, length, author details) and produces a complete, publish-ready
  book in multiple formats (PDF, DOCX, EPUB, KDP ZIP) with professional cover art,
  KDP paperback wrap cover, back cover, social media launch posts (LinkedIn,
  Instagram), and all files needed for Amazon Kindle self-publishing. Handles
  everything from content writing to print-ready formatting.
---

# Book Generator — Full Publishing Pipeline

## Overview

This skill captures an end-to-end workflow for generating a complete, publish-ready book from a user's concept. It was originally built for **"Beyond the Big Bang: A New Theory of Everything"** by Ram Awasthi — a 20-chapter, 4-part science/philosophy book — and is designed to be reused for any future book project.

The workflow produces:
- **Book content** as a structured, print-ready HTML manuscript
- **PDF** (6×9 inch trade paperback, interior + covers merged)
- **DOCX** (Word document)
- **EPUB** (e-reader format with chapter navigation)
- **KDP ZIP** (Kindle Direct Publishing reflowable HTML upload)
- **Front cover** (AI-generated, high-resolution)
- **Back cover** (with synopsis, tagline, and author name)
- **Full wrap cover** (front + spine + back, 300 DPI, KDP-compliant)
- **Social media launch posts** (LinkedIn and Instagram)

---

## Prerequisites

### System Requirements
- **Node.js** (v18+ recommended)
- **Python 3** with `pymupdf` and `Pillow` packages
- **Google Chrome or Microsoft Edge** (for Puppeteer-based PDF generation)
- **npm** packages (installed via `npm install`):
  - `puppeteer-core` — headless browser PDF generation
  - `cheerio` — HTML parsing for EPUB/KDP extraction
  - `html-to-docx` — DOCX conversion
  - `epub-gen-memory` — EPUB generation
  - `archiver` — ZIP file creation

### Install Dependencies
```bash
npm init -y
npm install puppeteer-core cheerio html-to-docx epub-gen-memory archiver
pip install pymupdf Pillow
```

---

## Workflow

### Phase 1: Gather Book Details from User

Collect the following information through conversation:

1. **Book title** and **subtitle**
2. **Author name**
3. **Book topic/concept** — What is the book about? What is the core thesis?
4. **Target length** — Approximate word count or page count (e.g., ~200 pages, ~60,000 words)
5. **Structure** — How many parts/sections? How many chapters? Provide a chapter outline if available
6. **Genre/category** — Science, fiction, self-help, philosophy, etc.
7. **Target audience** — Who is this book for?
8. **Tone** — Academic, conversational, storytelling, poetic, etc.
9. **Trim size** — Default is 6×9 inches (standard trade paperback)
10. **ISBN** (if available) — Or note that one will be assigned by KDP
11. **Amazon ASIN/links** (if already listed)
12. **Author bio** — Brief paragraph for the "About the Author" page

> [!IMPORTANT]
> Do NOT start writing until you have at minimum: title, author, topic/thesis, approximate length, and chapter outline. If the user has handwritten notes or a rough draft, ask them to share key points per chapter.

---

### Phase 2: Generate the Book Content (book.html)

Create a single `book.html` file containing the entire manuscript. This is the **master source file** from which all other formats are derived.

#### HTML Structure

The book.html must follow this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{Book Title} — {Subtitle}</title>
  <link rel="stylesheet" href="styles.css">
  <style>
    /* Cover-specific styles (full-bleed, no margins) */
    .cover-page { page-break-after: always; margin: 0; padding: 0; width: 6in; height: 9in; overflow: hidden; }
    .cover-page img { width: 100%; height: 100%; object-fit: contain; display: block; }
    .back-cover-page { break-before: right; margin: 0; padding: 0; width: 6in; height: 9in; overflow: hidden; background: linear-gradient(135deg, #050a15, #0a1128, #050a15); }
    .back-cover-overlay { /* ... absolute positioned overlay with synopsis */ }
  </style>
</head>
<body>
  <!-- FRONT COVER -->
  <div class="cover-page"><img src="front_cover.png" alt="..."></div>

  <!-- TITLE PAGE -->
  <div class="title-page">
    <div class="book-title">{Title}</div>
    <div class="book-subtitle">{Subtitle}</div>
    <div class="ornament">✦ ✦ ✦</div>
    <div class="author-name">{Author}</div>
  </div>

  <!-- COPYRIGHT PAGE -->
  <div class="copyright-page">
    <p><strong>{Full Title}</strong></p>
    <p>Copyright © {Year} {Author}</p>
    <p>All rights reserved. ...</p>
    <p>First Edition, {Year}</p>
    <p>ISBN: {ISBN}</p>
  </div>

  <!-- TABLE OF CONTENTS -->
  <div class="toc">
    <h2>Contents</h2>
    <div class="toc-part">Part I — {Part Title}</div>
    <div class="toc-entry"><span class="toc-chapter-num">1</span><span class="toc-chapter-title">{Chapter Title}</span></div>
    <!-- ... more entries ... -->
  </div>

  <!-- PART PAGES -->
  <div class="part-page">
    <div class="part-number">Part I</div>
    <div class="part-title">{Part Title}</div>
    <div class="part-ornament">✦ ✦ ✦</div>
  </div>

  <!-- CHAPTERS -->
  <div class="chapter">
    <div class="chapter-header">
      <span class="chapter-number">Chapter One</span>
      <h2 class="chapter-title">{Title}</h2>
      <span class="chapter-ornament">✦</span>
    </div>
    <div class="epigraph">
      <p>"{Quote}"</p>
      <p class="attribution">— {Attribution}</p>
    </div>
    <div class="chapter-body">
      <p>{Opening paragraph — first letter gets drop cap via CSS}</p>
      <h3>{Section heading}</h3>
      <p>{Content...}</p>
    </div>
  </div>

  <!-- GLOSSARY (optional) -->
  <div class="glossary">...</div>

  <!-- ABOUT THE AUTHOR -->
  <div class="about-author">...</div>

  <!-- BACK COVER -->
  <div class="back-cover-page">
    <div class="back-cover-overlay">
      <div class="back-tagline">{Tagline questions}</div>
      <div class="back-synopsis"><p>{Synopsis}</p></div>
      <div class="back-quote">"{Pull quote}"</div>
      <div class="back-author">{Author}</div>
    </div>
  </div>
</body>
</html>
```

#### CSS Design System (styles.css)

Create a professional book CSS with:
- **Fonts**: Merriweather (body), Playfair Display (headings), Source Sans 3 (UI elements) via Google Fonts
- **Page setup**: `@page { size: 6in 9in; margin: 0.85in 0.75in; }` with alternating left/right margins
- **Typography**: 11pt base, 1.72 line-height, justified text with hyphens, `orphans: 3; widows: 3`
- **Drop caps**: `::first-letter` on first paragraph of each chapter
- **Color palette**: `--color-text: #1a1a1a`, `--color-accent: #2c3e6b`, `--color-muted: #555`
- **Print optimization**: `@media print` rules for page breaks, orphan/widow control

> [!TIP]
> Write each chapter to approximately 3,000–4,000 words for a standard non-fiction book. Include epigraphs (relevant quotes) at the start of each chapter for polish.

#### Content Writing Guidelines

- **Each chapter** should open with an engaging hook paragraph
- Use **section headings** (`<h3>`) to break up long chapters
- Include **blockquotes** for important quotes or key concepts
- End each chapter with a **bridge paragraph** that leads into the next chapter
- Use **analogies and metaphors** to make complex topics accessible
- Write the **back cover synopsis** as a compelling marketing pitch (3 short paragraphs)
- Write the **glossary** with `<dl>`, `<dt>`, `<dd>` elements

---

### Phase 3: Generate the Front Cover

Use the `generate_image` tool to create a high-resolution front cover image.

**Prompt guidelines for cover art:**
- Include the book title, subtitle, and author name in the prompt
- Specify the genre aesthetic (e.g., "cosmic, deep space, scientific, ethereal")
- Request text overlay with the title prominently displayed
- Use aspect ratio `2:3` (matches 6×9 trim size)
- Save as `front_cover.png`

> [!IMPORTANT]
> The cover image must be high quality. Iterate on the prompt if the first generation is not satisfactory. The cover is the single most important marketing asset.

---

### Phase 4: Generate Output Formats

Run each generator script in sequence:

#### 4a. PDF Generation (`generate_pdf.js`)

```bash
node generate_pdf.js
```

**What it does:**
1. Launches headless Chrome/Edge via Puppeteer
2. Loads `book.html` with `waitUntil: 'networkidle0'`
3. Waits for fonts to load (`document.fonts.ready`)
4. Generates interior pages with margins: `top: 0.85in, bottom: 0.85in, left: 0.75in, right: 0.75in`
5. Generates full-bleed covers separately (zero margins)
6. Merges covers + interior using Python `pymupdf`: front cover → interior pages → back cover
7. Output: `{BookTitle}_by_{Author}.pdf`

**Key details:**
- Page size: 6in × 9in
- The script auto-detects Chrome or Edge on Windows
- Interior and covers are rendered separately because covers need zero margins (full-bleed) while interior needs print margins
- PyMuPDF (`pymupdf`) handles the final PDF merge

#### 4b. DOCX Generation (`generate_docx.js`)

```bash
node generate_docx.js
```

**What it does:**
1. Reads `book.html`
2. Converts local image `src` attributes to `file:///` absolute paths
3. Converts HTML to DOCX using `html-to-docx` with matching margins (0.85in top/bottom, 0.75in left/right)
4. Output: `{BookTitle}_by_{Author}.docx`

#### 4c. EPUB Generation (`generate_epub.js`)

```bash
node generate_epub.js
```

**What it does:**
1. Parses `book.html` with Cheerio
2. Extracts title, author from CSS class selectors (`.book-title`, `.author-name`)
3. Splits content into chapters by iterating `body > div` elements
4. Part pages and chapters become EPUB navigation entries
5. Includes front cover image
6. Adds minimal reflowable CSS
7. Output: `{BookTitle}.epub`

#### 4d. KDP ZIP Generation (`generate_kdp_zip.js`)

```bash
node generate_kdp_zip.js
```

**What it does:**
1. Reads `book.html` and strips external stylesheet
2. Removes front cover page (KDP handles cover separately)
3. Injects KDP-safe inline CSS (simple serif fonts, page breaks, basic layout)
4. Removes absolute positioning and gradient backgrounds (not supported in reflowable Kindle format)
5. Writes cleaned HTML as `index.html`
6. Zips into `{BookTitle}_KDP.zip`
7. Output: ZIP file ready for Kindle Direct Publishing upload

---

### Phase 5: Generate KDP Paperback Wrap Cover

For **paperback** publishing on KDP, generate a full wrap cover (back + spine + front) at 300 DPI.

#### Method A: Node.js/Puppeteer (`generate_kdp_cover.js`)

```bash
node generate_kdp_cover.js
```

**KDP Cover Specifications:**
- **Total dimensions**: 12.556in × 9.250in at 300 DPI = 3767px × 2775px
- **Spine width**: Calculated from page count (0.306in ≈ 92px for ~200 pages)
- **Each cover panel**: (3767 - 92) / 2 = ~1838px wide
- **Layout**: Back Cover (left) | Spine (center) | Front Cover (right)

**Spine formula**: `spine_width = page_count × 0.0025in` (for white paper). Adjust for cream paper: `× 0.0028in`.

Use KDP's [Cover Calculator](https://kdp.amazon.com/en_US/cover-calculator) to get exact dimensions for your page count.

#### Method B: Python/Pillow (`create_wrap.py`)

```bash
python create_wrap.py
```

**What it does:**
1. Extracts back cover from the generated PDF at 300 DPI using PyMuPDF
2. Loads original front cover image
3. Trims white margins from back cover render
4. Resizes both to exact cover panel dimensions using `ImageOps.fit` (object-fit: cover)
5. Creates canvas at full wrap dimensions with dark background for spine
6. Pastes back cover (left), spine text (center, rotated 270°), front cover (right)
7. Outputs JPEG (300 DPI) and PDF

**Spine text**: Title in gold (#e8d5a3), author in white, rotated to read top-to-bottom.

---

### Phase 6: Generate Social Media Launch Posts

Create compelling launch posts for:

#### LinkedIn Post (`linkedin_post.txt`)
- **Tone**: Professional, personal storytelling, inspirational
- **Structure**:
  1. Hook line (attention-grabbing opening)
  2. Personal backstory (why you wrote this book)
  3. The pivotal realization moment
  4. Book content overview with bullet points (use ✦ or emoji markers)
  5. Emotional appeal and call to action
  6. Amazon links (India + US/Global)
  7. Hashtags (25-30 relevant tags)
- **Length**: 500-800 words
- **Emojis**: Use sparingly but strategically (📖, 🌌, 💡, 📕, 🇮🇳, 🇺🇸)

#### Instagram Post (`instagram_post.txt`)
- **Tone**: Casual, curiosity-driven, visual, punchy
- **Structure**:
  1. Hook question (provocative/curious opening)
  2. Brief personal story
  3. "What's Inside" section with emoji bullets (🔭, 🕳️, ⚛️, 🧬, 💥, 🧠)
  4. Emotional positioning statement
  5. Amazon links
  6. Engagement CTA ("Tag someone who...", "Drop a 🚀 if...")
  7. Hashtags (30-35 tags, including platform-specific ones like #Bookstagram)
- **Length**: 300-500 words

---

## File Structure Summary

After the full workflow, the project directory should contain:

```
project/
├── book.html                           # Master HTML manuscript (source of truth)
├── styles.css                          # Print-ready CSS design system
├── front_cover.png                     # AI-generated front cover image
├── back_cover.png                      # Rendered back cover image
├── package.json                        # Node.js dependencies
├── node_modules/                       # Installed npm packages
│
├── generate_pdf.js                     # PDF generator (Puppeteer + PyMuPDF merge)
├── generate_docx.js                    # DOCX generator (html-to-docx)
├── generate_epub.js                    # EPUB generator (epub-gen-memory + Cheerio)
├── generate_kdp_zip.js                 # KDP HTML ZIP generator
├── generate_kdp_cover.js              # KDP wrap cover generator (Puppeteer)
├── create_wrap.py                      # Alternative wrap cover generator (Pillow)
├── merge.py                            # Auto-generated PDF merge helper
│
├── {Title}_by_{Author}.pdf            # Final print-ready PDF (covers + interior)
├── {Title}_by_{Author}.docx           # Word document
├── {Title}.epub                        # EPUB e-book
├── {Title}_KDP.zip                    # Kindle Direct Publishing upload
├── {Title}_Full_Cover.jpg             # 300 DPI wrap cover (JPEG)
├── {Title}_Full_Cover.pdf             # 300 DPI wrap cover (PDF)
│
├── linkedin_post.txt                   # LinkedIn launch post
└── instagram_post.txt                  # Instagram launch post
```

---

## Common Mistakes

1. **Forgetting to wait for fonts** — The PDF generator must call `document.fonts.ready` and add a delay (5 seconds) before rendering. Without this, Google Fonts won't load and the PDF will use fallback system fonts.

2. **Using margins for cover pages** — Front and back covers MUST be rendered with zero margins (full-bleed). The interior pages use 0.85in/0.75in margins. The PDF generator handles this by rendering covers and interior separately, then merging.

3. **KDP cover dimensions** — The spine width varies based on page count. Always recalculate using the formula `spine_width = page_count × 0.0025in` (white paper) or use KDP's Cover Calculator. Getting this wrong will cause KDP to reject the cover.

4. **EPUB absolute positioning** — EPUB is a reflowable format. Never include CSS with `position: absolute`, fixed widths in inches, or gradient backgrounds. The KDP ZIP generator specifically strips these out.

5. **Not testing the PDF on an actual e-reader or print preview** — Always open the generated PDF in a PDF reader and check page breaks, drop caps rendering, and that the cover pages are truly full-bleed with no white borders.

---

## Quick Start

To generate a new book from scratch:

```
1. User provides: title, author, outline, length requirements, topic
2. Agent creates: styles.css, book.html (full manuscript)
3. Agent generates: front_cover.png (via generate_image tool)
4. Agent creates: generate_pdf.js, generate_docx.js, generate_epub.js, generate_kdp_zip.js, generate_kdp_cover.js, create_wrap.py
5. Agent runs: npm install
6. Agent runs: node generate_pdf.js → produces PDF
7. Agent runs: node generate_docx.js → produces DOCX
8. Agent runs: node generate_epub.js → produces EPUB
9. Agent runs: node generate_kdp_zip.js → produces KDP ZIP
10. Agent runs: node generate_kdp_cover.js → produces wrap cover
11. Agent creates: linkedin_post.txt, instagram_post.txt
12. All files delivered to user
```

---

## Reference Implementation

This skill was built from the production workflow used for:

- **Book**: *Beyond the Big Bang: A New Theory of Everything*
- **Author**: Ram Awasthi
- **Specs**: 20 chapters, 4 parts, ~200 pages, 6×9 inch trade paperback
- **Published on**: Amazon Kindle (ASIN: B0HDSSZMZL)
- **ISBN**: 9798191729602

All generator scripts, CSS, and HTML structure in this workspace serve as reference implementations.
