(function ($) {
  $('#invite').on('click', function () {
    $.ajax({
      url: 'http://127.0.0.1:1111/invite.new',
      type: 'POST',
      dataType: 'JSON',
      contentType: 'application/x-www-form-urlencoded',
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader('Authorization', 'Bearer ' + sessionStorage.getItem(
          'tk'));
        xhr.setRequestHeader('ressource', 'utilisateur');
        xhr.setRequestHeader('b-action', 'CREATE');
      },
      headers: {
        'Authorization': 'Bearer ' + sessionStorage.getItem(
          'tk'),
        'ressource': 'utilisateur',
        'b-action': 'CREATE'
      },
      data: {
        n: $('#nom_invite').val(),
        p: $('#email_invite').val(),
        s: 'BlueWorkS1'
      },
      success: function (data) {
        $('#myModalInviter').modal('hide');
        alert(data.msg);
      },
      async: true
    });
  });
})(jQuery);