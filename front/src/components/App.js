import React from 'react';
import UploadFile from './UploadFile';
import ImageList from './ImageList';
import ImageTrain from './ImageTrain';
import ImagePredict from './ImagePredict';

class App extends React.Component {
    state = {
        images: []
    };

    onUploadSubmit = (images) => {
        console.log("App here:")
        console.log(images);
        this.setState({images: images});
    }

    render() {
        return (
            <div className="ui container" style={{ marginTop: '10px' }}>
                <UploadFile onSubmit={this.onUploadSubmit} />
                <ImageTrain />
                <ImagePredict />
                <ImageList images={this.state.images}/>
            </div>
        )
    }
}

export default App;
