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
import json

from imap_tools import MailBox, MailBoxFolderManager
from importlib_resources import files


def get_imap_server(user):
    """
    Given an email address, return imap server if found
    :param user: email address
    :return: imap server address if specified in json
    """
    domain = user[user.index('@') + 1:]
    with open(files('WhereDoIHaveAnAccount').joinpath('imap-server.json')) as json_file:
        server = json.load(json_file)
    if domain in server:
        return server[domain]
    else:
        return None


def scrape(username, password, imap_server):
    """
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Set of domains

    """
    von = []
    with MailBox(imap_server).login(username, password) as mailbox:
        for folder in MailBoxFolderManager(mailbox).list():
            if 'sent' in folder.name.lower():
                continue
            mailbox.folder.set(folder.name)
            for msg in mailbox.fetch(headers_only=True, bulk=True):
                von.append(msg.from_)

    domains = []
    for email_address in von:
        try:
            domains.append('.'.join(email_address.split('@')[1].split('.')[-2:]))
        except IndexError:
            continue

    domains = set(domains)
    return domains


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
