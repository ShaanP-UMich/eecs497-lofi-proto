import React from "react";
import axios from "axios";

export default class SignUp extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            fullname: "",
            username: "",
            email: "",
            file: null,
            password: "",
            operation: "create"
        }
    }

    postCreateForm = (event) => {
        event.preventDefault();
        const { fullname, username, email, file, password, operation } = this.state;
        const { updateCurrentPage, getUserLoggedIn } = this.props;

        let loginFormData = new FormData();

        loginFormData.append('fullname', fullname);
        loginFormData.append('username', username);
        loginFormData.append('email', email);
        loginFormData.append('file', file);
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
        });

    }

    setFullname = (fullname) => {
        this.setState({ fullname: fullname });
    }

    setUsername = (username) => {
        this.setState({ username: username });
    }

    setEmail = (email) => {
        this.setState({ email: email });
    }

    setFile = (event) => {
        const img = event.target.files[0];
        this.setState({ file: img });
        // console.log(img);
    }

    setPassword = (password) => {
        this.setState({ password: password });
    }

    render() {
        const { updateCurrentPage } = this.props;

        return (
            <div>
                <form className="login-form" onSubmit={this.postCreateForm} method="post" encType="multipart/form-data">
                    <label>Profile Picture</label><input type="file" accept="image/*" name="file"
                        onChange={this.setFile} required />
                    <br />
                    <label>Full Name</label><input type="text" name="fullname" required
                        onChange={(e) => { this.setFullname(e.target.value) }} />
                    <br />
                    <label>Username</label><input type="text" name="username" required
                        onChange={(e) => { this.setUsername(e.target.value) }} />
                    <br />
                    <label>Email</label><input type="email" name="email" required
                        onChange={(e) => { this.setEmail(e.target.value) }} />
                    <br />
                    <label>Password</label><input type="password" name="password" required
                        onChange={(e) => { this.setPassword(e.target.value) }} />
                    <br />
                    {/* <a onClick={this.postCreateForm} type="submit" className="button">Sign Up</a> */}
                    <input type="submit" name="signup" value="Sign Up" />
                    <br />
                    <input type="hidden" name="operation" value="create" />
                </form>

                <p>Have an account? <a style={{color: 'blue', textDecoration: 'underline' }} onClick={() => { updateCurrentPage("login") }}> <strong>Log in</strong></a></p>
            </div>
        );
    }
}