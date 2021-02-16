import React from "react";

export default class FetchRecipe extends React.Component {
    state = {
        loading: true,
        recipes: []
    };

    async componentDidMount() {
        const url = "http://localhost:8888/recipes";
        const response = await fetch(url);
        const data = await response.json();

        console.log(data);
        this.setState({recipes: data.recipes, loading: false})
    }

    
    render(){
        return (
            this.state.loading ? <div>Loading...</div> : this.state.recipes.length == 0 ? <div>Got no recipes</div> :  <div>
            {this.state.recipes}

        </div>      
            
        );


    }
}