// DOM Element References
const dateInput = document.getElementById("date-input");
const sunsetCheckbox = document.getElementById("sunset-checkbox");
const form = document.getElementById("converter-form");
const convertBtn = document.getElementById("convert-btn");
const resultBox = document.getElementById("result-box");
const errorBox = document.getElementById("error-box");
const gregorianDisplay = document.getElementById("gregorian-display");
const hebrewDisplay = document.getElementById("hebrew-display");

// Date Picker Initialization (Default Today & Dynamic +/- 200 Years Range)
const today = new Date();
const currentYear = today.getFullYear();

dateInput.value = today.toISOString().split("T")[0];
dateInput.min = `${currentYear - 200}-01-01`;
dateInput.max = `${currentYear + 200}-12-31`;

// Form Submission & Backend Integration Handler
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // 1. Reset UI State & Lock Submit Button
    errorBox.classList.add("hidden");
    resultBox.classList.add("hidden");
    convertBtn.disabled = true;
    convertBtn.textContent = "Converting...";

    try {
        // 2. Send Asynchronous POST Request to Flask Service
        const response = await fetch("/api/convert", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                date: dateInput.value,
                after_sunset: sunsetCheckbox.checked
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Conversion failed.");
        }

        // 3. Populate & Display Conversion Results
        gregorianDisplay.textContent = `Gregorian: ${data.gregorian_date}`;
        hebrewDisplay.textContent = data.hebrew_date;
        resultBox.classList.remove("hidden");
    } catch (err) {
        // 4. Display Validation or Network Errors
        errorBox.textContent = err.message;
        errorBox.classList.remove("hidden");
    } finally {
        // 5. Restore Submit Button State
        convertBtn.disabled = false;
        convertBtn.textContent = "Convert";
    }
});