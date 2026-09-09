/**
 * generate_pdf.js — Production PDF Generator for "The Complete AI Engineer"
 * 
 * Uses Puppeteer (headless Chrome/Edge) to render book.html into a 6×9 inch print-ready PDF.
 * - Auto-detects Chrome or Edge on Windows
 * - Waits for Google Fonts and MathJax 3 CHTML typesetting to complete across all chapters
 * - Renders full-bleed covers (zero margin) and interior pages (0.85in/0.75in print margins)
 * - Merges front cover, interior pages, and back cover using PyMuPDF
 * 
 * Usage: node generate_pdf.js
 */

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

function findBrowser() {
  const candidates = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    process.env.LOCALAPPDATA + '\\Google\\Chrome\\Application\\chrome.exe',
    process.env.LOCALAPPDATA + '\\Microsoft\\Edge\\Application\\msedge.exe',
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  throw new Error('Chrome or Edge not found! Please ensure Google Chrome or Microsoft Edge is installed.');
}

async function generatePDF() {
  const bookTitle = 'The_Complete_AI_Engineer';
  const author = 'Ram_Awasthi';
  const htmlPath = path.resolve(__dirname, 'book.html');
  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

  console.log('🔍 Locating Chromium browser...');
  const executablePath = findBrowser();
  console.log(`✅ Using browser: ${executablePath}`);

  console.log('🚀 Launching headless browser...');
  const browser = await puppeteer.launch({
    executablePath,
    headless: 'new',
    protocolTimeout: 600000, // 10 minutes timeout for CDP Page.printToPDF
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--js-flags=--max-old-space-size=8192'
    ]
  });

  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(600000);
  page.setDefaultTimeout(600000);

  page.on('console', msg => {
    const text = msg.text();
    if (text.includes('MathJax') || text.toLowerCase().includes('chapter')) {
      console.log('  [Console]', text);
    }
  });

  console.log('📄 Loading book.html into renderer...');
  const t0 = Date.now();
  await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });
  console.log(`✅ DOM loaded in ${((Date.now() - t0) / 1000).toFixed(1)}s`);

  console.log('⏳ Typesetting mathematical equations & loading fonts...');
  const t1 = Date.now();
  await page.evaluate(async () => {
    await document.fonts.ready;
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      await window.MathJax.startup.promise;
    }
  });
  console.log(`✅ MathJax typesetting complete in ${((Date.now() - t1) / 1000).toFixed(1)}s`);

  // Extra pause to ensure all layout calculations and fonts are fully settled
  await new Promise(r => setTimeout(r, 3000));

  console.log('🖨️ Emulating print media format...');
  await page.emulateMediaType('print');

  // 1. Generate interior PDF (with standard 6x9 trade paperback margins)
  console.log('📖 Generating interior pages (6in × 9in trade paperback)...');
  const t2 = Date.now();
  await page.pdf({
    path: 'interior.pdf',
    width: '6in',
    height: '9in',
    margin: { top: '0.85in', bottom: '0.85in', left: '0.75in', right: '0.75in' },
    printBackground: true,
    displayHeaderFooter: false,
    timeout: 0
  });
  console.log(`✅ Interior PDF generated in ${((Date.now() - t2) / 1000).toFixed(1)}s`);

  // 2. Query total interior page count to locate back cover
  const interiorPages = parseInt(execSync('python -c "import pymupdf; print(pymupdf.open(\'interior.pdf\').page_count)"').toString().trim(), 10);
  console.log(`📊 Interior contains ${interiorPages} pages.`);

  // 3. Generate front cover (full bleed, zero margin)
  console.log('🖼️ Generating full-bleed front cover...');
  await page.pdf({
    path: 'front_cover.pdf',
    width: '6in',
    height: '9in',
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
    printBackground: true,
    displayHeaderFooter: false,
    pageRanges: '1',
    timeout: 0
  });
  console.log('✅ Front cover generated');

  // 4. Generate back cover (full bleed, zero margin)
  console.log('🖼️ Generating full-bleed back cover...');
  await page.pdf({
    path: 'back_cover.pdf',
    width: '6in',
    height: '9in',
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
    printBackground: true,
    displayHeaderFooter: false,
    pageRanges: `${interiorPages}`,
    timeout: 0
  });
  console.log('✅ Back cover generated');

  await browser.close();

  // 5. Merge using PyMuPDF
  console.log('🔗 Merging front cover, interior manuscript, and back cover...');
  const mergeScript = `
import pymupdf
import os

front = pymupdf.open("front_cover.pdf")
interior = pymupdf.open("interior.pdf")
back = pymupdf.open("back_cover.pdf")
final = pymupdf.open()

total_interior = interior.page_count
print(f"Merging: 1 front cover + {total_interior - 2} interior pages + 1 back cover")

# 1. Insert full-bleed front cover
final.insert_pdf(front, from_page=0, to_page=0)

# 2. Insert interior manuscript (pages 2 to total_interior - 1, 0-indexed as 1 to total_interior - 2)
if total_interior > 2:
    final.insert_pdf(interior, from_page=1, to_page=total_interior - 2)

# 3. Insert full-bleed back cover
final.insert_pdf(back, from_page=0, to_page=0)

output_filename = "${bookTitle}_by_${author}.pdf"
final.save(output_filename, garbage=3, deflate=True)

size_mb = os.path.getsize(output_filename) / (1024 * 1024)
print(f"\\n=======================================================")
print(f"SUCCESS: {output_filename}")
print(f"Total Pages: {final.page_count}")
print(f"File Size: {size_mb:.2f} MB")
print(f"=======================================================\\n")
`;
  fs.writeFileSync('merge.py', mergeScript);

  try {
    execSync('python merge.py', { stdio: 'inherit' });
    console.log(`🎉 Master PDF successfully created: ${bookTitle}_by_${author}.pdf`);
  } catch (e) {
    console.error('⚠️ PDF merge encountered an error:', e.message);
  }

  // Cleanup temp files
  try {
    if (fs.existsSync('interior.pdf')) fs.unlinkSync('interior.pdf');
    if (fs.existsSync('front_cover.pdf')) fs.unlinkSync('front_cover.pdf');
    if (fs.existsSync('back_cover.pdf')) fs.unlinkSync('back_cover.pdf');
    if (fs.existsSync('merge.py')) fs.unlinkSync('merge.py');
  } catch (e) { /* ignore */ }
}

generatePDF().catch(console.error);
