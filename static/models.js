const base_url = "http://127.0.0.1:5000/api";

class Cupcake {
    /*
    Models a cupcake to be used on client side and interact with api
    */

    constructor({id, flavor, size, rating, image}) {
        this.id = id;
        this.flavor = flavor;
        this.size = size;
        this.rating = rating;
        this.image = image;
    }

    cupcakeHTML() {
        /* 
        Generates HTML for cupcake that returns a div element with information 
        about cupcake and image
        */
    
        return `
        <div class="col-lg-3 col-md-4 mb-3" id="cupcake">
            <div>
                <div class="card">
                    <img 
                    src="${this.image}" 
                    class="card-img-top img-fluid" 
                    alt="${this.flavor} cupcake">
                    <div class="card-body">
                        <h5 class="card-title">${this.flavor} cupcake</h5>
                        <ul> 
                          <li>Size: ${this.size}</li>
                          <li>Rating: ${this.rating}
                        </ul>
                        <button data-cupcake-id=${this.id} class="delete-cupcake btn btn-danger">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        `;
    };

    static async showAllCupcakes() {
        /* 
        Calls api to retrieve all cupcakes stored in server and returns 
        json data of all cupcakes
        */
    
        const response = await axios.get(`${base_url}/cupcakes`)
    
        return response.data.cupcakes
    }
    
    static async createCupcake(data) {
        /*
        Calls api to create a new post request and returns new Cupcake
        */

        const response = await axios.post(`${base_url}/cupcakes`, data)
   
        let { cupcake } = response.data

        return new Cupcake(
            {
                id: cupcake.id,
                flavor: cupcake.flavor,
                size: cupcake.size,
                rating: cupcake.rating,
                image: cupcake.image
            }
        )

    }

    static async deleteCupcake(id) {
        /* 
        Calls api to delete a cupcake from the server and returns response
        */

        const response = await axios.delete(`${base_url}/cupcakes/${id}`)

        return response.data
    }
}