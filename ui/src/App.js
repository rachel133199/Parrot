import './App.css';
import Word from './Word'
import SpeakButton from './SpeakButton'
import PlayButton from './PlayButton'
import Phoneme from './Phoneme'
import NavBar from './NavBar'
import { useState } from 'react';
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { recordAudio, sleep } from "./record"


function App() {
  const [word, setWord] = useState({
    phonemes: ["P", "EH1", "R", "AH0", "T"],
    word: "parrot"
  })
  let phm = word.phonemes
  phm.map(phm => "gray")
  const [phmCol, setPhmCol] = useState(phm)

  function changeColor() {
    let original = phmCol.map(c => "grey")
    console.log('color change!')
    
    let count = -1
    let color = phmCol.map(c => {
      count = count + 1
      // console.log(word.phonemes[count])
      if(word.phonemes[count] != undefined) {
        var last = word.phonemes[count].slice(-1)
      }
      if (last == "2") {
        return "DarkBlue"
      } else if (last == "1") {
        return "BlueViolet"
      } else if (last == "0") {
        return "Plum"
      }
      return ("gray")
    })
    setPhmCol(color)
    // setTimeout(function () { setPhmCol(original) }, 700)
    console.log(phmCol)
    // console.log(word.phonemes)
    
  }

  function changeBackColor(){
    let original = phmCol.map(c => "grey")
    setPhmCol(original)
    console.log("back")
  }

  function getWord() {
    changeColor()
    fetch("http://127.0.0.1:5000/get_word")
      .then(response => response.json())
      .then(response => {
        // console.log(response)
        setWord(response)
        // console.log(word)
      });

    return word.word
  }

  let audio;

  async function record() {
    fetch("https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken", {
      method: 'POST',
      headers: {
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-length': '0',
        'Ocp-Apim-Subscription-Key': '7c0cb9b8617f487eb23ed60138a8d928'
      }
    })
    .then(response => console.log(response));
    // .then(response => console.log(response));

    // console.log(response)

    const recorder = await recordAudio();
    recorder.start();
    await sleep(3000);
    audio = await recorder.stop();
    // fetch("https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-CA", {
    //   method: 'POST',
    //   host: "westus.stt.speech.microsoft.com",
    //   headers: {
    //     'Authorization': "", 
    //     'Content-type': 'application/ssml+xml',
    //     'Content-Length': '199',
    //   },
    //   connection: 'Keep-Alive',
    //   body: URL()
    // })
  }

  function playback() {
    audio.play();
    console.log(audio)
  }

  return (
    <div className="App">
      <NavBar />
      {/* <SpeakButton /> */}
      {/* <span><FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} size="10x"/></span> */}
      <Word getWord={getWord} word={word.word} changeColor={changeColor} changeBackColor={changeBackColor}/>
      <Phoneme phmCol={phmCol} phm={word.phonemes} />
      <SpeakButton onClick={record}/>
      <PlayButton onClick={playback} />
    </div>
  );
}

export default App;
