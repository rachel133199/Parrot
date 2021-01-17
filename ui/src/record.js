const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    async function sendAudioFile(file) {
      const formData = new FormData();
      formData.append('audio-file', 'file');
      const response = await fetch('https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=detailed', {
        method: 'POST',
        host: "westus.stt.speech.microsoft.com",
        headers: {
          'Ocp-Apim-Subscription-Key': '7c0cb9b8617f487eb23ed60138a8d928',
          'Authorization': "eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJyZWdpb24iOiJ3ZXN0dXMiLCJzdWJzY3JpcHRpb24taWQiOiJjOGM5MmU0NmVlZTU0ZGQxODUxMzk0MzcxZjFhYzNkMyIsInByb2R1Y3QtaWQiOiJTcGVlY2hTZXJ2aWNlcy5GMCIsImNvZ25pdGl2ZS1zZXJ2aWNlcy1lbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNvZ25pdGl2ZS5taWNyb3NvZnQuY29tL2ludGVybmFsL3YxLjAvIiwiYXp1cmUtcmVzb3VyY2UtaWQiOiIvc3Vic2NyaXB0aW9ucy8zNWY3ZDczYy03Mzc0LTRjOTgtODBiOC1kZjFjNjlkNGE5MWMvcmVzb3VyY2VHcm91cHMvSGFja1RoZU5vcnRoL3Byb3ZpZGVycy9NaWNyb3NvZnQuQ29*",
          'Content-type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
          'Content-Length': '199',
          'Transfer-encoding': 'chunked'
        },
        connection: 'Keep-Alive',
        body: file.audioUrl
      });
      console.log(file)
      return response;
    }

    const start = () => mediaRecorder.start();

    const stop = () =>
      new Promise(resolve => {
        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks);
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          const play = () => audio.play();
          console.log(audio)
          // const audioFile = new Blob(audioChunks, {
          //   'type' : 'audio/wav; codecs=MS_PCM'
          // })
          // console.log(audioFile)
          const response = sendAudioFile(audioBlob)
          console.log(response)
          resolve({ audioBlob, audioUrl, play });
        });

        mediaRecorder.stop();
      });

    resolve({ start, stop });
  });

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

export { recordAudio, sleep };