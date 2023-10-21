const $all_cupcakes = $("#all-cupcakes")

async function allCupcakes() {
    // When browser loads, makes api call to retrieve all cupcakes and append to div element with all cupcakes

    const cupcakes_all = await Cupcake.showAllCupcakes()

    for (let cupcake of cupcakes_all) {

        let js_cupcake = new Cupcake(cupcake)
        let $new_cupcake = $(js_cupcake.cupcakeHTML());
        $all_cupcakes.append($new_cupcake);
    }; 
}

$(document).ready(allCupcakes)

async function createCupcake(evt) {
    /* 
    When submit button is clicked, goes through values submitted with wtf forms and stores them in empty dictionary.
    Sends data to api and returns a new Cupcake object. If error occurs, error message displays below field that needs 
    user action
    */

    evt.preventDefault()
    const $inputs = $(".input-new-cupcake");
    const $token = $('input[name="csrf_token"]');
    
    data = {}
    
    data["csrf_token"] = $token.val()

    for (let i = 0; i < $inputs.length; i++) {

        let key = $inputs[i].name;
        let value = $inputs[i].value;
        data[key] = value;
    }   
    
    if (data["image"] == "") {
        delete data["image"];
    }

    try {
        let new_cupcake = await Cupcake.createCupcake(data)
        let $html_cupcake = $(new_cupcake.cupcakeHTML());
        $all_cupcakes.append($html_cupcake);
        $("#new-cupcake-form").trigger("reset")
        alert("New Cupcake Created!")
    } catch (error) {
        const response_error = error.response.data.errors
       
        for (const fieldName in response_error) {
            const errorMessage = response_error[fieldName].toString();
            const $errorField = $(`#error-${fieldName}`);
            $errorField.text(errorMessage);
        } 
    }   
}

$("#new-cupcake-form").on("submit", createCupcake);

async function deleteCupcake(evt) {
    /*
    When delete button is clicked for a cupcake, it sends an api request to delete cupcake from api and server.
    Removes cupcake card for delete button that was clicked
    */

    evt.preventDefault()
    const id = $(this).data("cupcake-id")
    await Cupcake.deleteCupcake(id)
    const cupcake_html = $(this).closest("div#cupcake")
    cupcake_html.remove()
    alert("Cupcake Deleted")
}

$("#all-cupcakes").on("click", ".delete-cupcake", deleteCupcake);