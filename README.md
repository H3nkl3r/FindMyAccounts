<p align="center">
  <a href="https://findmyaccounts.com"><img src="https://user-images.githubusercontent.com/22354443/171009590-ea823176-dd29-4cf0-ac56-a065623ed0f4.png" alt="FindMyAccount"></a>
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

https://app.findmyaccounts.com

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
* speed up the process
* Improve exception handling
* Improve testing
* work on user facing and developer facing documentation

## Third Party Dependencies

FindMyAccounts depends on third party libraries to implement some functionality. This document describes which libraries FindMyAccounts depends on. This is a best effort attempt to describe the library's dependencies, it is subject to change as libraries are added/removed.

| Name            | URL                                                | License                |
|-----------------|----------------------------------------------------|------------------------|
| imap-tools      | https://github.com/ikvk/imap_tools                 | Apache-2.0 license     |
| requests        | https://github.com/psf/requests                    | Apache-2.0 license     |
| email-validator | https://github.com/JoshData/python-email-validator | CC0-1.0 license        |
| pandas          | https://github.com/pandas-dev/pandas               | BSD-3-Clause license   |
| validators      | https://github.com/kvesteri/validators             | MIT license            |

### For tests


| Name            | URL                                                | License                |
|-----------------|----------------------------------------------------|------------------------|
| pytest          | https://github.com/pytest-dev/pytest               | MIT license            |
| pytest-cov      | https://github.com/pytest-dev/pytest-cov           | MIT license            |
| tox             | https://github.com/tox-dev/tox                     | MIT license            |