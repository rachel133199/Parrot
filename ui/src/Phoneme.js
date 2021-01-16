import React from 'react'

function Phoneme(props){
    let fullPhm = ""
    let phonemes = props.phm.map(phm => {
        fullPhm = fullPhm + " " + phm
        if(fullPhm.slice(-1) == "1") {

        }
    })
    return(
        <div className="Phoneme">
            <h1 className="PhonemeWord" style={props.phmCol}>[ {fullPhm} ]</h1>
        </div>
    )
}

export default Phoneme