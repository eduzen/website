function colorize() {
  return {
    randomColor: function() {
      const colors = [
        'dracula-pink',
        'dracula-orange',
        'dracula-green',
        'dracula-purple',
        'dracula-yellow',
        'dracula-cyan'
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    }
  }
}
