var stockade = {
  build_notification: function(type) {
    var x = $('<div class="alert" data-dismiss="alert"></div>').addClass('alert-'+type);

    window.setTimeout(function() {
      x.fadeOut(1000);
    }, 5000);

    return x.fadeIn(1000);
  },

  display_error: function(msg) {
    $('.alerts').append(stockade.build_notification('danger').prepend(document.createTextNode(msg)));
  },

  display_success: function(msg) {
    $('.alerts').append(stockade.build_notification('success').prepend(document.createTextNode(msg)));
  }
};
