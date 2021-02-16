import React from "react";
import axios from "axios";

export default class FetchCookies extends React.Component {
    state = {
        loading: true,
        cookie_name: null
    };

    async componentDidMount() {
        const url = "http://localhost:8888/cookies";
        //const url = "https://api.randomuser.me/";
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        this.setState({cookie_name: data.cookies, loading:false})
    }
    
    render(){
        function clickHandler(){
            console.log("Button clicked")

        }
        console.log(this.state.cookie_name)
        return (
            this.state.loading ? (<div>Loading...</div>):(
                this.state.cookie_name.map( (e, i) => 
                    <div>
                        <div> Cookie name: {e.name} 
                        <button onClick={clickHandler}>Show recipe</button>
                        </div> 
                        <br></br>
                    </div>)
            )
        );


    }
}