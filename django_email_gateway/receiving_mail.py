import json
from lxml import html


def sns_notification(body):
    json_body = body.decode('utf8')
    js = json.loads(json_body.replace('\n', ''))
    if js["Type"] == "Notification":
        arg_info = js["Message"]
        arg_info = json.loads(arg_info)
        content = arg_info['content']
        subject = arg_info['mail']['commonHeaders']['subject']
        html_content = content.partition('Content-Type: text/html; charset=UTF-8')[2]
        if 'Content-Transfer-Encoding' in html_content:
            html_content = html_content.partition('Content-Transfer-Encoding: quoted-printable')[2]
        text = html_content.replace('\r\n', '')
        table = html.fromstring(text)
        content = ''
        for item in table:
            if item.text:
                content += item.text.strip()
        mail_content = str(content)
        from_mail = arg_info['mail']['source']
        to_mail = arg_info['mail']['destination'][0]
        hash_code = arg_info['mail']['destination'][0].split('@')[0]
        return subject, from_mail, to_mail, hash_code, mail_content
