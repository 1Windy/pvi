
$(function () {
   $(".save-bha-btn").click(function (event) {
       event.preventDefault();

       var id = $(this).attr('data-id');
       var round = $(this).attr('data-round');
       var status = $(this).prev('#update_status').val();

       $.ajax({
           url: '/',
           type: 'post',
           data: {
               'id': id,
               'round': round,
               'status': status
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
