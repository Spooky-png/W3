var my_time;
$(document).ready(function() {
  pageScroll();
  $("#contain").mouseover(function() {
    clearTimeout(my_time);
  }).mouseout(function() {
    pageScroll();
  });
});

function pageScroll() {  
	var leaderboard = document.getElementById("contain");
  leaderboard.scrollTop = leaderboard.scrollTop + 1;  
  if (leaderboard.scrollTop == (leaderboard.scrollHeight - 100)) {
    leaderboard.scrollTop = 0;
  }
  my_time = setTimeout('pageScroll()', 100);
}