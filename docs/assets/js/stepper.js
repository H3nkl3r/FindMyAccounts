var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab
let domainlist;
let imap_server = null;
const name = 'wheredoihaveanaccount';
const protocol = 'https';
const cloud = 'azurewebsites';
const gTLD = 'net';

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

    if (!validateForm(0)) return false;
    if (!ValidateEmail(document.getElementById("email").value)) return false;
    if (!validateForm(1)) return false;
    const username = document.getElementById('email').value;

    if(document.getElementById('imap_server').style.display === 'block'){
        imap_server = document.getElementById('imap_server').value;
    } else if(imap_server === null){
        imap_server = await get_imap_server(username);
        if (imap_server === 'Not in DB') {
            document.getElementById('imap_server').style.display = 'block';
            document.getElementById('imap_server_label').style.display = 'block';
            return false;
        }
    }

    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + 1;
    // Otherwise, display the correct tab:
    showTab(currentTab);
    const password = document.getElementById('password').value
    await fetch(protocol + '://' + name + '.' + cloud + '.' + gTLD + '/accounts/?email=' + username + '&password=' + password + '&imap_server=' + imap_server)
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

function validateForm(n) {
    // This function deals with validation of the form fields
    let x, y, valid = true;
    x = document.getElementsByClassName("tab");
    console.log(x)
    y = x[currentTab].getElementsByTagName("input");
    // If a field is empty...
    if (y[n].value === "") {
        // add an "invalid" class to the field:
        y[n].className += " invalid";
        // and set the current valid status to false:
        valid = false;
    }
    return valid; // return the valid status
}

async function get_imap_server(email){
    const name = email.substring(0, email.lastIndexOf("@"));
    const domain = email.substring(email.lastIndexOf("@") + 1);
    let imap;
    await fetch('https://autoconfig.thunderbird.net/v1.1/' + domain)
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let xmlDoc = parser.parseFromString(data, "text/xml");
            imap = xmlDoc.getElementsByTagName("incomingServer")[0].getElementsByTagName("hostname")[0].childNodes[0].nodeValue.toString();
        })
        .catch(error => {
            imap = 'Not in DB';
        });
    return imap;
}

function ValidateEmail(inputText)
{
    const mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(!inputText.value.match(mailformat)) {
        inputText.className += " invalid";
        return false;
    }
    return true;
}