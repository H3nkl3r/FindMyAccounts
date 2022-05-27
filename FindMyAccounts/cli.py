# Copyright (c) 2022 Timo Kühne
import getpass
from xml.etree.ElementTree import fromstring

import requests

from FindMyAccounts.scraper import get_domain_from_email, distinct_scrape


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

    domains = distinct_scrape(username, password, imap_server)

    if isinstance(domains, str):
        print(domains)
    else:
        print("\n\n List of all UNIQUE accounts:")
        print("-------------------------------")
        for domain in domains:
            print(domain)
