<p align="center">
  FindMyAccounts
</p>
<p align="center">
    <em>A privacy first, open-source tool that analyses your emails to find out where you possible could have accounts.</em>
</p>
<p align="center">
<a href="https://github.com/H3nkl3r/FindMyAccounts/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/h3nkl3r/FindMyAccounts/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/h3nkl3r/FindMyAccounts" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/h3nkl3r/FindMyAccounts?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/FindMyAccounts" target="_blank">
    <img src="https://img.shields.io/pypi/v/FindMyAccounts?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/FindMyAccounts" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/FindMyAccounts?color=%2334D058" alt="Supported Python versions">
</a>
</p>

#

Did you ever wonder where you have all registered your email address? In the best case you have a Password manager where
you keep all this info but in case you haven't here is your tool.

## About
I got into this because I wanted to fill my password manager with all accounts I have. 
But I had problems finding them all, so I did this bit over engineered script.
I hope it helps you find all your accounts.

## Usage

Just go for the online tool and fill in your email and password.

https://h3nkl3r.github.io/WhereDoIHaveAnAccount-online/

### For Experts
`$ pip install FindMyAccounts`

To get started right away:

`$ FindMyAccounts`

You can run FindMyAccounts as a package if running it as a script doesn't work:

`$ python -m FindMyAccounts`

After that Enter your email address

If you have 2FA activated for your email account, you need to use an app password.

## Limitations 
* Assumption that every account you have is linked to your email address
* Every Account provider sent a verification email to your email

## Contribution
Pull requests are very welcomed.
### ToDo
* Implement Gmail API (see Issue for more info)
* More exception handling
* Better testing
