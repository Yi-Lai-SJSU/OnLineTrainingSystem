import './ImageList.css';
import React from 'react';
import axios from 'axios';

class ImageCard extends React.Component {
    state = {
        term: '',
        currentType: 'Unclassified',
    };

    makePostRequest = async (id, type) => {
        let params = {
          id: id,
          type: type
        }
        let res = await axios.post('http://127.0.0.1:8000/classifyImage/', params);
        console.log(res.data);
    }

    onFormSubmit = (event) => {
        event.preventDefault();
        console.log(this.state.term);
        this.setState({currentType: this.state.term});
        this.makePostRequest(this.props.image.id, this.state.term);
    }

    render() {
        return (
            <div className="ui segment">
                <img id={this.props.image.id} src={this.props.image.url} />
                <form onSubmit={(event) => this.onFormSubmit(event)} className="ui form">
                    <div className="field">
                        <label> { this.state.currentType } </label>
                        <input 
                            type="text" 
                            value={this.state.term}
                            onChange={e=>this.setState({term: e.target.value})}
                        />
                    </div>
                </form>
            </div>
        );
    }
}

export default ImageCard;