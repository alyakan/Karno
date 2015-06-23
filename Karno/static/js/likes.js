$(document).ready(function(){
	$('.like-btn').click(function(){
	    var fileid;
	    fileid = $(this).attr("data-fileid");
	    $.get('/main/like/file/', {file_id: fileid}, function(data){
	    	var like_count = '#like_count' + fileid
	    	data1 = " <strong>" + data + "</strong>"
	        $(like_count).html(data1);
	        var like_success = '#like-success' + fileid
	        $(like_success).toggle()
	        var unlike = '#unlike' + fileid
	        $(unlike).removeClass("hidden");
	        var like = '#like' + fileid
	        $(like).addClass("hidden");
	    });
	});
	$('.unlike-btn').click(function(){
	    var fileid;
	    fileid = $(this).attr("data-fileid");
	    $.get('/main/unlike/file/', {file_id: fileid}, function(data){
	    	var like_count = '#like_count' + fileid
	    	data1 = " <strong>" + data + "</strong>"
	        $(like_count).html(data1);
	        var unlike = '#unlike' + fileid
	        $(unlike).addClass("hidden");
	        var like_success = '#like-success' + fileid
	        $(like_success).toggle()
	        var like = '#like' + fileid
	        $(like).removeClass("hidden");
	    });
	});
});

