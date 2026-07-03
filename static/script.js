const predictBtn = document.getElementById("predictBtn");
const textInput = document.getElementById("textInput");

const loading = document.getElementById("loading");
const resultCard = document.getElementById("resultCard");

const prediction = document.getElementById("prediction");
const confidence = document.getElementById("confidence");
const progressBar = document.getElementById("progressBar");


predictBtn.addEventListener("click", async () => {

    const text = textInput.value.trim();

    if (text.length === 0) {
        alert("Please enter some text.");
        return;
    }

    loading.classList.remove("hidden");
    resultCard.classList.add("hidden");

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });

        const data = await response.json();

        loading.classList.add("hidden");

        if (data.success) {

            prediction.innerText = data.prediction;

            confidence.innerText = data.confidence;

            progressBar.style.width = data.confidence + "%";

            resultCard.classList.remove("hidden");

        }
        else {

            alert(data.message);

        }

    }
    catch (error) {

        loading.classList.add("hidden");

        alert("Server Error. Please try again.");

        console.log(error);

    }

});
