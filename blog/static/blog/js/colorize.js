function colorize() {
  return {
      randomColor: function() {
          const colors = [
              'text-pink-400',
              'text-orange-400',
              'text-green-400',
              'text-purple-500',
              'text-yellow-400',
              'text-blue-400'
          ];
          return colors[Math.floor(Math.random() * colors.length)];
      }
  }
}

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

document.addEventListener("DOMContentLoaded", function() {
  const paragraphs = document.querySelectorAll('p');
  paragraphs.forEach(p => colorizeParagraph(p));
});
