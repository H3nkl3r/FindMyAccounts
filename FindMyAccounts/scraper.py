# Copyright (c) 2022 Timo Kühne
import logging
import math

from imap_tools import MailBox, MailBoxFolderManager
from imap_tools.errors import MailboxLoginError

from email_validator import validate_email, EmailNotValidError
import pandas as pd
import pickle
import nltk
import re


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


def get_email_headers(username, password, imap_server):
    """
    Scrape the mailbox of a user
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Dataframe with subject and from_
    """
    # validate email address
    email = None
    try:
        # Validate & take the normalized form of the email
        email = validate_email(username).email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        logging.error(f"An exception of type {type(e).__name__}: {e}")
        return "email is not valid"

    email_header_df = pd.DataFrame(columns=['from', 'subject'])
    try:
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
                        email_header_df = email_header_df.append([{'from': msg.from_, 'subject': msg.subject}])
    except MailboxLoginError:
        return 'Authentication failed: If you have 2-Factor-Authentication activated for your Email, you need to use ' \
               'an App-Password '
    except Exception as e:
        logging.error(f"An exception of type {type(e).__name__}: {e}")
        return "An internal error has occurred!"

    email_header_df['domain'] = email_header_df['from'].apply(lambda x: get_domain_from_email(x))

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


def filtered_scrape(username, password, imap_server, filter_domains_list):
    """
    Scrape the mailbox of a user but only for domains that are in the filter_domains_list
    :param filter_domains_list: path to a feature file which contains the domains to filter
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Set of domains
    """
    email_header_df = get_email_headers(username, password, imap_server)
    filter_list = pd.read_feather(filter_domains_list)
    filter_domains = filter_list['domain'].tolist()
    return email_header_df[email_header_df['domain'].isin(filter_domains)][:, 'domain'].drop_duplicates(subset=['domain'], ignore_index=True).to_dict(orient='records')


def preprocess_data(email_header_df):
    """
    Preprocess the data
    :param email_header_df: dataframe containing the email headers
    :return: dataframe containing the email headers
    """
    # to lower case
    email_header_df['subject'] = email_header_df['subject'].str.lower()

    # remove all non-ascii characters
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: re.sub("[^a-z\u00C0-\u017F]", " ", x))
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: re.sub("ä", "ae", x))
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: re.sub("ö", "oe", x))
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: re.sub("ü", "ue", x))
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: re.sub("ß", "ss", x))

    # tokenize
    nltk.download('punkt')
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: nltk.word_tokenize(x))

    # remove stopwords
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('english') + nltk.corpus.stopwords.words('german')
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: [word for word in x if word not in stopwords])

    # lemmatize
    lemmatizer = nltk.stem.WordNetLemmatizer()
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    email_header_df['subject'] = email_header_df['subject'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

    return email_header_df


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


def sklearn_scrape(username, password, imap_server, model, vector_model):
    """
    Scrape the mailbox of a user but only for domains that are in the filter_domains_list
    :param vector_model: path to a pickle file which contains the vectorizer
    :param model: path to a pickle file which contains a fitted sklearn model
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Set of domains
    """
    email_header_df = get_email_headers(username, password, imap_server)

    # load models
    model = pickle.load(open(model, 'rb'))
    vectorizer = pickle.load(open(vector_model, 'rb'))

    # transform data
    email_header_df = preprocess_data(email_header_df)

    subject_features = vectorizer.transform([' '.join(o) for o in email_header_df['subject'].tolist()])

    email_header_df['prediction'] = model.predict(subject_features.toarray())
    email_header_df['probability'] = model.predict_proba(subject_features.toarray())[:, 1]

    # cut to 4 decimals
    email_header_df['probability'] = email_header_df['probability'].apply(lambda x: truncate(x, 2))

    return email_header_df.loc[email_header_df['prediction'] == 1, ['domain', 'probability']].sort_values(by='probability', ascending=False).drop_duplicates(subset=['domain'], ignore_index=True).to_dict(orient='records')






