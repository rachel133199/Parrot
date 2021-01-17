import './App.css';
import Word from './Word'
import SpeakButton from './SpeakButton'
import PlayButton from './PlayButton'
import Phoneme from './Phoneme'
import NavBar from './NavBar'
import { useEffect, useState } from 'react';
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { recordAudio, sleep } from "./record";
import { getSpeech, getScore } from './azure';


function App() {
  const user_id = '0';
  const [word, setWord] = useState({
    phonemes: ["P", "EH1", "R", "AH0", "T"],
    word: "parrot"
  });
  let phm = word.phonemes
  phm.map(phm => "gray")
  const [phmCol, setPhmCol] = useState(phm)

  useEffect(() => {
    pronounce(word.word);
  }, [word]);

  function changeColor() {
    let original = phmCol.map(c => "grey")
    
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

  async function pronounce(word) {
      let recording = await getSpeech(word);
      const audioUrl = URL.createObjectURL(recording);
      let pronunciation = new Audio(audioUrl);
      pronunciation.play();
  }

  function getWord() {
    changeColor()
    fetch("http://127.0.0.1:8001/get_word?" + user_id)
      .then(response => response.json())
      .then(response => {
        // console.log(response)
        setWord(response);
        // console.log(word)
      });

    return word.word
  }

  function submitResults(score) {
    let scores = []

    if (score.NBest) {
      scores = score.NBest[0].Words.map(w => {
        return {
          word: w.Word,
          score: w.AccuracyScore
        }
      })
    } 

    let data = {
      'user_id': user_id,
      'scores': scores
    }

    fetch("http://127.0.0.1:8001/submit_results", {
      method:"POST",
      body: data,
      headers: {
        'Access-Control-Allow-Origin': '*',
      }
    });
  }

  let audio;
  let recorder;

  async function record() {
    recorder = await recordAudio();
    recorder.start();
  }

  async function stopRecording() {
    audio = await recorder.stop();
    let score = await getScore(audio, word.word);
    // TODO: set the color of the phonemes
    submitResults(score);
  }

  function playback() {
    audio.play();
  }

  return (
    <div className="App">
      <NavBar />
      {/* <SpeakButton /> */}
      {/* <span><FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} size="10x"/></span> */}
      <Word getWord={getWord} word={word.word} changeColor={changeColor} changeBackColor={changeBackColor}/>
      <Phoneme phmCol={phmCol} phm={word.phonemes} word={word.word} />
      <SpeakButton start={record} stop={stopRecording}/>
      <PlayButton onClick={playback} />
    </div>
  );
}

export default App;
