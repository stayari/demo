import React from "react";

export default class FetchPallets extends React.Component {
    state = {
        loading: true,
        pallets: []
    };

    async componentDidMount() {
        const url = "http://localhost:8888/pallets";
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        this.setState({pallets: data.pallets, loading:false})
    }
    
    render(){
        return (
            this.state.loading ? (<div>Loading...</div>):(
                this.state.pallets.map( (e) => 
                    <div>
                        <div>Pallet ID : {e.id}</div>
                        <div>Cookie to produce: {e.cookie}</div>
                        <div>Delivery date: {e.productionDate}</div>
                        <br></br>
                    </div>)
            )
        );


    }
}