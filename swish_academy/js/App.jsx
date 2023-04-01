import React from "react";

import axios from "axios";
import Home from "./Home";
import Contact from "./Contact";
import Login from "./Login";

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentPage: "home"
        }
    }

    componentDidMount() {

    }

    updateCurrentPage = (page) => {
        this.setState({
            currentPage: page
        });
    }

    render() {
        const { currentPage } = this.state;

        return (
            <div>
                <header>
                    <nav className="navBar" id="nav">
                        <input type="checkbox" id="check" />
                        <label htmlFor="check" className="checkbtn">
                            <i className="fas fa-bars">&#8205;</i>
                        </label>
                        <img src="static/imgs/Swish Academy Logo_White.png" />
                        <ul>
                            <li><a className={currentPage === "home" ? 'active' : ''} onClick={() => {this.updateCurrentPage("home")}}>Home</a></li>
                            <li><a className={currentPage === "contact" ? 'active' : ''} onClick={() => {this.updateCurrentPage("contact")}}>Contact</a></li>
                            <li><a className={currentPage === "login" ? 'active' : ''} onClick={() => {this.updateCurrentPage("login")}}>Login</a></li>
                        </ul>
                    </nav>
                </header>

                {currentPage === "home" && <Home />}
                {currentPage === "contact" && <Contact />}
                {currentPage === "login" && <Login />}
            </div>
        );
    }
}