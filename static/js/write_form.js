$(document).on("blur","span[contenteditable=true]",function() {  
  var marker_id='#'+$(this).data('marker');
  var text = $(this).text().replace(new RegExp('↵', 'g'),'<br/>');  
  $(marker_id).val(text);
})

