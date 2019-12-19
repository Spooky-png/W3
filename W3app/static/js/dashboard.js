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
  $('p:nth-of-type(1)').html('scrollTop : '+ leaderboard.scrollTop);
  $('p:nth-of-type(2)').html('scrollHeight : ' + leaderboard.scrollHeight);
  if (leaderboard.scrollTop == (leaderboard.scrollHeight - 100)) {
    leaderboard.scrollTop = 0;
  }
  my_time = setTimeout('pageScroll()', 25);
}