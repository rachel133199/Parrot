import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import Grid from '@material-ui/core/Grid';
import {getSpeech} from './azure';

function Phoneme(props){
    var count = -1
    let phm = props.phm.map(p => {
        count = count + 1
        p = p.toLowerCase();
        if (p[p.length-1] === '0') {
            p = p.substring(0, p.length-1);
        } else if (p[p.length-1] === '1' || p[p.length-1] === '2') {
            p = (<b>{p.substring(0, p.length-1)}</b>);
        } 
        if (count != props.phm.length-1){
            return(<span className="PhonemeWord" style={{color: props.phmCol}}>{p}{'\u00B7'}</span>);
        }
        return(<span className="PhonemeWord" style={{color: props.phmCol}}>{p}</span>);
    })

    let audio;
    
    async function pronounce(word) {
        let recording = await getSpeech(word);
        const audioUrl = URL.createObjectURL(recording);
        audio = new Audio(audioUrl);
        audio.play();
    }

    return(
        <div className="Phoneme">
        <Grid 
            container 
            direction="row"
            alignItems="center" 
            justify="center"
            spacing={0}
        >
            <Grid item sm={1} justify="flex-end"></Grid>
            <Grid item className="PhonemeWord">[ {phm} ]</Grid>
            <FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} onClick={() => {pronounce(props.word)}} size="8x" />
        </Grid>
        </div>
    )
}

export default Phoneme