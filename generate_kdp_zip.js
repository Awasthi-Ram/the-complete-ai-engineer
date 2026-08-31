/**
 * generate_kdp_zip.js — KDP ZIP Generator for The Complete AI Engineer
 * 
 * Creates a Kindle Direct Publishing-ready ZIP file with cleaned HTML.
 * Strips absolute positioning, gradients, and other unsupported CSS.
 * 
 * Usage: node generate_kdp_zip.js
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const archiver = require('archiver');

async function generateKDP() {
  const bookTitle = 'The_Complete_AI_Engineer';
  const outputFile = `${bookTitle}_KDP.zip`;

  console.log('📄 Reading book.html...');
  const html = fs.readFileSync(path.resolve(__dirname, 'book.html'), 'utf8');
  const $ = cheerio.load(html);

  // Remove front cover (KDP handles cover separately)
  $('.cover-page').remove();
  // Remove back cover (not used in KDP reflowable)
  $('.back-cover-page').remove();
  // Remove external stylesheet link
  $('link[rel="stylesheet"]').remove();

  // Inject KDP-safe inline CSS
  const kdpCSS = `
    <style>
      body { font-family: Georgia, "Times New Roman", serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; margin: 1em; }
      h1, h2, h3, h4 { font-family: Georgia, serif; color: #0d1b2a; page-break-after: avoid; }
      h2 { font-size: 1.5em; margin-top: 1.5em; }
      h3 { font-size: 1.2em; color: #1b4965; }
      pre, code { font-family: "Courier New", monospace; font-size: 0.88em; background: #f0f0f0; }
      pre { padding: 10px; border: 1px solid #ccc; white-space: pre-wrap; word-wrap: break-word; page-break-inside: avoid; }
      code { padding: 1px 4px; }
      pre code { background: transparent; padding: 0; }
      blockquote { border-left: 3px solid #5fa8d3; padding-left: 15px; font-style: italic; color: #555; }
      table { border-collapse: collapse; width: 100%; margin: 1em 0; }
      th, td { border: 1px solid #999; padding: 5px 8px; text-align: left; font-size: 0.9em; }
      th { background: #1b4965; color: white; }
      .chapter { page-break-before: always; }
      .part-page { page-break-before: always; text-align: center; padding-top: 40%; }
      .epigraph { font-style: italic; color: #666; margin: 1em 2em; border-left: 2px solid #ccc; padding-left: 1em; }
      .key-insight { background: #fffde7; border-left: 4px solid #f4b400; padding: 10px 15px; margin: 1em 0; }
      .problem { border: 1px solid #ddd; padding: 10px; margin: 1em 0; background: #fafafa; }
      .solution { background: #f5f5f5; padding: 10px; border-left: 3px solid #1b4965; margin-top: 8px; }
      .project-section { background: #f1f8e9; border: 2px solid #4caf50; padding: 15px; margin: 1.5em 0; }
      .scaffold-notice { background: #fff3e0; border: 2px dashed #ff9800; padding: 10px; text-align: center; color: #e65100; }
    </style>
  `;

  // Replace existing <style> block
  $('head style').remove();
  $('head').append(kdpCSS);

  // Clean CSS from inline styles
  $('[style]').each((i, el) => {
    let style = $(el).attr('style') || '';
    style = style.replace(/position:\s*absolute[^;]*/gi, '');
    style = style.replace(/background:\s*linear-gradient[^;]*/gi, '');
    style = style.replace(/width:\s*6in/gi, 'width: 100%');
    style = style.replace(/height:\s*9in/gi, 'height: auto');
    style = style.replace(/overflow:\s*hidden/gi, '');
    if (style.trim()) {
      $(el).attr('style', style);
    } else {
      $(el).removeAttr('style');
    }
  });

  const cleanedHTML = $.html();

  console.log('📦 Creating KDP ZIP...');
  const output = fs.createWriteStream(outputFile);
  const archive = archiver('zip', { zlib: { level: 9 } });

  archive.pipe(output);
  archive.append(cleanedHTML, { name: 'index.html' });

  // Include front cover if it exists
  const coverPath = path.resolve(__dirname, 'front_cover.png');
  if (fs.existsSync(coverPath)) {
    archive.file(coverPath, { name: 'front_cover.png' });
  }

  await archive.finalize();

  return new Promise((resolve) => {
    output.on('close', () => {
      console.log(`✅ KDP ZIP generated: ${outputFile} (${archive.pointer()} bytes)`);
      resolve();
    });
  });
}

generateKDP().catch(console.error);
