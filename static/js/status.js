
$(function () {
   $(".save-bha-btn").click(function (event) {
       event.preventDefault();

       var id = $(this).attr('data-id');
       var status = $(this).prev('#update_status').val();

       $.ajax({
           url: '/',
           type: 'post',
           data: {
               'id': id,
               'status': status
           },
           success: function(data){
               if(data.code==200){
                   window.location.href = '/';
               }else {
                   alert(data.message);
               }
           }
       });
   })
});
