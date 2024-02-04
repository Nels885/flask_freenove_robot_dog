$('#detail-list a').on('click', function (e) {
  e.preventDefault();
  $(this).tab('show')
});


// Hide message
$(".fader-auto").fadeTo(10000, 500).slideUp(500, function () {
  $(".fader-auto").slideUp(500);
});


// System modal
$('#msgModal').on('show.bs.modal', function(event) {
  const url = $(event.relatedTarget).data('url');
  $.ajax({
      url: url,
      type: 'GET',
      success: function (response) {
          console.log(response);
          $(".modal-body").html(response['html']);
          if (response['status'] != 'busy') {
            setTimeout("location.reload();", 50000);
          } else {
            setTimeout("location.reload();", 5000);
          }
      }
  });
});


function addMessage(text, extra_tags = "success", fixed = false) {
  var message = $(`
          <div style="border-radius:0;" class="alert alert-icon alert-${extra_tags} alert-dismissible fade show mb-0" role="alert">\n
                  ${text}\n
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n
                  <span aria-hidden="true">&times;</span>\n
              </button>\n
          </div>`).hide();
  $("#messages").append(message);
  message.fadeIn(500);

  if (!fixed && extra_tags === "success") {
      message.fadeTo(10000, 500).slideUp(500, function () {
          message.slideUp(500);
          message.remove();
      });
  }
}


function textCopy(text) {
  const elem = document.createElement('textarea');
  elem.value = text;
  document.body.appendChild(elem);
  elem.select();
  document.execCommand("copy");
  document.body.removeChild(elem);
  addMessage(elem.value + " copié !");
  // alert("Copied the text: " + elem.value);
}


function excelCopy(response) {
  const data = JSON.parse(response);
  const elem = document.createElement('textarea');
  console.log(data);
  let text = data['matRef'] + "\t" + data['compRef'] + "\t" + data['calFile'] + "\t" + data['calEdit'] + "\t" + data['diagMsg'] + "\t" + data['calDate'] + "\t" + data['spNumber'];
  elem.value = text;
  document.body.appendChild(elem);
  elem.select();
  document.execCommand("copy");
  document.body.removeChild(elem);
  addMessage(text + " copié !");
  // alert("Copied the text: " + elem.value);
}