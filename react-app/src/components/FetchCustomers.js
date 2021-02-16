import React from "react";

export default class FetchCustomers extends React.Component {
    state = {
        loading: true,
        customers: []
    };

    async componentDidMount() {
        const url = "http://localhost:8888/customers";
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        this.setState({customers: data.customers, loading:false})
    }
    
    render(){
        return (
            this.state.loading ? (<div>Loading...</div>):(
                this.state.customers.map( (e) => 
                    <div>
                        <div>Company: {e.name}</div>
                        <div>Address: {e.address}</div>
                        <br></br>
                    </div>)
            )
        );


    }
}