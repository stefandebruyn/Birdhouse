  // navigator.mediaDevices.getUserMedia({ audio: true })
  // .then(stream => {
  //   const mediaRecorder = new MediaRecorder(stream);
  //   mediaRecorder.start();
  //
  //   const audioChunks = [];
  //   mediaRecorder.addEventListener("dataavailable", event => {
  //     audioChunks.push(event.data);
  //   });
  //
  //   mediaRecorder.addEventListener("stop", () => {
  //     const audioBlob = new Blob(audioChunks);
  //     callAJAX(audioBlob);
  //   });
  //
  //   setTimeout(() => {
  //     mediaRecorder.stop();
  //   }, 3000);
  // });
function test() {
  console.log('test');
  navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];
    mediaRecorder.addEventListener('dataavailable', event => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener('stop', () => {
      const audioBlob = new Blob(audioChunks);
      console.log(audioChunks);
      console.log(audioBlob);
      callAJAX(audioBlob);
    });

    setTimeout(() => {
      mediaRecorder.stop();
    }, 3000);
  });
}

function callAJAX(audioBlob) {
  console.log('init AJAX call');
  var fileType = 'audio';
  var fileName = 'output.mp3';
  var formData = new FormData();
  formData.append(fileType, audioBlob, fileName);
  console.log('audio blob length: ' + audioBlob.size);
  $.ajax({
    type: 'POST',
    url: '/upload/',
    data: formData,
    processData: false,  // prevent jQuery from converting the data
    contentType: false,  // prevent jQuery from overriding content type
    success: function(response) {
      console.log('success');
      // console.log(formData === null);
    },
    error: function (error) {
      console.log('there was an error');
    }
   });
 }
