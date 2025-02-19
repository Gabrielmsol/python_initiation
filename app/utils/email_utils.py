# %% [markdown]
# # Email Utils
# Esse arquivo é responsavel por manejar
# e cuidar da seleção de emails,
# vamos ter como retorno uma lista cheia de dicionarios.
#
# Como é padrão sempre vai ter um problema,
# por questão de segurança o google te obriga
# a criar uma senha de APP para poder usar essa merda...
#
# [Crie a merda da senha aqui](https://myaccount.google.com/apppasswords)
#
# Voce tambem precisa de Two factor authentication
# ativado para poder ussar essa merda.
# %%
import imaplib
import email
from email.header import decode_header
from email.message import Message
from dotenv import load_dotenv
import os

# Pega informações necessárias
load_dotenv()
imap_server = os.getenv("IMAP_SERVER")
imap_port = os.getenv("IMAP_PORT")
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
email_sender = "something@gmail.com"


def process_email(sender: str = None, max_emails: int = 1) -> list[tuple[str, dict]] | list[None]:
    """
    Função principal responsavel
    por compilar uma lista de emails.
    """
    if not sender:
        sender = email_sender

    mail = connect_to_email_server()
    mail.select("inbox")

    _, messages = mail.search(None, f"FROM {sender}")
    email_ids = messages[0].split()[-max_emails:]

    results = []
    for email_id in email_ids:
        try:
            # RFC822 é uma parada velha de como os emails devem ser extruturados
            # Sei so que funciona, fonts: stackoverflow, se quiser so o corpo do texto
            # substitui o "(RFC822)" por "(UID BODY[TEXT])" ai so vem o corpo mesmo.
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            # Essa merda aqui da problema que so a porra
            # fiz esse gato. o return desse header é uma merda assim =?UTF-8?B?U3ViamVjdCBvZiBNSU5J?="
            # ai precisa dar decode ->[(b'Subject of MINI', 'utf-8')]
            subject_header = decode_header(msg["Subject"])[0]
            subject = subject_header[0]
            if isinstance(subject, bytes):
                subject = subject.decode(
                    subject_header[1] if subject_header[1] else "utf-8"
                )

            email_data = {
                "subject": subject,
                "from": msg["From"],
                "date": msg["Date"],
                "body": get_email_body(msg),
            }
            results.append((email_id, email_data))

        except Exception as e:
            raise RuntimeError(f"Error processing email {email_id}:\n {str(e)}")
    mail.close()
    mail.logout()

    return results


def connect_to_email_server() -> imaplib.IMAP4_SSL:
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        return mail

    except Exception as e:
        print(imap_server)
        print(email_user, email_pass)
        raise RuntimeError(f"Email connection failed: {str(e)}")


def get_email_body(msg: Message) -> str:
    def write_to_file(bodi):
        """Função de debug"""
        file_folder_path = "static/etc"
        os.makedirs(file_folder_path, exist_ok=True)

        base_filename = f"{file_folder_path}/email_body.html"
        file_name = base_filename

        counter = 1
        while os.path.exists(file_name):
            file_name = f"{file_folder_path}/email_body{counter}.html"
            counter += 1

        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(bodi)

    # Checa se o email é simples, sem html or attachemetns
    # depois tranbsforma legivel, se não houver nada retorna uma string vazia em binario,
    # pega o charset, geralmente pé utf-8, se houver erro no parsing ele so limpa.
    if not msg.is_multipart():
        body = (msg.get_payload(decode=True) or b"").decode(
            msg.get_content_charset() or "utf-8", errors="replace"
        )  # .strip() # Se quiser tudo limpo
        write_to_file(body)  # DEBUG
        return body

    for part in msg.walk():
        if part.get_content_maintype() != "text":
            continue  # Pula attachements e HTML

        content_type = part.get_content_type()
        content_disposition = part.get("Content-Disposition", "").lower()

        if "attachment" in content_disposition:
            continue  # Pula attachments, voce pode por eles num file se quiser

        body = part.get_payload(decode=True)
        if body:
            body = body.decode(
                part.get_content_charset() or "utf-8", errors="replace"
            )  # .strip()
            print(content_type)
            if content_type == "text/plain":
                return body  # Tenta pegar so texto ao invez de html.
            # Fiz essa merda que se o bagulho estiver em HTMl
            # pelo menos consigo ler essa bosta.
            elif content_type == "text/html":
                body = part.get_payload(decode=True)
                if body:
                    body = body.decode(
                        part.get_content_charset() or "utf-8", errors="replace"
                    )  # .strip()
                    write_to_file(body)  # DEBUG
                    return body

    return body or ""


# %%
