var stockade = {
  build_notification: function(type) {
    return $('<div class="alert" data-dismiss="alert"></div>').addClass('alert-'+type);
  },

  build_fading_notification: function(type) {
    var x = stockade.build_notification(type);
    window.setTimeout(function() {
      x.fadeOut(1000);
    }, 5000);

    return x.fadeIn(1000);
  },

  append_error: function(msg, node) {
    $(node).append(stockade.build_fading_notification('danger').prepend(document.createTextNode(msg)));
  },

  display_error: function(msg) {
    $('.alerts').append(stockade.build_fading_notification('danger').prepend(document.createTextNode(msg)));
  },

  display_success: function(msg) {
    $('.alerts').append(stockade.build_fading_notification('success').prepend(document.createTextNode(msg)));
  }
};
