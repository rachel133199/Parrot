import React from 'react'

function Phoneme(props){
    var count = -1
    var size = props.phm.map(p => 70)
    let phm = props.phm.map(p => {
        count = count + 1
        if(props.phmCol[count] == "DarkBlue") {
            size[count] = 110
        } else if(props.phmCol[count] == "BlueViolet") {
            size[count] = 95
        } else if(props.phmCol[count] == "Plum") {
            size[count] = 70
        }
        return(<span className="PhonemeWord" style={{color: props.phmCol[count], fontSize: size[count]}}>{p} </span>)
    })
    return(
        <div className="Phoneme">
            {/* <span className="PhonemeWord" style={props.phmCol}>[ {fullPhm} ]</span> */}
            {phm}
            {/* <span className="Phoneme" style={{color: props.phmCol[0]}}>{props.phm[0]}</span> */}
            {/* <span className="Phoneme" style={props.phmCol[2]}>{props.phm[0]}</span> */}
            {/* <span className="Phoneme" styles={props.phmCol[2]}>{props.phm[0]}</span> */}
        </div>
    )
}

export default Phoneme