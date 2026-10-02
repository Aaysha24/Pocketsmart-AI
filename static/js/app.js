const form = document.getElementById("aiForm");
const promptInput = document.getElementById("prompt");
const submitBtn = document.getElementById("submitBtn");
const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const errorText = document.getElementById("errorText");
const resultBox = document.getElementById("resultBox");
const resultText = document.getElementById("resultText");
const copyBtn = document.getElementById("copyBtn");
const characterCount = document.getElementById("characterCount");


if (promptInput && characterCount) {

    promptInput.addEventListener(
        "input",
        function () {

            characterCount.textContent =
                `${promptInput.value.length}/5000`;

        }
    );

}


if (form) {

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const prompt =
                promptInput.value.trim();


            if (!prompt) {

                return;

            }


            submitBtn.disabled = true;

            loading.style.display = "block";

            errorMessage.style.display = "none";

            resultBox.style.display = "none";


            try {

                const response =
                    await fetch(
                        "/generate",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                prompt: prompt
                            })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Something went wrong."
                    );

                }


                resultText.textContent =
                    data.response;

                resultBox.style.display =
                    "block";


            }

            catch (error) {

                errorText.textContent =
                    error.message;

                errorMessage.style.display =
                    "block";

            }

            finally {

                submitBtn.disabled = false;

                loading.style.display =
                    "none";

            }

        }
    );

}


if (copyBtn) {

    copyBtn.addEventListener(
        "click",
        async function () {

            try {

                await navigator.clipboard.writeText(
                    resultText.textContent
                );

                copyBtn.textContent =
                    "Copied!";

                setTimeout(
                    function () {

                        copyBtn.textContent =
                            "Copy";

                    },
                    1500
                );

            }

            catch (error) {

                console.error(
                    "Copy failed:",
                    error
                );

            }

        }
    );

}