import React from 'react';
import { faCrow } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import logo from './parrot.png';

function NavBar() {
    return (
        <Navbar bg="outline-primary">
            <a href="#">
                <img src={logo} width="50px" height="50px"></img>
                <Navbar.Brand href="#">
                    <h3 className="ParrotHome">Parrot</h3>
                </Navbar.Brand>
            </a>
        </Navbar>
    )
}

export default NavBar