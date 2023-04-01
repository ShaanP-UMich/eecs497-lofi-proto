import React from "react";
import axios from "axios";

export default class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
            operation: "login"
        }
    }

    postLoginForm = () => {
        const { username, password, operation } = this.state;
        let loginFormData = new FormData();

        loginFormData.append('username', username);
        loginFormData.append('password', password);
        loginFormData.append('operation', operation);

        axios({
            method: 'post',
            url: '/accounts/',
            data: loginFormData,
            headers: { "Content-Type": "multipart/form-data" }
        });
    }

    postLogout = () => {
        axios({
            method: 'post',
            url: '/accounts/logout/'
        });
    }

    setUsername = (username) => {
        this.setState({ username: username });
    }

    setPassword = (password) => {
        this.setState({ password: password });
    }

    render() {
        return (
            <form className="login-form" action="" method="post" encType="multipart/form-data" >
                <label htmlFor="user">Username</label>
                <input type="text" name="username" id="user" placeholder="Your username..." onChange={(e) => { this.setUsername(e.target.value) }} />
                <label htmlFor="password">Password</label>
                <input type="password" name="password" id="password" placeholder="Your password..." onChange={(e) => { this.setPassword(e.target.value) }} />
                <div className="button-container">
                    <a onClick={this.postLoginForm} type="submit" className="button">Login</a>
                    <a onClick={this.postLogout} type="submit" className="button">Logout</a>
                    <span className="button-text">Don't have an account? <a href="/accounts/create/"><strong>Sign up</strong></a></span>
                </div>
                <input type="hidden" name="operation" value="login" />
            </form>
        );
    }
}
