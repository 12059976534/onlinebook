$(document).ready(function(){
    var limit=8;
    var start=0;
    
    var action ='inactivate'

    function load_post_data(limit,start){

      console.log(start,limit)
      $.ajax({
        url:'postsearch/',
        method:'GET',
        data:{
          limit:limit,
          start:start,
        },
       
        caches:false,
        
        success:function(response){
          $('#hasil').append(response);
          console.log(response)
          if(response == ""){
            $("#more-data").html("<center><button type='button' class='btn btn-info mb-2'>not found !!</button></center>");
            action = 'activate';
          }else{

            $("#more-data").html("<center><button type='button' class='btn btn-success mb-2'>loading book ...</button></center>");
            action = 'inactivate';
            setTimeout(function(){
              $("#more-data").html("<center><button type='button' class='btn btn-success mb-2'>all book</button></center>");
              }, 5000);

          }
        },

        
      })
    }

    if (action =='inactivate') {
      action='activate'
      load_post_data(limit,start);
      
    }

    $(window).scroll(function(){
      if($(window).scrollTop() + $(window).height() > $('#hasil').height() && action == 'inactivate'){
        action = 'activate';
        start=start+4;
        limit=limit+4;
        setTimeout(function(){
          load_post_data(limit,start);
          
        },1000)
      }
    })



  /////////////////////////////////////


 });


// search





