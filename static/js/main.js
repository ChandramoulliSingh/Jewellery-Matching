$(document).ready(function () {
	$('#discount').on('change', function() {
    alert($('#Category').val());
  });
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
	$('#myimg').clear;

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
		$('#myimg').html('');
		$('#myimg').hide();
        readURL(this);
    });
	function getSelectValue(){
		var SelectedValue = document.getElementById("Category").value;
		console.log(SelectedValue)
	}
    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
		var SelectedValue = document.getElementById("Category").value;
		form_data.append('value',JSON.stringify(SelectedValue))
		console.log(SelectedValue)

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            //data: {form_data:form_data,selected:SelectedValue},
			data:form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {console.log(data);
			$('.loader').hide();
			$('#myimg').fadeIn(650);
			$('#myimg').append('<h4>Matches</h4>')
			for (var i=0; i<10; i++){
				//$('#myimg').text(data)
				//$('#result').text('Score'+ data.score[i])
				$('#myimg').append('<div style="width:image width px; font-size:80%; text-align:center;"><img class="img-responsive"  src="'+data.filenames[i]+'" width="200" height="200" style="padding-bottom:0.5em;" /><h5>Similarity Score:  '+data.score[i]+'</h5>')
				//$('#myimg').html('<img class="img-responsive"  src="'+data[i]+'" width="256" height="256"/>' );
			}
            },
        });
    });

});
