var sdk = require("microsoft-cognitiveservices-speech-sdk");
var readline = require("readline");

let subscriptionKey = "7c0cb9b8617f487eb23ed60138a8d928";
let serviceRegion = "westus";  
let language = "en-US";
let filename = "Audio.wav"


export async function getWord() {
    const response = await fetch('http://127.0.0.1:8001/get_word');

    response.json().then(data => {
        return data.word;
    })
}

export async function submitResults() {
    const response = await fetch('http://127.0.0.1:8001/submit_results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    response.json().then(data => {
        return data;
    })
}

export function assessPronunciation() {
    let pronunciationAssessmentConfig = new sdk.PronunciationAssessmentConfig("Hello",
    sdk.PronunciationAssessmentGradingSystem.HundredMark,
    sdk.PronunciationAssessmentGranularity.Word, true);

    let speechRecognizer = sdk.SpeechRecognizer.FromConfig(sdk.speechConfig, sdk.audioConfig);
    // apply the pronunciation assessment configuration to the speech recognizer
    pronunciationAssessmentConfig.applyTo(speechRecognizer);

    speechRecognizer.recognizeOnceAsync((result) => {
        let pronunciationAssessmentResult = sdk.PronunciationAssessmentResult.fromResult(result);
        let pronunciationScore = sdk.pronResult.pronunciationScore;
        let wordLevelResult = sdk.pronResult.detailResult.Words;
        console.log(pronunciationAssessmentResult);
        console.log(pronunciationScore);
        console.log(wordLevelResult);
    },
    {});
}


export function textToSpeech() {
    let audioConfig = sdk.AudioConfig.fromAudioFileOutput(filename);
    let speechConfig = sdk.SpeechConfig.fromSubscription(subscriptionKey, serviceRegion);
    // create the speech synthesizer.
    var synthesizer = new sdk.SpeechSynthesizer(speechConfig, audioConfig);

    var rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question("Type some text that you want to speak...\n> ", function (text) {
      rl.close();
      // start the synthesizer and wait for a result.
      synthesizer.speakTextAsync(text,
          function (result) {
        if (result.reason === sdk.ResultReason.SynthesizingAudioCompleted) {
          console.log("synthesis finished.");
        } else {
          console.error("Speech synthesis canceled, " + result.errorDetails +
              "\nDid you update the subscription info?");
        }
        synthesizer.close();
        synthesizer = undefined;
      },
          function (err) {
        console.trace("err - " + err);
        synthesizer.close();
        synthesizer = undefined;
      });
      console.log("Now synthesizing to: " + filename);
    });

}

