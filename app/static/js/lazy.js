

       
$(document).ready(function(){
    
    var limit=8;
    var start=1;
    
  var action ='inactivate'
    function load_post_data(limit,start){
     
      console.log(start,limit)
      // const judul= document.getElementById("search").value
      // console.log("ddddddddddddddddddddddddddddddddddddddddddddddddddd",judul)
      $.ajax({
        url:'fetch/',
        method:'GET',
        data:{
          limit:limit,
          start:start,
          
        },
        caches:false,

        success:function(response){
          l=limit
          s=start
        if (response == ""){
          console.log("respose:",response)
        }
          
          $('#hasil').append(response);
          console.log(response)
          if(response == ""){
            $("#more-data").html("<button type='button' class='btn btn-info mb-2'>not found !!</button>");
            action = 'activate';
          }else{

            $("#more-data").html("<div class='mb-2 text-primary font-weight-bold font-italic' style='margin-left:30%'>loading book....</div>");
            action = 'inactivate';
            setTimeout(function(){
              $("#more-data").html("<button type='button' class='mb-2 btn btn-success' style='margin-left:30%'>All book</button>");
              }, 5000);

          }
        }
      })
    }

    if (action =='inactivate') {
      action='activate'
      load_post_data(limit,start);
      
    }

    $(window).scroll(function(){
      if($(window).scrollTop() + $(window).height() > $('#hasil').height() && action == 'inactivate'){
        action = 'activate';
        start=start+7;      
        limit=limit+7;
        setTimeout(function(){
          load_post_data(limit,start);
          
        },1000)
      }
    })



  


 });


// search









