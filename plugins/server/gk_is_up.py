import requests
import time

from plugins.server.mixins import MailgunMixin
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template

class UptimePlugin(MailgunMixin, WillPlugin):

    def _verify_url(self, url):
        try:
            r = requests.get(url)
            if not r.status_code == 200:
                time.sleep(5)
                r = requests.get(url)
                if not r.status_code == 200:
                    self.say("@all WARNING: %s is down! (%s code)" % (url, r.status_code), color="red")

                if r.status_code == 500:
                    on_fire_list = self.load("on_fire_list", [])
                    self._send_email(
                        "ERROR <errors@scrapbin.com>",
                        on_fire_list,
                        "Website 500 error - %s" % url,
                        "%s is down!" % url
                    )
        except:
            pass

    @periodic(second='5')
    def gk_is_up(self):
        self._verify_url("https://www.greenkahuna.com")

    @periodic(second='5')
    def sb_is_up(self):
        self._verify_url("https://www.scrapbin.com")

    @respond_to("^add (?P<email>.*) to on fire list", multiline=True)
    def add_to_fire_list(self, message, email=""):
        on_fire_list = self.load("on_fire_list", [])
        on_fire_list.append(email)

        self.save("on_fire_list", on_fire_list)
        self.say("Got it, added %s to on fire list" % email, message=message)

    @respond_to("^on fire list", multiline=True)
    def get_fire_list(self, message):
        on_fire_list = self.load("on_fire_list", [])
        fire_list_html = rendered_template("fire_list.html", {"fire_list": on_fire_list})
        self.say(fire_list_html, message=message, html=True)

    @respond_to("^remove (?P<email>.*) from on fire list", multiline=True)
    def remove_from_fire_list(self, message, email=""):
        on_fire_list = self.load("on_fire_list", [])
        on_fire_list.remove(email)

        self.save("on_fire_list", on_fire_list)
        self.say("Got it, removed %s from on fire list" % email, message=message)

    @respond_to("^send test email to on fire list", multiline=True)
    def test_on_fire_emails(self, message):
        on_fire_list = self.load("on_fire_list", [])

        self._send_email(
            "ERROR <errors@scrapbin.com>",
            on_fire_list,
            "Website 500 error -- just kidding!",
            "Everything is fine :)"
        )

        self.say("Sent out the test email", message=message)
