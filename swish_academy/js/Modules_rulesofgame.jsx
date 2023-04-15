import React from "react";

export default class Modules_rulesofgame extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div class="module-container">
                <h1>Rules of the Game</h1>
                <h2>Teams</h2>
                <p>
                    Basketball is typically played with two teams, each consisting of 5 players on the court at a time.
                </p>
                <h2>Court Dimensions</h2>
                <p>The basketball court is 94 feet long and 50 feet wide. The court is divided into two halves by the midcourt line.</p>
                <h2>Baskets</h2>
                <p> Each team has a basket located at opposite ends of the court. The basket is mounted on a backboard and is 10 feet high from the ground.</p>
                <h2>Scoring</h2>
                <p>
                    A player scores when he or she shoots the ball into the opponents basket. Each successful shot is worth two points.
                    If the shot is taken beyond the three-point line, it is worth three points.
                </p>
                <h2>Time Limit</h2>
                <p>
                    Each game is divided into four quarters of 12 minutes each. If the game ends in a tie, an overtime period is played.
                </p>
                <h2>Fouls</h2>
                <p>
                    A foul is called when a player makes physical contact with another player.
                    If a player commits more than five fouls, he or she is disqualified from the game.
                </p>
                <h2>Traveling</h2>
                <p>
                    A player cannot move more than two steps without dribbling the ball. If a player moves more than two steps without dribbling,
                    it is considered a violation and the ball is turned over to the opposing team.
                </p>
                <h2>Time-outs</h2>
                <p>
                    Each team is allowed six time-outs per game. Each time-out lasts for one minute.
                </p>
                <h2>Dribbling</h2>
                <p>
                    A player can dribble the ball with one hand at a time.
                    If a player dribbles with both hands or stops dribbling and then starts again, it is considered a violation.
                </p>
                <h2>Passing</h2>
                <p>
                    Players can pass the ball to their teammates by throwing it to them. They can pass the ball using their hands,
                    but cannot throw it to themselves or take more than one step without dribbling after catching the ball.
                </p>
                <h2>Rebounding</h2>
                <p>
                    When a player misses a shot, other players can try to grab the ball before it hits the ground. This is called rebounding and it's an important part of the game.
                </p>
                <h2>Defense</h2>
                <p>
                    Defense: Players can try to steal the ball from their opponents, block their shots, or contest their passes.
                    However, they must do so without fouling, which means making illegal contact with an opponent.
                </p>
                <div id="youtubeVideo">
                    <iframe width="560" height="315"
                        src="https://www.youtube.com/embed/XbtmGKif7Ck"
                        title="YouTube video player" frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                    <figcaption>This video has a great visual representation of the rules we discussed above.</figcaption>
                </div>
                <p>Have fun and play fair!
                    Basketball is a team sport that requires good sportsmanship, teamwork, and respect for the rules and opponents.</p>
            </div>

        );
    }
}
