import React, { Component } from "react";
import FetchCookies from "./components/FetchCookies";
import FetchRecipe from "./components/FetchRecipe";
import FetchCustomers from "./components/FetchCustomers";
import FetchPallets from "./components/FetchPallets";

import Header from "./components/Header"
import Button from "react-bootstrap/Button"



class App extends Component {
  state = {
    visible: true,
    customer: false,
    cookies: false,
    pallet: false

  };

  render() {
    return (
    <div className="App">
      <div>
        <h1>The Bakery API</h1>
        <Button onClick={()=> this.setState({customer: true, cookies: false, pallet: false})}>
          Customers
        </Button>
        <Button onClick={()=> this.setState({customer: false, cookies: true, pallet: false})} >
          Cookies
        </Button>
        <Button onClick={()=> this.setState({customer: false, cookies: false, pallet: true})} >
          Ordered pallets
        </Button>
        {this.state.customer ? <FetchCustomers></FetchCustomers> : 
          this.state.cookies ? <FetchCookies></FetchCookies> : 
                              <FetchPallets></FetchPallets>}
      </div>
      

      {/* <Header /> */}
    </div>
    );
  };
}

export default App;
