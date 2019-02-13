window.addEventListener('message', function(evt) {
  if(evt.data.messageType === 'SCORE') {
    // Contains attribute 'score'
    $.getScript('/static/js/token_verification.js', function() {
      $.ajax({
        url: '/game/update_score',
        data: {
          'id': data.id,
          'score': evt.data.score
        },
        type: 'POST'
      });
    });
  } else if(evt.data.messageType === 'SAVE'){
    // Contains attribute 'gameState'
    $.getScript('/static/js/token_verification.js', function() {
      $.ajax({
        url: '/game/save_game',
        data: {
          'id': data.id,
          'game_state': JSON.stringify(evt.data.gameState)
        },
        type: 'POST'
      });
    });
  } else if(evt.data.messageType === 'LOAD_REQUEST'){

    $.getScript('/static/js/token_verification.js', function() {
      $.post(
        '/game/load_game',
        {
          'id': data.id,
          'game_state': JSON.stringify(evt.data.gameState)
        }, function(response) {
          var game_frame = document.getElementById('game_frame');
          var res = JSON.parse(response);
          if(res['head']==='LOAD') {
            var msg = {
              'messageType': res['head'],
              'gameState': JSON.parse(res['body']),
            };
            game_frame.contentWindow.postMessage(msg, '*');
          } else {
            var msg = {
              'messageType': res['head'],
              'info': res['body'],
            };
            game_frame.contentWindow.postMessage(msg, '*');
          }
        });
    });

  } else if(evt.data.messageType === 'SETTING'){
    // Contains attribute 'options' which contains game specific configurations for adjusting the layout if needed
    $(document).ready(function() {
      $('iframe').css(evt.data.options);
    });
  }
});
