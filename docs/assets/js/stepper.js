var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab
let domainlist;

function showTab(n) {
    // This function will display the specified tab of the form ...
    const x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    // ... and run a function that displays the correct step indicator:
    //fixStepIndicator(n)
}

async function next() {
    // This function will figure out which tab to display
    const x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (!validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + 1;
    // Otherwise, display the correct tab:
    showTab(currentTab);
    const username = document.getElementById('email').value
    const password = document.getElementById('password').value
    const imap_server = document.getElementById('imap_server').value
    //domainlist = await eel.expose_scrape(username, password, imap_server)();
    await fetch('https://wheredoihaveanaccount.azurewebsites.net/accounts/?email=' + username + '&password=' + password + '&imap_server=' + imap_server)
        .then(response => response.json())
        .then(data => {
            domainlist = data
        })
        .catch(error => console.log(error))
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + 1;
    // Otherwise, display the correct tab:
    showTab(currentTab);

    // create list of domains
    domainlist.forEach(item => {
    let li = document.createElement('li');
    li.style.listStyleImage = "url('https://www.google.com/s2/favicons?domain=" + item + "')";
    document.getElementById('domainlist').appendChild(li);

    li.innerHTML += item;
});
}

function copytoclipboard() {
    if (navigator && navigator.clipboard && navigator.clipboard.writeText)
        return navigator.clipboard.writeText(String(domainlist).split(",").join("\n"));
    return Promise.reject('The Clipboard API is not available.');
}


function validateForm() {
    // This function deals with validation of the form fields
    let x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    console.log(x)
    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value === "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false:
            valid = false;
        }
    }
    return valid; // return the valid status
}