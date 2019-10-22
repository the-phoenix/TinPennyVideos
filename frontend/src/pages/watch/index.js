import React from 'react';
import { connect } from "react-redux";
import { Helmet } from "react-helmet";
import {
  useParams
} from "react-router";
import actions from "redux/video/actions";
import VideoPlayer from "components/VideoPlayers/HLSVideoPlayer";
// import './App.css';

@connect(
  (state, { videoId }) => ({
    video: (state.video.results || []).find(({id}) => id === videoId) || state.video.individual,
    loading: state.video.loading,

  }),
  { loadIndividualVideo: actions.loadIndividualVideo }
)
class WatchPage extends React.Component {
  componentWillMount() {
    const {video, videoId} = this.props;

    if (!video) {
      this.props.loadIndividualVideo(videoId);
    }
  }

  renderVideo(video) {
    const hlsSource = video.streams.find(stream => stream.includes(".m3u8"));
    if (!hlsSource) {
      throw new Error("Missing HLS format from video streams");
    }

    return (
      <div className="columns is-vcentered">
        <div className="column is-7">
          {/* <figure className="image is-4by3"> */}
          <figure className="image">
              <VideoPlayer source={hlsSource} />
          </figure>
        </div>
        <div className="column is-4 is-offset-1">
          <h1 className="title is-2">
            {video.title}
          </h1>
          <h2 className="subtitle is-4">
            {video.publisher}
          </h2>
          <h2 className="subtitle is-5">
            Category: {video.category_name}
          </h2>
          <h3 className="subtitle is-5">
            Modified: {video.modified}
          </h3>
        </div>
      </div>
    )
  } 
  renderLoading() {
    return <h1>Loading...</h1>
  }
  render() {
    let { loading, video } = this.props;

    return (
      <section className="section is-fullheight is-default is-bold ">
        <Helmet title="View Video" />
        {loading && this.renderLoading()}
        {video && this.renderVideo(video)}
        {!video && !loading && <h1>Something went wrong!</h1>}
      </section>
    );
  }
}

export default function Watch() {
  const { id } = useParams()
  return <WatchPage videoId={id} />
}
