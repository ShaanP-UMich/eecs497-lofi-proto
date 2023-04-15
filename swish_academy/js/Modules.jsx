import React from "react";
import axios from "axios";

export default class Modules extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { updateCurrentPage } = this.props;

        return (
            <div className="modules-container">
                <div className="module-item">
                    <h2>Module 1: The Basics</h2>
                    <div className="module-item-img">
                        <img src="static/imgs/basketball-hoop.png" />
                    </div>
                    <div className="module-item-box">
                        <ul className="module-item-list">
                            <li><a className="module-item-list-item" onClick={() => {updateCurrentPage('rulesofgame')}}>Rules of the Game</a></li>
                            <li><a className="module-item-list-item" href="index.html">Dribbling Basics</a></li>
                            <li><a className="module-item-list-item" href="index.html">Shooting Basics</a></li>
                        </ul>
                    </div>
                </div>

                <div className="module-item">
                    <h2>Module 2: Positions</h2>
                    <div className="module-item-img">
                        <img src="static/imgs/positions_2.png" />
                    </div>
                    <div className="module-item-box">
                        <ul className="module-item-list">
                            <li><a className="module-item-list-item" href="index.html">Guard</a></li>
                            <li><a className="module-item-list-item" href="index.html">Forward</a></li>
                            <li><a className="module-item-list-item" href="index.html">Center</a></li>
                        </ul>
                    </div>
                </div>

                <div className="module-item">
                    <h2>Module 3: Teamwork</h2>
                    <div className="module-item-img">
                        <img src="static/imgs/teamwork.jpg" />
                    </div>
                    <div className="module-item-box">
                        <ul className="module-item-list">
                            <li><a className="module-item-list-item" href="index.html">Passing</a></li>
                            <li><a className="module-item-list-item" href="index.html">Screens</a></li>
                            <li><a className="module-item-list-item" href="index.html">Cutting</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        );
    }
}