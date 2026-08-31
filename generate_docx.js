/**
 * generate_docx.js — DOCX Generator for The Complete AI Engineer
 * 
 * Converts book.html into a Word document using html-to-docx.
 * 
 * Usage: node generate_docx.js
 */

const fs = require('fs');
const path = require('path');
const HTMLtoDOCX = require('html-to-docx');

async function generateDOCX() {
  const bookTitle = 'The_Complete_AI_Engineer';
  const author = 'Ram_Awasthi';
  const outputFile = `${bookTitle}_by_${author}.docx`;

  console.log('📄 Reading book.html...');
  let html = fs.readFileSync(path.resolve(__dirname, 'book.html'), 'utf8');

  // Convert local image src to file:/// absolute paths
  const dir = path.resolve(__dirname).replace(/\\/g, '/');
  html = html.replace(/src="([^"]+\.(?:png|jpg|jpeg|gif|svg))"/g, (match, src) => {
    if (src.startsWith('http') || src.startsWith('file:')) return match;
    return `src="file:///${dir}/${src}"`;
  });

  console.log('📝 Converting to DOCX...');
  const docxBuffer = await HTMLtoDOCX(html, null, {
    table: { row: { cantSplit: true } },
    margins: {
      top: 1224,    // 0.85 inch in twips
      bottom: 1224,
      left: 1080,   // 0.75 inch in twips
      right: 1080,
    },
    title: 'The Complete AI Engineer',
    subject: 'From Absolute Beginner to Production-Ready Engineer',
    creator: 'Ram Awasthi',
  });

  fs.writeFileSync(outputFile, docxBuffer);
  console.log(`✅ DOCX generated: ${outputFile}`);
}

generateDOCX().catch(console.error);
