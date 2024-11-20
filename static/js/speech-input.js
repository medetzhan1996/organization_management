if ("webkitSpeechRecognition" in window) {
  // Initialize webkitSpeechRecognition
  let speechRecognition = new webkitSpeechRecognition();

  // String for the Final Transcript
  let final_transcript = "";

  // Set the properties for the Speech Recognition object
  speechRecognition.continuous = true;
  speechRecognition.interimResults = true;
  speechRecognition.lang = 'ru-RU';

  // Callback Function for the onStart Event
  speechRecognition.onstart = () => {
    // Show the Status Element
    document.querySelector("#status").style.display = "block";
  };
  speechRecognition.onerror = () => {
    // Hide the Status Element
    document.querySelector("#status").style.display = "none";
  };
  speechRecognition.onend = () => {
    // Hide the Status Element
    document.querySelector("#status").style.display = "none";
  };

  speechRecognition.onresult = (event) => {
    // Create the interim transcript string locally because we don't want it to persist like final transcript
    let interim_transcript = " ";

    // Loop through the results from the speech recognition object.
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      // If the result item is Final, add it to Final Transcript, Else add it to Interim transcript
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }

    // Set the Final transcript and Interim transcript.
    document.querySelector("#result-audio").innerHTML = final_transcript;
    document.querySelector("#interim").innerHTML = interim_transcript;
  };

  $(document).on('click', '#start-audio', function(event) {
    $("#result-audio").attr("placeholder", "Слушаю .....")
    $(this).attr("id", "stop-audio")
    speechRecognition.start()
  })

  $(document).on('click', '#stop-audio', function(event) {
    $("#result-audio").attr("placeholder", "")
    speechRecognition.stop()
    $(this).attr("id", "start-audio")
  })

  $(document).on('click', '#save-audio', function(event) {
    var result_audio = $("#result-audio").val()
    var marker = $('#marker-audio').val()
    var element = $('#' + marker)
    var name = element.attr('name')
    $('#' + name).append(result_audio)
    var result = element.val() + result_audio
    element.val(result)
    $('#universal-modal').modal('hide')
    speechRecognition.stop()
  })

  $(document).on('click', '#clear-audio', function(){
    $('#result-audio').val("")
  })
  
} else {
  console.log("Speech Recognition Not Available");
}