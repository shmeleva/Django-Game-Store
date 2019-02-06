$(document).ready(function() {

  // https://docs.djangoproject.com/en/2.1/ref/csrf/#setting-the-token-on-the-ajax-request

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

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
