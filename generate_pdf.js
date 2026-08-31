/**
 * generate_pdf.js — PDF Generator for The Complete AI Engineer
 * 
 * Uses Puppeteer (headless Chrome/Edge) to render book.html into a print-ready PDF.
 * Renders covers and interior separately (different margin requirements), then
 * merges them using Python's PyMuPDF.
 * 
 * Usage: node generate_pdf.js
 * Prerequisites: npm install puppeteer-core; pip install pymupdf
 */

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

// Auto-detect browser on Windows
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
  throw new Error('Chrome or Edge not found! Install one of them.');
}

async function generatePDF() {
  const bookTitle = 'The_Complete_AI_Engineer';
  const author = 'Ram_Awasthi';
  const htmlPath = path.resolve(__dirname, 'book.html');
  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

  console.log('🔍 Finding browser...');
  const executablePath = findBrowser();
  console.log(`✅ Using: ${executablePath}`);

  const browser = await puppeteer.launch({
    executablePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  console.log('📄 Loading book.html...');
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 120000 });

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 5000));
  console.log('✅ Fonts loaded');

  // Generate interior PDF (with margins)
  console.log('📖 Generating interior pages...');
  await page.pdf({
    path: 'interior.pdf',
    width: '6in',
    height: '9in',
    margin: { top: '0.85in', bottom: '0.85in', left: '0.75in', right: '0.75in' },
    printBackground: true,
    displayHeaderFooter: false,
  });

  // Generate covers (full-bleed, no margins)
  console.log('🖼️ Generating cover pages...');
  await page.pdf({
    path: 'covers.pdf',
    width: '6in',
    height: '9in',
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
    printBackground: true,
    displayHeaderFooter: false,
    pageRanges: '1',  // Just front cover
  });

  await browser.close();

  // Merge using PyMuPDF
  console.log('🔗 Merging PDFs...');
  const mergeScript = `
import pymupdf
covers = pymupdf.open("covers.pdf")
interior = pymupdf.open("interior.pdf")
final = pymupdf.open()
# Add front cover
final.insert_pdf(covers, from_page=0, to_page=0)
# Add interior (skip cover pages)
if interior.page_count > 2:
    final.insert_pdf(interior, from_page=1, to_page=interior.page_count-2)
else:
    final.insert_pdf(interior)
# Add back cover (last page of interior)
if interior.page_count > 1:
    final.insert_pdf(interior, from_page=interior.page_count-1)
final.save("${bookTitle}_by_${author}.pdf")
print(f"✅ Final PDF: {final.page_count} pages")
`;
  fs.writeFileSync('merge.py', mergeScript);

  try {
    execSync('python merge.py', { stdio: 'inherit' });
    console.log(`✅ PDF generated: ${bookTitle}_by_${author}.pdf`);
  } catch (e) {
    console.log('⚠️ PDF merge failed. You may need to install pymupdf: pip install pymupdf');
    console.log('   The interior.pdf file is still available.');
  }

  // Cleanup temp files
  try {
    fs.unlinkSync('interior.pdf');
    fs.unlinkSync('covers.pdf');
  } catch (e) { /* ignore */ }
}

generatePDF().catch(console.error);
