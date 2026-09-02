/**
 * generate_epub.js — EPUB Generator for The Complete AI Engineer
 * 
 * Parses book.html with Cheerio and generates a navigable EPUB file.
 * Handles images cleanly for offline e-readers.
 * 
 * Usage: node generate_epub.js
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const epub = require('epub-gen-memory').default;

async function generateEPUB() {
  const bookTitle = 'The_Complete_AI_Engineer';
  const outputFile = `${bookTitle}.epub`;

  console.log('📄 Reading book.html...');
  const html = fs.readFileSync(path.resolve(__dirname, 'book.html'), 'utf8');
  const $ = cheerio.load(html);

  // Extract title and author
  const title = $('.book-title').first().text().trim() || 'The Complete AI Engineer';
  const author = $('.author-name').first().text().trim() || 'Ram Awasthi';

  // Extract chapters
  const chapters = [];
  $('body > div').each((i, el) => {
    const div = $(el);
    const classes = div.attr('class') || '';

    if (classes.includes('cover-page') || classes.includes('back-cover-page')) return;

    let chapterTitle = 'Section';

    if (classes.includes('title-page')) {
      chapterTitle = 'Title Page';
    } else if (classes.includes('copyright-page')) {
      chapterTitle = 'Copyright';
    } else if (classes.includes('message-page')) {
      chapterTitle = 'A Message From the Book';
    } else if (classes.includes('toc')) {
      chapterTitle = 'Table of Contents';
    } else if (classes.includes('part-page')) {
      chapterTitle = div.find('.part-number').text() + ' — ' + div.find('.part-title').text();
    } else if (classes.includes('chapter')) {
      const num = div.find('.chapter-number').text();
      const name = div.find('.chapter-title').text();
      chapterTitle = num ? `${num}: ${name}` : name;
    } else if (classes.includes('project-section')) {
      chapterTitle = div.find('.project-title').text() || 'Project';
    } else if (classes.includes('glossary')) {
      chapterTitle = 'Glossary';
    } else if (classes.includes('about-author')) {
      chapterTitle = 'About the Author';
    } else if (classes.includes('github-repo-guide')) {
      chapterTitle = 'Official Companion Code Repository';
    }

    // Clean HTML for EPUB
    let content = $.html(el);
    content = content.replace(/position:\s*absolute/g, 'position: static');
    content = content.replace(/background:\s*linear-gradient[^;]+;/g, '');
    content = content.replace(/width:\s*6in/g, 'width: 100%');
    content = content.replace(/height:\s*9in/g, 'height: auto');

    // Replace local images with accessible text links for EPUB readers
    content = content.replace(/<img[^>]*src="github_repo_qr\.png"[^>]*>/gi, 
      '<p style="text-align: center; font-weight: bold; border: 1px solid #1b4965; padding: 12px;">🔗 <a href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions">Repository Link: https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions</a></p>');
    content = content.replace(/<img[^>]*>/gi, '');

    chapters.push({
      title: chapterTitle,
      content: content,
    });
  });

  console.log(`📚 Generating EPUB with ${chapters.length} chapters...`);

  const options = {
    title: title,
    author: author,
    publisher: 'Self-Published',
    css: `
      body { font-family: Georgia, serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; }
      h1, h2, h3 { font-family: Georgia, serif; color: #0d1b2a; }
      pre, code { font-family: monospace; font-size: 0.9em; background: #f4f4f0; padding: 2px 4px; }
      pre { padding: 8px; border-radius: 4px; white-space: pre-wrap; }
      blockquote { border-left: 3px solid #5fa8d3; padding-left: 12px; font-style: italic; color: #555; }
      table { border-collapse: collapse; width: 100%; margin: 1em 0; }
      th, td { border: 1px solid #ddd; padding: 6px 8px; text-align: left; }
      th { background: #1b4965; color: white; }
    `
  };

  const epubBuffer = await epub(options, chapters);
  fs.writeFileSync(outputFile, epubBuffer);
  console.log(`✅ EPUB generated: ${outputFile}`);
}

generateEPUB().catch(console.error);
