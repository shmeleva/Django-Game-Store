
console.log(data.id);
console.log(data.url);

window.addEventListener('message', function(evt) {
  if(evt.data.messageType === 'SCORE') {
    // Contains attribute 'score'
    // TODO save received score
    $.getScript('/static/js/token_verification.js', function() {
      $.ajax({
        url: data.url,
        data: { 'score': evt.data.score, 'id': data.id },
        type: 'POST'
      });
    });
  } else if(evt.data.messageType === 'SAVE'){
    // Contains attribute 'gameState'
    // Should save received game state
  } else if(evt.data.messageType === 'LOAD_REQUEST'){
    // Should load a game state if such exists and send it back to the game
    // Respond with either LOAD or ERROR (comments below)

    /*

    for loading previous game state:
    var game_frame = document.getElementById('game_frame');
    var msg = {
      'messageType': 'LOAD',
      'gameState': <here saved game state in JSON format for example>,
    };
    game_frame.contentWindow.postMessage(msg, '*');


    if something goes wrong when trying to recover previous game state in response to received LOAD_REQUEST:
    var game_frame = document.getElementById('game_frame');
    var msg = {
      'messageType': 'ERROR',
      'info': <here contextual information to the user on what went wrong>,
    };
    game_frame.contentWindow.postMessage(msg, '*');

    */

  } else if(evt.data.messageType === 'SETTING'){
    // Contains attribute 'options'
    // 'options' contains game specific configurations for adjusting the layout if needed
  }
});
