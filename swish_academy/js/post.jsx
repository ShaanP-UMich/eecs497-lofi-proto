import React from "react";
import PropTypes from "prop-types";
import moment from "moment";
import fetchCall from "./helper";

class Post extends React.Component {
  /* Display image and post owner of a single post */
  constructor(props) {
    // Initialize mutable state
    super(props);

    // console.log(props);

    this.state = {
      imgUrl: "",
      owner: "",
      comments: [],
      created: "",
      likes: {
        numLikes: -1,
        lognameLikesThis: false,
      },
      ownerImgUrl: "",
      ownerShowUrl: "",
      postShowUrl: "",
      postid: "",

      value: "",
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDoubleClickLike = this.handleDoubleClickLike.bind(this);
    this.handleLikeClick = this.handleLikeClick.bind(this);
    this.deleteComment = this.deleteComment.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // console.log(url);
    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          imgUrl: data.imgUrl,
          owner: data.owner,
          comments: data.comments,
          likes: data.likes,
          ownerImgUrl: data.ownerImgUrl,
          postShowUrl: data.postShowUrl,
          created: moment.utc(data.created),
          ownerShowUrl: data.ownerShowUrl,
          postid: data.postid,
        });
      })
      .catch((error) => console.log(error));
  }

  handleChange(event) {
    console.log("is this running? ");
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    console.log("handleSubmit is starting");
    event.preventDefault();
    const { value, postid } = this.state;
    let url = "";
    const payload = { text: value };
    url = "/api/v1/comments/?postid=".concat(postid);

    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((comment) => {
        this.setState((prevState) => {
          const { comments } = prevState;
          comments.push(comment);
          console.log("comment pushing is happening");
          return { comments };
        });
      })
      .catch((error) => console.log(error));

    this.setState({
      value: "",
    });

    console.log("handleSubmit is ending");
    event.preventDefault();
  }

  handleLikeClick() {
    let num = 0;
    let { likes } = this.state;
    const { postid } = this.state;

    if (likes.lognameLikesThis) {
      num = -1;
    } else {
      num = 1;
    }

    let url = "";
    let method = "";
    console.log("handleLikeClick url:");

    // this.state.likes.lognameLikesThis ? method = 'DELETE' : method = 'POST';

    if (!likes.lognameLikesThis) {
      url = "/api/v1/likes/?postid=".concat(postid);
      method = "POST";

      fetchCall(
        url,
        (data) => {
          console.log("the 'POST' fetch is running");

          this.setState((prevState) => {
            likes = { ...prevState.likes };
            likes.url = data.url;
            return { likes };
          });
        },
        method
      );
    } else {
      // DELETE
      url = likes.url;
      method = "DELETE";

      fetch(url, { method, credentials: "same-origin" })
        .then(() => {
          console.log("the 'DELETE' fetch is running");
        })
        .catch((error) => console.log(error));
    }

    this.setState((prevState) => {
      likes = { ...prevState.likes };
      likes.numLikes += num;
      likes.lognameLikesThis = !prevState.likes.lognameLikesThis;
      return { likes };
    });
  }

  handleDoubleClickLike() {
    const { likes } = this.state;
    console.log("im here");
    if (!likes.lognameLikesThis) {
      console.log("am i running this?");
      this.handleLikeClick();
    }
  }

  deleteComment(commentid) {
    let url = "";
    url = `/api/v1/comments/${commentid}/`;

    console.log("commentid: ");
    console.log(commentid);

    fetch(url, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
    })
      .then(() => {
        this.setState((prevState) => {
          let { comments } = prevState;
          console.log("comments inside setState");
          console.log(comments);
          // comments.splice(commentid, 1);

          comments = comments.filter(
            (comment) => comment.commentid !== commentid
          );

          console.log("filtered comments array:");
          console.log(comments);

          console.log("comment pushing is happening");
          return { comments };
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const {
      imgUrl,
      owner,
      comments,
      value,
      ownerImgUrl,
      ownerShowUrl,
      postShowUrl,
      created,
      likes,
    } = this.state;
    const timestamp = moment.duration(moment().diff(created)).humanize();

    const commentsList = comments.map((comment) => (
      <Comment
        key={comment.commentid}
        commentid={comment.commentid}
        lognameOwnsThis={comment.lognameOwnsThis}
        ownerShowUrl={comment.ownerShowUrl}
        owner={comment.owner}
        text={comment.text}
        onClick={() => this.deleteComment(comment.commentid)}
      />
    ));

    // console.log("comments:");
    // console.log(this.state.comments);
    // Render post image and post owner
    return (
      <div className="post">
        <div className="post-top">
          <ul>
            <li>
              <a href={ownerShowUrl}>
                <img
                  src={ownerImgUrl}
                  alt={owner}
                  style={{ width: "50px", height: "auto" }}
                />
              </a>
            </li>
            <li>
              <a href={ownerShowUrl}>
                <strong>{owner}</strong>
              </a>
            </li>
            <li style={{ float: "right" }}>
              <a href={postShowUrl}>
                <strong style={{ color: "#857d7d" }}>{timestamp} ago</strong>
              </a>
            </li>
          </ul>
        </div>
        <div className="post-mid">
          <img
            src={imgUrl}
            alt="post_image"
            onDoubleClick={this.handleDoubleClickLike}
          />
        </div>
        <div className="post-bot">
          <Likes
            numLikes={likes.numLikes}
            lognameLikesThis={likes.lognameLikesThis}
            onClick={this.handleLikeClick}
          />
          {commentsList}

          <form className="comment-form" onSubmit={this.handleSubmit}>
            <input type="text" value={value} onChange={this.handleChange} />
          </form>
        </div>
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

// Needs: lognameOwnsThis, onClick, ownerShowUrl, owner, text
function Comment(props) {
  let deleteButton = null;

  const { lognameOwnsThis, onClick, ownerShowUrl, owner, text } = props;

  if (lognameOwnsThis) {
    deleteButton = (
      <button type="button" className="delete-comment-button" onClick={onClick}>
        Delete Comment
      </button>
    );
  }
  return (
    <div className="comment">
      <p>
        <a href={ownerShowUrl}>
          <strong>{owner} &nbsp;</strong>
        </a>
      </p>
      <p>{text}</p>
      {deleteButton}
    </div>
  );
}

Comment.propTypes = {
  lognameOwnsThis: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  ownerShowUrl: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
};

// Needs: lognameLikesThis, numLikes, onClick
function Likes(props) {
  let phrase = "";
  let button = "";
  const { lognameLikesThis, numLikes, onClick } = props;

  if (lognameLikesThis) button = "unlike";
  else button = "like";

  if (numLikes === 1) phrase = " like";
  else phrase = " likes";

  return (
    <div>
      <button type="button" className="like-unlike-button" onClick={onClick}>
        {button}
      </button>
      <p>
        {numLikes}
        {phrase}
      </p>
    </div>
  );
}

Likes.propTypes = {
  numLikes: PropTypes.number.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default Post;
