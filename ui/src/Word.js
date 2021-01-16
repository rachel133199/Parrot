import React from 'react'
import Jumbotron from 'react-bootstrap/Jumbotron'
import Container from 'react-bootstrap/Container'

function Word(props){
    return(
        // <Jumbotron className="Word" fluid>
        //     <Container>
        //         <h1>{props.word}</h1>
        //     </Container>
        // </Jumbotron>
        <div className="Word">
            <a href="#">Giant</a>
        </div>
    )
}

export default Word