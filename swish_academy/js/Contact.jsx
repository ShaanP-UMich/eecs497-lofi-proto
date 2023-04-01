import React from "react";

export default class Contact extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <main className="contactContainer" id="contactMain">
                <div className="contactText">
                    <h1>Contact Us</h1>
                    <p>We'd love to chat!</p>
                </div>
                <div className="contactForm">
                    <form action="https://formspree.io/f/xbjbvlvb" method="POST">
                        <label htmlFor="fname">First Name</label>
                        <input type="text" id="fname" name="firstname" placeholder="Your name.." />
                        <br />
                        <label htmlFor="lname">Last Name</label>
                        <br />
                        <input type="text" id="lname" name="lastname" placeholder="Your last name.." />
                        <br />
                        <label htmlFor="email">Personal Email</label>
                        <input type="text" id="email" name="email" placeholder="Your email..." />
                        <br />
                        <label htmlFor="number">Phone Number</label>
                        <input type="text" id="number" name="number" placeholder="Your phone number..." />
                        <br />
                        <label htmlFor="message">Leave a Message</label>
                        <input type="text" id="message" name="message" placeholder="Your message..." />&#8205;
                        <br />
                        <input type="submit" value="Submit" />
                    </form>
                </div>
            </main>
        );
    }
}