import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import Grid from '@material-ui/core/Grid';

function Phoneme(props){
    var count = -1
    let phm = props.phm.map(p => {
        count = count + 1
        // if(props.phmCol[count] == "DarkBlue") {
        //     p = p.substring(0, p.length - 1)
        // } else if(props.phmCol[count] == "BlueViolet") {
        //     p = p.substring(0, p.length - 1)
        // } else if(props.phmCol[count] == "Plum") {
        //     p = p.substring(0, p.length - 1)
        // }
        p = p.toLowerCase();
        if (p[p.length-1] === '0') {
            p = p.substring(0, p.length-1);
        } else if (p[p.length-1] === '1' || p[p.length-1] === '2') {
            p = (<b>{p.substring(0, p.length-1)}</b>);
        } 
        if (count != props.phm.length-1){
            return(<span className="PhonemeWord">{p}{'\u00B7'}</span>);
        }
        return(<span className="PhonemeWord">{p}</span>);
    })
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
            <FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} onClick={props.onIconClick} size="8x" />
        </Grid>
        </div>
    )
}

export default Phoneme