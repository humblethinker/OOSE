function searchToggle(obj, evt) {
  var container = $(obj).closest('.search-wrapper');
  if (!container.hasClass('active')) {
    container.addClass('active');
    evt.preventDefault();
  } else if (container.hasClass('active') && $(obj).closest('.input-holder').length == 0) {
	 $(".card").hide();
	$("#lolz").hide();
    container.removeClass('active');
    // clear input
    container.find('.search-input').val('');
  }
}
$(document).ready(function () {
	var doc = localStorage.getItem('doctor');
	var nur = localStorage.getItem('nurse');
	var sta = localStorage.getItem('staff');
	var adm = localStorage.getItem('admin');
	if(!(sta==1||adm==1))
	{
		window.location.replace("http://127.0.0.1:5000/login/page");
		alert("You are not Logged In!");
	}
	$(".card").hide();
	$("#lolz").hide();
$('#search').click(function () {

  
  id=$('#pat').val();
  if(!id)
  {
    return;
  }
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "patient/"+id,
  "method": "GET",
  "headers": {
    "cache-control": "no-cache"
  }
}

$.ajax(settings).done(function (response) {
  
  console.log(response);
  if(response=="Invalid ID")
  {
	  alert("Invalid ID");
  }
  else
  {
  $(".card").html("<table> <tr><td>Patient First name </td><td>" + response[0].pat_first_name + "</td></tr> <tr><td>Patient last name </td>  <td>"
                        + response[0].pat_last_name + "</td></tr> <tr><td> Age </td><td>" + response[0].age + "</td></tr><tr><td> Sex </td><td>" 
                        + response[0].sex + "</td></tr></table>");			
  $(".card").show();
  $("#lolz").show();
  $('#lolz').click(function() {
    window.location.href = 'invoice/' + id;
    return false;
});
  }
});
}); 
})