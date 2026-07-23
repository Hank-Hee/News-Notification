(function () {
  'use strict';

  function processScoreBadges() {
    var scoreRe = /⭐️\s*(\d+(?:\.\d+)?)\/10/;
    document.querySelectorAll('.main-content h2, .main-content h3, .main-content li').forEach(function (el) {
      var match = el.innerHTML.match(scoreRe);
      if (!match) return;
      var score = parseFloat(match[1]);
      var tier = score >= 9 ? 'high' : score >= 7 ? 'good' : score >= 5 ? 'mid' : 'low';
      el.innerHTML = el.innerHTML.replace(
        scoreRe,
        '<span class="score-badge" data-tier="' + tier + '">' + match[1] + '/10</span>'
      );
    });
  }

  function markSourceLines() {
    document.querySelectorAll('.main-content p').forEach(function (paragraph) {
      if (/^(rss|reddit|github|hackernews|ossinsight|gdelt|google_news)\s*·/i.test(paragraph.textContent.trim())) {
        paragraph.classList.add('source-line');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    processScoreBadges();
    markSourceLines();
  });
})();
