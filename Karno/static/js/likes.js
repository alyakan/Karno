
$(document).ready(function(){
	$('.like-btn').click(function(){
	    var fileid;
	    fileid = $(this).attr("data-fileid");
	    $.get('/main/like/file/', {file_id: fileid}, function(data){
	    	var like_count = '#like_count' + fileid
	        $(like_count).html(data);
	        var like_success = '#like-success' + fileid
	        $(like_success).toggle()
	        var unlike = '#unlike' + fileid
	        $(unlike).show();
	        var like = '#like' + fileid
	        $(like).hide();
	    });
	});
	$('.unlike-btn').click(function(){
	    var fileid;
	    fileid = $(this).attr("data-fileid");
	    $.get('/main/unlike/file/', {file_id: fileid}, function(data){
	    	var like_count = '#like_count' + fileid
	        $(like_count).html(data);
	        var unlike = '#unlike' + fileid
	        $(unlike).hide();
	        var like_success = '#like-success' + fileid
	        $(like_success).toggle()
	        var like = '#like' + fileid
	        $(like).show();
	    });
	});
});
