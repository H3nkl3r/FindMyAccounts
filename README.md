# WhereDoIHaveAnAccount

![GitHub](https://img.shields.io/github/license/h3nkl3r/WhereDoIHaveAnAccount)
![GitHub](https://github.com/h3nkl3r/wheredoihaveanaccount/actions/workflows/tests.yml/badge.svg)

Did you ever wonder where you have all registered your email address? In the best case you have a Password manager where
you keep all this info but in case you haven't here is your tool.

## About
I got into this because I wanted to fill my password manager with all accounts I have. 
But I had problems finding them all, so I did this bit over engineered script.
I hope it helps you find all your accounts.

## Usage
`$ pip install git+https://github.com/H3nkl3r/WhereDoIHaveAnAccount`

To get started right away:

`$ WhereDoIHaveAnAccount`

You can run WhereDoIHaveAnAccount as a package if running it as a script doesn't work:

`$ python -m WhereDoIHaveAnAccount`

After that Enter your email address

If you have 2FA activated for your email account, you need to use an app password.

## Limitations 
* Assumption that every account you have is linked to your email address
* Every Account provider sent a verification email to your email

## Contribution
Pull requests are very welcomed.
### ToDo
* Add new servers to the imap-server list
* Make the whole thing go faster
* Add a way to search every folder but not the "sent" folder
