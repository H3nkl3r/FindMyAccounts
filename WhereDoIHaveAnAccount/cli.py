"""
    WhereDoIHaveAnAccount
    Copyright (C) 2022  Timo Kühne
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import getpass
from xml.etree.ElementTree import fromstring

import requests

from WhereDoIHaveAnAccount.scraper import get_domain_from_email, scrape


def get_imap_server(user):
    """
    Given an email address, return imap server if found
    :param user: email address
    :return: imap server address if specified in json
    """
    try:
        r = requests.get('https://autoconfig.thunderbird.net/v1.1/' + get_domain_from_email(user))
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        return None

    root = fromstring(r.content)
    for child in root[0]:
        if child.tag == 'incomingServer':
            return child[0].text


def main():
    print('\n#######################\n')

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    imap_server = get_imap_server(username)

    if imap_server is None:
        imap_server = input("Enter IMAP Server: ")

    print('\nStart analysing your emails...\n')

    domains = scrape(username, password, imap_server)

    print("\n\n List of all UNIQUE accounts:")
    print("-------------------------------")
    for domain in domains:
        print(domain)