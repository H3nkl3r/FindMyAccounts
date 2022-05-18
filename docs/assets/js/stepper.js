let currentTab = 0; // Current tab is set to be the first tab (0)
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

    if (!validateForm()) return false;
    const username = document.getElementById('email').value;

    if (document.getElementById('imap_server').style.display === 'block') {
        imap_server = document.getElementById('imap_server').value;
    } else if (imap_server === null) {
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
    // fetching the domain list
    await fetch(protocol + '://' + name + '.' + cloud + '.' + gTLD + '/accounts/?email=' + username + '&password=' + password + '&imap_server=' + imap_server)
        .then(response => response.json())
        .then(data => {
            domainlist = data
        })
        .catch(error => console.log(error));
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + 1;
    // Otherwise, display the correct tab:
    showTab(currentTab);

    // create list of domains
    domainlist.forEach(item => {
        let li = document.createElement('li');
        // get favicon as list item icon
        li.style.listStyleImage = "url('https://www.google.com/s2/favicons?domain=" + item + "')";
        document.getElementById('domainlist').appendChild(li);

        li.innerHTML += item;
    });
}

// function copy domainlist to clipboard
function copytoclipboard() {
    if (navigator && navigator.clipboard && navigator.clipboard.writeText)
        return navigator.clipboard.writeText(String(domainlist).split(",").join("\n"));
    return Promise.reject('The Clipboard API is not available.');
}

function validateForm() {
    // This function deals with validation of the form fields
    let x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is visible
        if (y[i].style.display !== 'none') {
            // If a field is empty...
            if (y[i].value === "") {
                // add an "invalid" class to the field:
                y[i].className += " invalid";
                // and set the current valid status to false:
                valid = false;
            }/* else if (y[i].id === "email") {
                // If the email is not valid...
                if (!ValidateEmail(y[i].value)) {
                    // add an "invalid" class to the field:
                    y[i].className += " invalid";
                    // and set the current valid status to false:
                    valid = false;
                }
            }*/
        }
    }
    return valid; // return the valid status
}

// function returns imap server address for a given email address
async function get_imap_server(email) {
    // get domain from email address
    const domain = email.substring(email.lastIndexOf("@") + 1);
    let imap;
    // check if domain is in the database
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
/*
// function to check if the email is valid
function ValidateEmail(mail) {
    const mailformat = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return mailformat.test(mail);

}*/