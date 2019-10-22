import React, { PureComponent } from "react";
import { Helmet } from "react-helmet";

export default class VideoAddPage extends PureComponent {
  render() {
    return (
      <div>
        <Helmet title="Add a new video" />
        <h1>Add new Video</h1>
      </div>
    )
  }
}
