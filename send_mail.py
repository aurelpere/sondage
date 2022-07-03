import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import pandas as pd
def process_server(csv_file):
    df = pd.read_csv('mapping.csv', sep=';')
    for index, row in df.iterrows():
        if row['name']=='ini':
            continue
        mailcsv=row['name']
        port=row['port']
        price=re.findall(r'\d{2}', row['name'])[0]
        yield(mailcsv,port,price)

def process_csv(csv_file):
    df=pd.read_csv(csv_file,sep=';',dtype={'hash':'str'})
    for index, row in df.iterrows():
        hash_=row['hash']
        email=row['email']
        name=row['name']
        yield(name,email,hash_)

def send(name,email,hash_,price,port):
    # me == my email address
    # you == recipient's email address
    me = "matangi.dev@gmail.com"
    you = f"{email}"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Message à l'attention de {name} - votre avis sur un service contre le harcèlement"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = """La société Matangi met en place un service web et mobile contre le harcèlement et sollicite votre avis\n
    Seriez-vous intéressé pour être référencé sur un annuaire des professionnels du harcèlement sur l'appli web et mobile ?\n
    Je serais intéressé pour un abonnement de X€ / mois: https://server:port/?answeryes=1&amp;answerno=0&amp;hash=x\n
    Je ne suis pas intéressé:https://server:port/?answeryes=0&amp;answerno=1&amp;hash=x\n
    Plus d'infos: www.harcelement.app"""
    text = text.replace('X€ / mois', f'{price}€ / mois')
    with open ('mailing.html','r',encoding='utf-8') as fileo:
        html=fileo.read()
        html=html.replace('X€ / mois',f'{price}€ / mois')
        html = html.replace('X€ / mois', f'{price}€ / mois')
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('matangi.dev@gmail.com', 'sjxuqzwduqtjrdoo')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()

if __name__ == '__main__':
    #for mailcsv_port_price in process_server('mapping.csv'):
    #    for name_email_hash in process_csv(mailcsv_port_price[0]):
    #        send(name_email_hash[0],name_email_hash[1],name_email_hash[2],mailcsv_port_price[2],mailcsv_port_price[1])
