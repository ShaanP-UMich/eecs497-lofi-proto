import React from "react";

import axios from "axios";
import Home from "./Home";
import Contact from "./Contact";
import Login from "./Login";
import SignUp from "./SignUp";
import Modules from "./Modules";
import Modules_rulesofgame from "./Modules_rulesofgame";

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentPage: "home",
            loggedInUser: null
        }
    }

    componentDidMount() {
        this.getUserLoggedIn();
    }

    updateCurrentPage = (page) => {
        this.setState({
            currentPage: page
        });
    }

    getUserLoggedIn = () => {
        axios({
            method: 'get',
            url: '/isLoggedIn/',
        }).then(response => {
            // console.log(response);
            this.setState({ loggedInUser: response.data.username });
        })
    }

    postLogout = () => {
        axios({
            method: 'post',
            url: '/accounts/logout/'
        }).then(() => {
            this.getUserLoggedIn();
            this.updateCurrentPage("home");
        });
    }

    render() {
        const { currentPage, loggedInUser } = this.state;

        console.log(loggedInUser);

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
                            <li><a className={currentPage === "home" ? 'active' : ''} onClick={() => { this.updateCurrentPage("home") }}>Home</a></li>
                            <li><a className={currentPage === "contact" ? 'active' : ''} onClick={() => { this.updateCurrentPage("contact") }}>Contact</a></li>
                            {loggedInUser !== null &&
                                <li><a className={currentPage === "modules" ? 'active' : ''} onClick={() => { this.updateCurrentPage("modules") }}>Modules</a></li>
                            }
                            {loggedInUser === null &&
                                <li><a className={currentPage === "login" ? 'active' : ''} onClick={() => { this.updateCurrentPage("login") }}>Login</a></li>
                            }
                            {loggedInUser !== null &&
                                <span>
                                    <li><a className="logged-in-username">{loggedInUser}</a></li>
                                    <a onClick={this.postLogout} type="submit" className="button">Logout</a>
                                </span>}
                        </ul>
                    </nav>
                </header>

                {currentPage === "home" && <Home />}
                {currentPage === "contact" && <Contact />}
                {currentPage === "login" &&
                    <Login
                        updateCurrentPage={this.updateCurrentPage}
                        getUserLoggedIn={this.getUserLoggedIn}
                    />}
                {currentPage === "signup" &&
                    <SignUp
                        updateCurrentPage={this.updateCurrentPage}
                        getUserLoggedIn={this.getUserLoggedIn}
                    />}
                {currentPage === "modules" &&
                    <Modules
                        updateCurrentPage={this.updateCurrentPage}
                    />}
                {currentPage === "rulesofgame" &&
                    <Modules_rulesofgame />
                }
            </div>
        );
    }
}