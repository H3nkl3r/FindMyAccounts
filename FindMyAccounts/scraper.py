# Copyright (c) 2022 Timo Kühne
import logging
import validators

from imap_tools import MailBox, MailBoxFolderManager

from email_validator import validate_email
import pandas as pd


def get_domain_from_email(email):
    """
    Get the domain from an email address
    :param email:
    :return:
    """
    try:
        domain = email[email.index('@') + 1:]
    except ValueError:
        domain = None
    return domain


class DomainNotValidError(ValueError):
    pass


def validate_domain(domain):
    """
    Validate a domain
    :param domain:
    :return:
    """
    if not validators.domain(domain):
        raise DomainNotValidError("The domain is not valid")
    return domain


def get_email_headers(username, password, imap_server):
    """
    Scrape the mailbox of a user
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Dataframe with subject and from_
    """
    # validate email address
    email = validate_email(username).email

    # fqdn validation of imap_server hostname
    imap_server = validate_domain(imap_server)

    email_header_df = pd.DataFrame(columns=['from', 'subject'])
    with MailBox(imap_server).login(email, password) as mailbox:
        # iterate over all folders
        for folder in MailBoxFolderManager(mailbox).list():
            # not scraping the sent folder because it is not necessary
            if 'sent' in folder.name.lower():
                continue
            mailbox.folder.set(folder.name)
            found_nums = mailbox.numbers('ALL')
            page_len = 100
            # if needed because of even and odd folder sizes
            pages = int(len(found_nums) // page_len) + 1 if len(found_nums) % page_len else int(
                len(found_nums) // page_len)
            # iterate over all pages
            for page in range(pages):
                page_limit = slice(page * page_len, page * page_len + page_len)
                for msg in mailbox.fetch(headers_only=True, bulk=True, limit=page_limit):
                    email_header_df = pd.concat([email_header_df, pd.DataFrame({'from': [msg.from_], 'subject': [msg.subject]})])

    # remove rows where from is ''
    email_header_df = email_header_df[email_header_df['from'] != '']

    email_header_df['domain'] = email_header_df['from'].apply(lambda x: get_domain_from_email(x))

    # remove rows where from is None
    email_header_df = email_header_df[email_header_df['from'] != 'None']

    # set type of columns to string
    email_header_df['from'] = email_header_df['from'].astype(str)
    email_header_df['subject'] = email_header_df['subject'].astype(str)

    return email_header_df


def distinct_scrape(username, password, imap_server):
    """
    Scrape the mailbox of a user
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Set of domains
    """

    email_header_df = get_email_headers(username, password, imap_server)

    return email_header_df['domain'].to_frame().drop_duplicates(subset=['domain'], ignore_index=True).to_dict(orient='records')
