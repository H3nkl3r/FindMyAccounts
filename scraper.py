import email.parser
import getpass
import imaplib
import json
import re
import sys

from tqdm import tqdm

ADDRESS_PATTERN = re.compile("<(.+)>")  # Finds email as <nospam@nospam.com>


def connect(user, pwd, server):
    """
    Connect to mail server. Return an open connection
    :param user: email address
    :param pwd: password
    :param server: IMAP server address
    :return: IMAP SSl Connection
    """
    conn = imaplib.IMAP4_SSL(server)
    try:
        conn.login(user, pwd)
    except imaplib.IMAP4.error:
        print("Failed to login")
        sys.exit(1)
    return conn


def get_folders(conn):
    """
    Returns a list of folders
    :param conn: IMAP SSL Connection
    :return: list of folders
    """
    folders = []
    for folder in conn.list()[1]:
        folders.append(folder.decode().split(' "/" ')[1])
    return folders


def get_mails_from_folder(conn, folder_name):
    """
    Fetch a specific folder (or label) from server
    :param conn: IMAP SSL Connection
    :param folder_name: Email folder to be analysed
    :return: list of email uid
    """
    typ, uid_data = conn.select(mailbox=folder_name, readonly=True)

    typ, uid_data = conn.search(None, 'ALL')
    if typ != 'OK':
        print("Could not get mail list of folder: ", folder_name)
        return

    return uid_data[0].split()


def fetch_message(conn, msg_uid):
    """
    Fetch a specific message uid (not sequential id!) from the given folder;
    return the parsed message. User must ensure that specified
    message ID exists in that folder
    :param conn: IMAP SSL Connection
    :param msg_uid:
    :return:
    """
    # TODO: Some better approach needed because this takes a lot of time
    # typ, msg_data = conn.fetch(msg_uid, '(RFC822)')
    typ, msg_data = conn.fetch(msg_uid, '(BODY.PEEK[HEADER])')
    if typ != 'OK':
        print("ERROR fetching message #", msg_uid)
        return

    return email.parser.BytesParser().parsebytes(msg_data[0][1], headersonly=True)


def get_sender(msg):
    """
    Given a parsed message, extract and return recipient list
    :param msg: email to be analysed
    :return: returns email sender
    """
    sender = []

    # str conversion is needed for non-ascii chars
    mail_sender = ADDRESS_PATTERN.findall(str(msg['From']))
    sender.extend(mail_sender)

    return sender


def get_imap_server(user):
    """
    Given an email address, return imap server if found
    :param user: email address
    :return: imap server address if specified in json
    """
    domain = user[user.index('@') + 1:]
    with open('imap-server.json') as json_file:
        server = json.load(json_file)
    if domain in server:
        return server[domain]
    else:
        return None


if __name__ == "__main__":
    print('\n#######################\n')

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    imap_server = get_imap_server(username)

    if imap_server is None:
        imap_server = input("Enter IMAP Server: ")

    print('\nStart analysing your emails...\n')

    # Connect
    mail_conn = connect(username, password, imap_server)

    # Open folders and get list of email message uid
    all_sender = []
    for folder in tqdm(get_folders(mail_conn), desc="Total progress", position=0):
        # switch to folder
        for mail_id in tqdm(get_mails_from_folder(mail_conn, folder), desc=f"Analysing {str(folder)}", position=1,
                            leave=False):
            data = fetch_message(mail_conn, mail_id)
            sender_list = get_sender(data)
            all_sender.extend(sender_list)

        mail_conn.close()

    mail_conn.logout()

    print("\n\n List of all UNIQUE accounts:")
    print("-------------------------------")
    all_domains = [x[x.index('@') + 1:].rsplit('.')[-2] for x in set(all_sender)]
    for domain in set(all_domains):
        print(domain)
