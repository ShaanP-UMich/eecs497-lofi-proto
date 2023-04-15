import React from "react";
import axios from "axios";

export default class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
            operation: "login",
            incorrectLogin: false
        }
    }

    postLoginForm = (event) => {
        event.preventDefault();
        const { username, password, operation } = this.state;
        const { updateCurrentPage, getUserLoggedIn } = this.props;
        let loginFormData = new FormData();

        loginFormData.append('username', username);
        loginFormData.append('password', password);
        loginFormData.append('operation', operation);

        axios({
            method: 'post',
            url: '/accounts/',
            data: loginFormData,
            headers: { "Content-Type": "multipart/form-data" }
        }).then(() => {
            getUserLoggedIn();
            updateCurrentPage("home");
            console.log("the page should go to home");
        }).catch(error => {
            if (error.response) {
                if (error.response.status === 403) {
                    this.setState({ incorrectLogin: true });
                }
            }
        })
    }

    setUsername = (username) => {
        this.setState({ username: username });
    }

    setPassword = (password) => {
        this.setState({ password: password });
    }

    render() {
        const { updateCurrentPage } = this.props;
        const { incorrectLogin } = this.state;

        return (
            <form className="login-form" onSubmit={this.postLoginForm} method="post" encType="multipart/form-data" >
                <label htmlFor="user">Username</label>
                <input type="text" name="username" id="user" placeholder="Your username..." onChange={(e) => { this.setUsername(e.target.value) }} required />
                <label htmlFor="password">Password</label>
                <input type="password" name="password" id="password" placeholder="Your password..." onChange={(e) => { this.setPassword(e.target.value) }} required />
                <div className="button-container">
                    <input type="submit" value="Login" />
                    <span className="button-text">Don't have an account? <a onClick={() => { updateCurrentPage("signup") }}><strong>Sign up</strong></a></span>
                </div>
                {incorrectLogin &&
                    <label className="error-text" >Incorrect username and/or password</label>
                }
                <input type="hidden" name="operation" value="login" />
            </form>
        );
    }
}
