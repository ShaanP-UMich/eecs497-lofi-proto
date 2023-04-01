import React from "react";

export default class Login extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <form class="login-form" action="/accounts/?target=/" method="post" enctype="multipart/form-data"/>
            <label for="user">Username</label>
            <input type="text" name="username" id="user" placeholder="Your username..." required />
            <label for="password">Password</label>
            <input type="password" name="password" id="password" placeholder="Your password..." required />
            <div class="button-container">
                <a href="indexx.html" type="submit" class="button">Login</a>
                <span class="button-text">Don't have an account? <a href="/accounts/create/"><strong>Sign up</strong></a></span>
            </div>
            <input type="hidden" name="operation" value="login" />
            </form>
        );
    }
}
