$(document).ready(function() {
   $("#likes").click(function() {
   var catid;
   // get the id of the opened category
   catid = $(this).attr("data-catid");
   // make ajax get request to this view
   $.get('/rango/like/', {category_id: catid}, function(data){
        // success function - upon returning from the view, update the new likes value
        // data here is the new number of likes - update its value and hide the button
        $('#like_count').html(data);
        $('#likes').hide();
       });
   });

   $("#suggestion").keyup(function() {
        // get all categories that start with the writen string so far
        var query;
        query = $(this).val();
        $.get('/rango/suggest/', {suggestion: query}, function(data) {
            $('#cats').html(data);
        });
   });
});

