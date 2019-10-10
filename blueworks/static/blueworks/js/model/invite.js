(function ($) {
  $('#invite').on('click', function () {
    $.ajax({
      url: 'http://127.0.0.1:1111/api.blueworks/account/invite',
      type: 'POST',
      dataType: 'JSON',
      contentType: 'application/x-www-form-urlencoded',
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem(
          'token'));
        xhr.setRequestHeader('ressource', 'utilisateur');
        xhr.setRequestHeader('b-action', 'CREATE');
      },
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem(
          'token'),
        'ressource': 'utilisateur',
        'b-action': 'CREATE'
      },
      data: {
        n: $('#nom_invite').val(),
        p: $('#email_invite').val(),
        s: 'BlueWorkS1'
      },
      error: function (xhr) {
        console.log(xhr);
      },
      async: true
    });
  });
})(jQuery);