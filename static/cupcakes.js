const cupcakesList = document.querySelector(".cupcakes-list")

async function displayCupcakes() {
    const response = await axios.get('/api/cupcakes')
    for (const cupcake of response.data.cupcakes) {
        const { flavor, size, rating, image_url } = cupcake

        const newCupcake = document.createElement("li")
        newCupcake.classList.add("list-group-item")

        const newCupcakeCard = document.createElement("div")
        newCupcakeCard.classList.add("card")
        newCupcakeCard.classList.add("w-25")

        const newCupcakeImage = document.createElement("img")
        newCupcakeImage.classList.add("card-img-top")
        newCupcakeImage.setAttribute('src', image_url)
        newCupcakeImage.setAttribute('alt', `Image of ${flavor} flavored cupcake`)

        const newCupcakeBody = document.createElement("div")
        newCupcakeBody.classList.add("card-body")

        const newCupcakeTitle = document.createElement("h4")
        newCupcakeTitle.classList.add("card-title")
        newCupcakeTitle.textContent = `${flavor} flavored cupcake`
        
        const newCupcakeDescription = document.createElement("p")
        newCupcakeDescription.classList.add("card-text")
        newCupcakeDescription.classList.add("font-weight-bold")
        newCupcakeDescription.textContent = `${size} size. Rating: ${rating}`

        newCupcakeBody.append(newCupcakeTitle)
        newCupcakeBody.append(newCupcakeDescription)
        newCupcakeCard.append(newCupcakeImage)
        newCupcakeCard.append(newCupcakeBody)
        newCupcake.append(newCupcakeCard)
        cupcakesList.append(newCupcake)

    }
}

displayCupcakes()