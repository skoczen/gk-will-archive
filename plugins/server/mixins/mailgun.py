import requests

from will import settings

class MailgunMixin(object):

    # Sends an email from errors@greenkahuna to everyone in the specified email list.
    #
    # from_email - Who the email is from
    # email_list - A list of emails to.. email!
    # subject - The subject of the message
    # message - The body of the message to send
    #
    # Example:
    #     r = requests.get(url)
    #
    #     if r.status_code == 500:
    #         self._send_email(
    #             "ERROR! <errors@greenkahuna.com>",
    #             ["helper@scrapbin.com"],
    #             "Website 500 error - %s" % url,
    #             "%s is down!" % url
    #         )
    #
    # Returns nothing
    def _send_email(self, from_email, email_list, subject, message):
        resp = requests.post(
            "https://api.mailgun.net/v2/scrapbin.com/messages",
            auth=("api", settings.WILL_MAILGUN_API_KEY),
            data={
                "from": from_email,
                "to": email_list,
                "subject": "Website 500 error",
                "text": message
            }
        )
