let ethanIsRecording = false;
let hasSentAJAX = false;
var mediaDev = navigator.mediaDevices;
var mediaRecorder = null;

function toggleRecording() {
    ethanIsRecording = !ethanIsRecording;
    if(ethanIsRecording) {
      document.getElementById(`micimage`).src = "/static/images/microphone-recording.png";
      mediaDev.getUserMedia({ audio: true })
      .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        console.log("finna start");
        mediaRecorder.start();

        const audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
          console.log("pivot");
        });

        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks);
          console.log(audioChunks);
          console.log(audioBlob);
          console.log("call ajax");
          callAJAX(audioBlob);
        });
      });
    } else {
      document.getElementById(`micimage`).src = "/static/images/bird-flying.gif";
      document.getElementById(`micimage`).onclick = null;
      document.getElementById(`micimage`).style.cursor = `default`;
      mediaRecorder.stop();
      // remove mic

      // set bird animation
    }
}

function callAJAX(audioBlob) {
  console.log("init AJAX call");
  var fileType = 'audio';
  var fileName = 'output.mp3';
  var formData = new FormData();
  console.log("blob size: " + audioBlob.size);
  formData.append(fileType, audioBlob, fileName);
  $.ajax({
      type: 'POST',
      //url: 'https://talk2home-hacktx.appspot.com/upload/',
      url: '/upload/',
      data: formData,
      processData: false,  // prevent jQuery from converting the data
      contentType: false,  // prevent jQuery from overriding content type
      success: function(response) {
          console.log("success");
          document.write(response);
          document.close();
      },
      error: function (error) {
          console.log("there was an error");
        }
  });
  hasSentAJAX = true;
}

function setImageVisible(id, visible) {
    var img = document.getElementById(id);
    img.style.visibility = (visible ? 'visible' : 'hidden');
}
