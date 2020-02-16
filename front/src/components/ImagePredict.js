import React from 'react';
import axios from 'axios';

class ImagePredict extends React.Component {

    state = {
        image: null,
        predict_result: "",
    };

    handleImageChange = (e) => {
        this.setState({image: e.target.files[0]})
    };

    handleSubmit = (e) => {
        e.preventDefault();
        let form_data = new FormData();
        form_data.append('image', this.state.image, this.state.image.name)

        let url = 'http://localhost:8000/predict/image/';
            axios.post(url, form_data, {
            headers: {
                'content-type': 'multipart/form-data'
            }
        }).then(res => {this.setState({predict_result: res.data})}).catch(err => console.log(err))
    };

    render() {
        return (
            <div className="ui segment">
              <form className="ui form" onSubmit={this.handleSubmit}>
                  <div className="field">
                      <input type="file" 
                          id="image" 
                          accept="image/jpg, video/jpeg"  
                          onChange={this.handleImageChange} 
                          required
                      />
                      <input type="submit"/>
                      <h4> { this.state.predict_result }</h4>
                  </div>
              </form>
            </div>
          );
    }
}

export default ImagePredict;