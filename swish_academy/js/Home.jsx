import React from "react";

export default class Home extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <div className="main-container">
                    <img src="static/imgs/kids-playing_2.png" />

                    <div>
                        <h1>Our Mission</h1>
                        <p>Our mission at Swish Academy is to provide a fun, engaging, and educational platform where kids can learn
                            the fundamentals of basketball. Our goal is to inspire a love for the game and help young players
                            develop the skills, confidence, and teamwork needed to succeed both on and off the court.
                        </p>
                    </div>
                    <div>
                        <h1>Our Culture</h1>
                        <p>We strive to create a safe and inclusive environment where children of all backgrounds and abilities can
                            come together to learn and play the game of basketball. Our website offers a variety of resources,
                            including instructional videos, drills, and tips from experienced coaches and players.
                            We are committed to helping kids improve their basketball skills while fostering a sense of
                            sportsmanship and community.</p>
                    </div>
                </div>

                <div className='student-testimonials'>
                    <h1>Raving Reviews</h1>
                    <ul className="student-test-list">
                        <li className="student-test-item">
                            <img id="panda-test" src="static/imgs/cartman.png" />
                            <div className="student-test-text">
                                <p>Billy Smogemaster</p>
                                <p>Age 12 • 6th Grade</p>
                                <p><i>"Swish Academy made learning the sport of basketball so easy and fun!"</i></p>
                            </div>
                        </li>
                        <li className="student-test-item">
                            <img id="chicken-test" src="static/imgs/kenny.png" />
                            <div className="student-test-text">
                                <p>Robby Bedgeman</p>
                                <p>Age 10 • 4th Grade</p>
                                <p><i>"I feel alot more confident in my basketball skills with Swish Academy"</i></p>
                            </div>
                        </li>
                        <li className="student-test-item">
                            <img id="shark-test" src="static/imgs/butters.png" />
                            <div className="student-test-text">
                                <p>Big Mike</p>
                                <p>Age 11 • 5th Grade</p>
                                <p><i>"The dribbling module taught by Pranav Kasula was very easy to follow!"</i></p>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        );
    }
}

