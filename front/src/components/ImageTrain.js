import React from 'react';
import axios from 'axios';

class ImageTrain extends React.Component {
    state = {
        currentStatus: "Press this button to Train New Model",
        isButtonPressed: false,
        task_id: null,
        timerId: null,
    };

    checkStatusOfTrainingModel() {
        if (this.state.task_id) {
            console.log(this.state.task_id);
            axios.get('http://localhost:8000/trainModel/checkStatus/', {
                        params: {
                            task_id: this.state.task_id
                        }
                    }).then(response =>{
                        console.log(response);
                        if (response.data === "yes") {
                            console.log("Congraduation!");
                            alert("Model training done");
                            clearInterval(this.state.timerId);
                            this.setState({currentStatus: "New model has generated"});
                        }
                        if (response.data === 'no') {
                            console.log("Waiting please");
                        }
                    });
        }
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.setState({currentStatus: "Model is being trained, please wait"})

        axios.get('http://localhost:8000/trainModel/train/').then(response => { 
                 console.log(response);
                 this.setState({task_id : response.data});
                 this.setState({timerId: setInterval(() => this.checkStatusOfTrainingModel(), 100000)});
        }).catch(function (error) { console.log(error); });
    }

    render() {
        return (
            <div className="ui segment">
                <form className="ui form" onSubmit={this.handleSubmit}>
                    <label>{ this.state.currentStatus + ":   "}</label>
                    <button type="submit">Training models</button>
                </form>
            </div>
        )
    }
}

export default ImageTrain;