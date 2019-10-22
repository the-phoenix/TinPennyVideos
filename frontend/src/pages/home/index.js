import React from 'react';
import { connect } from "react-redux";
import { Helmet } from "react-helmet";
import actions from "redux/video/actions";
import { Link } from "react-router-dom"

@connect(
  state => ({
    videos: state.video
  }),
  { loadVideos: actions.loadVideos }
)
class VideoListPage extends React.Component {
  componentWillMount() {
    this.props.loadVideos();
  }

  renderVideos(video) {
    return (
      <div className="column is-one-third-desktop is-half-tablet" key={video.id}>
        <div className="card-image">
          <figure className="image is-3by2">
              <img src={video.poster_thumbnail_distributed} alt={video.title} />
            {/* <img src="https://unsplash.it/300/200/?random&pic=2" alt=""> */}
          </figure>
          
          <div className="card-content is-overlay is-clipped">
            <span className="tag is-info">
              {video.category_name}
            </span>       
          </div>
        </div>
        <footer className="card-footer">
          <Link to={"/watch/" + video.id} className="card-footer-item">
            {video.title}
          </Link>
        </footer>
      </div>
    )
  }

  render() {
    const {videos} = this.props;

    return (
      <section className="section is-fullheight is-default is-bold ">
        <Helmet title="Home" />
        <div className="container is-fluid">
            <h1 className="title">Videos</h1>
            <div className="columns is-multiline" id="video-container">
              {videos.results && videos.results.map(video => this.renderVideos(video))}
            </div>
        </div>
      </section>
    );
  }
}

export default VideoListPage
