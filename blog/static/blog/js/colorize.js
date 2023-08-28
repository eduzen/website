function splitHTMLByWords(html) {
  return html.split(/(<.*?>|[\s\n]+)/).filter(chunk => chunk.trim() !== "");
}

function colorizeParagraph(paragraphElement) {
  const colors = [
    'text-blue-400', 'text-green-400', 'text-indigo-400',
    'text-orange-400', 'text-pink-400', 'text-purple-400',
    'text-teal-400', 'text-yellow-400'
  ];

  function randomColor() {
    return colors[Math.floor(Math.random() * colors.length)];
  }

  function colorizeContent(content, percentage) {
    let chunks = splitHTMLByWords(content);
    let wordChunks = chunks.filter(chunk => !chunk.startsWith("<"));
    let numWordsToColorize = Math.floor(wordChunks.length * percentage);
    let indices = [];

    while (indices.length < numWordsToColorize) {
      let randomIndex = Math.floor(Math.random() * wordChunks.length);
      if (indices.indexOf(randomIndex) === -1) {
        indices.push(randomIndex);
        let wordChunkIndex = chunks.indexOf(wordChunks[randomIndex]);
        chunks[wordChunkIndex] = `<span class="${randomColor()}">${chunks[wordChunkIndex]}</span>`;
      }
    }
    return chunks.join(' ');
  }

  paragraphElement.innerHTML = colorizeContent(paragraphElement.innerHTML, 0.3);
}

function colorizeAllParagraphs() {
  const paragraphs = document.querySelectorAll('p');
  paragraphs.forEach(p => colorizeParagraph(p));
}

function shouldColorize(url) {
  // Regular expression patterns for paths that should be colorized
  const colorizePatterns = [
    /\/consultancy\/?$/,
    /\/classes\/?$/,
    /\/about\/?$/
  ];

  // Check if the provided URL matches one of the patterns that should be colorized
  return colorizePatterns.some(pattern => pattern.test(url));
}

// Export the function for external use
window.colorizeAllParagraphs = colorizeAllParagraphs;

document.body.addEventListener('htmx:afterSwap', function(event) {
  //const targetURL = event.detail.path; //
  const targetURL = event.detail.xhr.responseURL;
  if (shouldColorize(targetURL)) {
    window.colorizeAllParagraphs();
  }
});

document.addEventListener("DOMContentLoaded", function() {
  if (shouldColorize(window.location.pathname)) {
    window.colorizeAllParagraphs();
  }
});
