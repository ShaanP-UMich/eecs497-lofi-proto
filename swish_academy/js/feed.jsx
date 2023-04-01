import React from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import PropTypes from "prop-types";
import fetchCall from "./helper";
import Post from "./post";

class Feed extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      results: [],
      next: "",
    };

    this.getNext = this.getNext.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    // let url = "/api/v1/posts/";
    const { url } = this.props;
    // url = this.state.endpoints.posts;

    // Call REST API to get the post's information
    fetchCall(url, (data) => {
      this.setState({
        results: data.results,
        next: data.next,
      });
    });
  }

  getNext() {
    const { next } = this.state;
    fetchCall(next, (data) => {
      this.setState((prevState) => ({
        results: prevState.results.concat(data.results),
        next: data.next,
      }));
    });
  }

  render() {
    const { results, next } = this.state;
    const posts = results.map((result) => (
      <Post key={result.postid} url={result.url} />
    ));
    const hasMore = next !== "";

    return (
      <InfiniteScroll
        dataLength={results.length} // This is important field to render the next data
        next={this.getNext}
        hasMore={hasMore}
      >
        {posts}
      </InfiniteScroll>
    );
  }
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Feed;
