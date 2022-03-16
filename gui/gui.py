import sys
import tkinter as tk
import tkinter.messagebox
import tkinter.scrolledtext
import webbrowser
from pathlib import Path

from tqdm.tk import tqdm

# Parts of this file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

# Add WhereDoIHaveAnAccount to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    import WhereDoIHaveAnAccount.scraper
except ModuleNotFoundError:
    raise RuntimeError("Couldn't add WhereDoIHaveAnAccount to the PATH.")

# Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"


def gui_scrape(username, password, imap_server):
    """
    Scrape from WhereDoIHaveAnAccount with tqdm gui method
    :param username: email address
    :param password: password for the specified email address
    :param imap_server: imap server for specified email address
    :return: Set of domains

    """
    mail_conn = WhereDoIHaveAnAccount.scraper.connect(username, password, imap_server)

    # Open folders and get list of email message uid
    all_sender = []
    for folder in tqdm(WhereDoIHaveAnAccount.scraper.get_folders(mail_conn), desc="Total progress", position=0,
                       leave=False, tk_parent=window):
        # switch to folder
        for mail_id in tqdm(WhereDoIHaveAnAccount.scraper.get_mails_from_folder(mail_conn, folder),
                            desc=f"Analysing {str(folder)}", position=1,
                            leave=False, tk_parent=window):
            data = WhereDoIHaveAnAccount.scraper.fetch_message(mail_conn, mail_id)
            sender_list = WhereDoIHaveAnAccount.scraper.get_sender(data)
            all_sender.extend(sender_list)

        mail_conn.close()

    mail_conn.logout()

    all_domains = [x[x.index('@') + 1:].rsplit('.')[-2] for x in set(all_sender)]
    email_entry.destroy()
    password_entry.destroy()
    imap_server_entry.destroy()
    analyse_btn.destroy()
    canvas.delete(email_label)
    canvas.delete(password_label)
    canvas.delete(imap_server_label)
    canvas.delete(analyse_label)
    canvas.delete(enter_the_details_label)
    canvas.delete(email_entry_img)
    canvas.delete(password_entry_img)
    canvas.delete(imap_serve_entry_img)

    canvas.create_text(
        720, 88.0, text="Potential accounts.",
        fill="#515486", font=("Arial-BoldMT", int(22.0)))
    account_list = tk.scrolledtext.ScrolledText(window, font=("Arial-BoldMT", int(13.0)), width=30, height=18)
    account_list.place(x=550.0, y=156.0)
    account_list.insert(tk.INSERT, '\n'.join(all_domains))


def btn_clicked():
    email = email_entry.get()
    password = password_entry.get()
    imap_server = imap_server_entry.get()
    imap_server = imap_server.strip()

    if not email:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter email.")
        return
    if not password:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter password.")
        return
    if not imap_server:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Please enter imap server.")
        return

    gui_scrape(email, password, imap_server)


def know_more_clicked():
    instructions = "https://github.com/H3nkl3r/WhereDoIHaveAnAccount/"
    webbrowser.open_new_tab(instructions)


window = tk.Tk()
window.title("WhereDoIHaveAnAccount")

window.geometry("950x519")
window.configure(bg="#000220")
canvas = tk.Canvas(
    window, bg="#000229", height=519, width=950,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431 + 88, 0, 431 + 88 + 431, 0 + 519, fill="#FCFCFC", outline="")
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
email_entry_img = canvas.create_image(700.5, 167.5, image=text_box_bg)
password_entry_img = canvas.create_image(700.5, 248.5, image=text_box_bg)
imap_serve_entry_img = canvas.create_image(700.5, 329.5, image=text_box_bg)

email_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
email_entry.place(x=550.0, y=137 + 25, width=321.0, height=35)
email_entry.focus()

password_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0, show='*')
password_entry.place(x=550.0, y=218 + 25, width=321.0, height=35)

imap_server_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
imap_server_entry.place(x=550.0, y=299 + 25, width=321.0, height=35)

email_label = canvas.create_text(
    550.0, 156.0, text="Email", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
password_label = canvas.create_text(
    550.0, 234.5, text="Password", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
imap_server_label = canvas.create_text(
    550.0, 315.5, text="IMAP Server",
    fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
analyse_label = canvas.create_text(
    646.5, 428.5, text="Analyse",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
enter_the_details_label = canvas.create_text(
    700, 88.0, text="Enter the details.",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))

title = tk.Label(
    text="Welcome to WhereDoIHaveAnAccount", bg="#000229",
    fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)

info_text = tk.Label(
    text="A privacy first, open-source tool\n"
         "that analyses your emails to find out\n"
         "where you possible could have accounts.",
    bg="#000229", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=27.0, y=200.0)

know_more = tk.Label(
    text="Click here for instructions",
    bg="#000229", fg="white", cursor="hand2")
know_more.place(x=27, y=400)
know_more.bind('<Button-1>', know_more_clicked)

analyse_btn_img = tk.PhotoImage(file=ASSETS_PATH / "analyse.png")
analyse_btn = tk.Button(
    image=analyse_btn_img, borderwidth=0, highlightthickness=0,
    command=btn_clicked, relief="flat")
analyse_btn.place(x=557, y=401, width=236, height=50)

window.resizable(False, False)
window.mainloop()
