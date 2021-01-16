import React from 'react'

function Phoneme(props){
    var count = -1
    var size = props.phm.map(p => 70)
    let phm = props.phm.map(p => {
        count = count + 1
        if(props.phmCol[count] == "DarkBlue") {
            size[count] = 110
            p = p.substring(0, p.length - 1)
        } else if(props.phmCol[count] == "BlueViolet") {
            size[count] = 95
            p = p.substring(0, p.length - 1)
        } else if(props.phmCol[count] == "Plum") {
            size[count] = 70
            p = p.substring(0, p.length - 1)
        }
        return(<span className="PhonemeWord" style={{color: props.phmCol[count], fontSize: size[count]}}>{p} </span>)
    })
    return(
        <div className="Phoneme">
            <div className="PhonemeWord">[ {phm} ]</div>
        </div>
    )
}

export default Phoneme