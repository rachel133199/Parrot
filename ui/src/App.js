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
  })

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
    // setTimeout(function(){ setScore(0) }, 1500)
    // setTimeout(function () { setPhmCol("gray") }, 1500)

  };

  useEffect(() => {
    pronounce(word.word);
    setScore(0);
    setPhmCol("gray");
  }, [word]);

  async function pronounce(word) {
    let recording = await getSpeech(word);
    const url = URL.createObjectURL(recording);
    let pronunciation = new Audio(url);
    pronunciation.play();
  }

  function getWord() {
    fetch("http://127.0.0.1:8001/get_word?user_id=" + user_id)
      .then(response => response.json())
      .then(response => {
        setWord(response);
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
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        'Access-Control-Allow-Origin': '*',
      }
    });
  }

  const [audio, setAudio] = useState(null);
  let recorder;

  async function record() {
    recorder = await recordAudio();
    recorder.start();
  }

  async function stopRecording() {
    let a = await recorder.stop();
    setAudio(a);
    let score = await getScore(a, word.word);
    let s = 0
    if(score.NBest != undefined) {s = score.NBest[0].AccuracyScore}
    s = Math.round(s / 10)
    setScore(s);
    submitResults(s);
    changeColor(s);
    // setScore(0);
    // TODO: set the color of the phonemes
    submitResults(score);
  }

  function playback() {
    if (audio) {
      audio.play();
    }
  }


  return (
    <div className="App">
      <NavBar />
      <Word getWord={getWord} word={word.word} />
      <Phoneme phmCol={phmCol} phm={word.phonemes} word={word.word}/>
      <div>
        <h1 className="Score">Your score is <span style={{color: phmCol}}>{score}</span></h1>
      </div>
      <SpeakButton start={record} stop={stopRecording} />
      <PlayButton onClick={playback} />
    </div>
  );
}

export default App;
