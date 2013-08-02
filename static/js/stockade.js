var stockade = {
  build_notification: function(type) {
    return $('<div class="alert fade in" data-dismiss="alert"> <a class="close" href="#">&times;</a></div>').addClass('alert-'+type);
  },

  display_error: function(msg) {
    $('.alerts').append(stockade.build_notification('danger').prepend(document.createTextNode(msg)));
  },

  display_success: function(msg) {
    $('.alerts').append(stockade.build_notification('success').prepend(document.createTextNode(msg)));
  }
};
