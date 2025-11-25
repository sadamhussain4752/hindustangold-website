$(document).ready(function() {
    var some = $('#cities_json').val();
    var obj = $.parseJSON(some);
    
   $('#state_id').on('change', function() {
        var selected_state = $(this).val();
        if (obj[selected_state])  {
          $('#city_id').empty();
          $('#city_id').append('<option value="">Select City</option>');
          for(var i = 0; i < obj[selected_state].length; i++) {
            $('#city_id').append('<option value="' + obj[selected_state][i].id + '">' + obj[selected_state][i].name + '</option>');
          }
        }
        else{
          $('#city_id').empty();
          $('#city_id').append('<option value="">Select City</option>');
        }
        
   });
});