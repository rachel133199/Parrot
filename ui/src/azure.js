
const {createReadStream} = require('fs');

let key = "7c0cb9b8617f487eb23ed60138a8d928";
let tokenEndpoint = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken";

let ttsEndpoint = "https://westus.tts.speech.microsoft.com/cognitiveservices/v1";
let sttEndpoint = "https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US";

let tokenHeaders = {
    "Content-type": "application/x-www-form-urlencoded",
    "Content-Length": 0,
    "Ocp-Apim-Subscription-Key": key
}

let ttsHeaders = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/ssml+xml',
    'X-Microsoft-OutputFormat': 'audio-16khz-64kbitrate-mono-mp3',
    'Content-Length': '225'
};

let sttHeaders = {
    'Ocp-Apim-Subscription-Key': key,
    'Authorization': 'Bearer ',
    'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
    'Pronunciation-Assessment': '',
    'Accept': 'application/json',
}

let pronunciationAssessment = {
    "GradingSystem": "HundredMark",
    "Granularity": "Phoneme",
}

async function getBearer() {
    return await fetch(tokenEndpoint, {
        method: 'POST',
        headers: tokenHeaders
    }).then(response => response.text())
    .then(data => {
        return data;
    })
}

async function getSpeech(word) {
    let t = await getBearer();
    let headers = {...ttsHeaders};
    headers.Authorization += t;
    if (t !== "") {
        return fetch(ttsEndpoint, {
            method: "POST",
            headers: headers,
            body: '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US"><voice name="en-US-AriaRUS">' + word + '</voice></speak>',
        }).then(response => {
            return response.blob();
        })
    }
}

async function getScore(audio, text) {
    let t = await getBearer();
    let p = {...pronunciationAssessment};
    p["ReferenceText"] = text;

    var pronAssessmentStr = JSON.stringify(p);
    var pronAssessmentHeader = Buffer.from(pronAssessmentStr).toString("base64");

    let headers = {...sttHeaders};
    headers["Authorization"] += t;
    headers["Pronunciation-Assessment"] = pronAssessmentHeader;
    
    if (t !== "") {
        return fetch(sttEndpoint, {
            method: "POST",
            headers: headers,
            body: audio.audioBlob,
        })
        .then(response => response.json())
        .then(response => {
            return response
        });
    }
}

export { getSpeech, getScore };