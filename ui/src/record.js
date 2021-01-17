const recordAudio = () =>
new Promise(async resolve => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream);
  const audioChunks = [];

  mediaRecorder.addEventListener("dataavailable", event => {
    audioChunks.push(event.data);
  });

  const start = () => mediaRecorder.start();

  const stop = () =>
    new Promise(resolve => {
      mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks, {type: 'audio/ogg; codecs=opus'});
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        const play = () => audio.play();
        resolve({ audioBlob, audioUrl, play });
      });

      mediaRecorder.stop();
    });

  resolve({ start, stop });
});

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

export {recordAudio, sleep};