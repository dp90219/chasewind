// $(document).ready(function() {
// 	
// 
// 	$('#likes').click(function(){
// 	        var catid;
// 	        catid = $(this).attr("data-catid");
// 	         $.get('/rango/like_category/', {category_id: catid}, function(data){
// 	                   $('#like_count').html(data);
// 	                   $('#likes').hide();
// 	               });
// 	    });
// 
// 
//     	$('#suggestion').keyup(function(){
// 		var query;
// 		query = $(this).val();
// 		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
//                  $('#cats').html(data);
// 		});
// 	});
// 
//     
// 	$('.post-add').click(function(){
//         var url = $(this).attr("data-url");
//         var title = $(this).attr("data-title");
//         var me = $(this)
// 	    $.get('/blog/auto_add_page/', {url: url, title: title}, function(data){
// 	                   $('#posts').html(data);
// 	                   me.hide();
// 	               });
// 	    });
// 
// });
//
$(document).ready(function(){
  $('.post-add').click(function(){
    var me = $(this);
    var url = $(this).attr("data-url");
    var title = $(this).attr("data-title");
    var summary = $(this).attr("data-summary")
    $.get('/blog/auto_add_page/', {url: url, title: title, summary: summary}, function(data){
      me.hide();
      $('#posts').html(data);
    });
  });

  $('#search-button').click(function() {
    var query = $('#search-input').val()
    $.get('/blog/search_ajax/', {query: query}, function(data){
      $('#search-content').html(data)
    });

  })



});
