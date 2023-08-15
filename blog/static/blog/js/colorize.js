function colorize() {
  return {
    randomColor: function() {
      const colors = [
        'text-pink-400',
        'text-orange-400',
        'text-green-500',
        'text-purple-500',
        'text-yellow-400',
        'text-blue-400'
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    }
  }
}
