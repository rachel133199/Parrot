import './App.css';
import Word from './Word'
import SpeakButton from './SpeakButton'
import PlayButton from './PlayButton'
import Phoneme from './Phoneme'
import NavBar from './NavBar'
import { useState } from 'react';
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { recordAudio, sleep } from "./record";
import { getSpeech, getScore } from './azure';


function App() {
  const [word, setWord] = useState({
    phonemes: ["P", "EH1", "R", "AH0", "T"],
    word: "parrot"
  })
  // let phm = word.phonemes
  // phm.map(phm => "gray")
  const [phmCol, setPhmCol] = useState("gray")
  const [score, setScore] = useState(0)

  function changeColor(n) {
    let color = "red"
    if (n >= 8) {
      color = "green"
    } else if (n >= 5 && n < 8) {
      color = "orange"
    }
    setPhmCol(color)
    console.log(color)
    setTimeout(function () { setPhmCol("gray") }, 2000)
  }

  function getWord() {
    // changeColor()
    fetch("http://127.0.0.1:5000/get_word")
      .then(response => response.json())
      .then(response => {
        setWord(response)
      });

    return word.word
  }

  function submitResults(score) {
    fetch("http://127.0.0.1:5000/submit_results", {
      method: "POST",
      body: score,
    }).then(response => console.log(response.json()));
  }

  let audio;

  async function record() {
    const recorder = await recordAudio();
    recorder.start();
    await sleep(3000);
    audio = await recorder.stop();
    let result = await getScore(audio, word.word);
    let s = result.NBest[0].AccuracyScore
    s = Math.round(s / 10)
    setScore(s);
    submitResults(s);
    changeColor(s);
    // setScore(0);
  }

  function playback() {
    if (audio !== undefined) {
      audio.play();
      changeColor(score);
    }
  }

  return (
    <div className="App">
      <NavBar />
      {/* <SpeakButton /> */}
      {/* <span><FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} size="10x"/></span> */}
      <Word getWord={getWord} word={word.word} />
      <Phoneme phmCol={phmCol} phm={word.phonemes} word={word.word} />
      <div>
        <h1 className="Score">Your score is {score}</h1>
      </div>
      <SpeakButton onClick={record} />
      <PlayButton onClick={playback} />
    </div>
  );
}

export default App;
