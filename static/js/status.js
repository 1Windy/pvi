
$(function () {
   $(".save-bha-btn").click(function (event) {
       event.preventDefault();

       var id = $(this).attr('data-id');
       var round = $(this).attr('data-round');
       var tr = $(this).parent().parent();
       var status = tr.find("#update_status").val();
       var comment = tr.find('input[name="comment"]').val();

       $.ajax({
           url: '/',
           type: 'post',
           data: {
               'id': id,
               'round': round,
               'status': status,
               'comment': comment
           },
           success: function(data){
               if (data.code == 200) {
               } else {
                   alert(data.message);
               }
           }
       });
   })
});
