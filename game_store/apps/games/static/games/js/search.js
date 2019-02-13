$(document).ready(function() {

  $.getScript('/static/js/token_verification.js', function() {

    var searchForm = $("#game-search-form");

    function postSearchForm() {
      $.ajax({
          url : "search",
          type : "POST",
          data: searchForm.serialize(),
          success : function(json) {
              $("#game-search-results").html(json.rendered);
          },
          error : function(xhr, errorMessage, error) {
            console.log(error);
          }
      });
    }

    searchForm.submit(function(e) {
      e.preventDefault();
      postSearchForm();
      return false;
    });

    $(".game-ownership-filters input:checkbox, .game-category-filters input:checkbox").change(function() {
      postSearchForm();
    });
  });
});
