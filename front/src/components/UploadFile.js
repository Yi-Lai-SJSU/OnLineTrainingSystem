import React, { Component } from 'react';
import axios from 'axios';

class UploadFile extends Component {
  state = {
    title: '',
    content: '',
    video: null
  };

  handleChange = (e) => {
    this.setState({
      [e.target.id]: e.target.value
    })
  };

  handleVideoChange = (e) => {
    this.setState({
        video: e.target.files[0]
    })
  };

  handleSubmit = (e) => {
    e.preventDefault();
    console.log(this.state);
    let form_data = new FormData();

    form_data.append('video', this.state.video, this.state.video.name);
    form_data.append('title', this.state.title);
    form_data.append('content', this.state.content);

    let url = 'http://127.0.0.1:8000/videoToFrames/';
    axios.post(url, form_data, {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }).then(res => {this.props.onSubmit(res.data);}).catch(err => console.log(err))
  };

  render() {
    return (
      <div className="ui segment">
        <form className="ui form" onSubmit={this.handleSubmit}>
            <div className="field">
                <input type="text" 
                    placeholder='Title' 
                    id='title' 
                    value={this.state.title} 
                    onChange={this.handleChange} 
                    required
                />
                <p> </p>
                <input type="text" 
                    placeholder='Content' 
                    id='content' 
                    value={this.state.content} 
                    onChange={this.handleChange} 
                    required
                />
                <p> </p>
                <input type="file" 
                    id="video" 
                    accept="video/mp4, video/mov"  
                    onChange={this.handleVideoChange} 
                    required
                />
                <p> </p>
                <input type="submit"/>
            </div>
        </form>
      </div>
    );
  }
}

export default UploadFile;