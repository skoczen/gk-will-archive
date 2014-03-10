"""
Add people to list with their "personal zoom" urls seen on the profile page after login
When someone requests @will zoom, it grabs their personal url (if it exists)
They have to join the zoom first before others can

Levi's zoom room: https://zoom.us/j/5760057307

@will my zoom is https://zoom.us/j/5760057307
@will what is my zoom
@will zoom
"""
import requests
import time

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template

class ZoomPlugin(WillPlugin):

    @respond_to("^set my zoom url to (?P<zoom_url>.*)", multiline=True)
    def set_my_info(self, message, zoom_url=""):
        zoom_urls = self.load("zoom_urls", {})
        zoom_urls[message.sender.nick] = {
            "zoom_url": zoom_url,
            "name": message.sender.name,
            }
        self.save("zoom_urls", zoom_urls)
        self.say("Got it.", message=message)

    @respond_to("^zoom", multiline=True)
    def zoom(self, message):
        zoom_urls = self.load("zoom_urls", {})
        zoom_url = zoom_urls.get(message.sender.nick, None)

        if zoom_url:
            self.say("Join %s" % zoom_url["zoom_url"], message=message)
        else:
            self.say(
                "You need to set your zoom url first, you can find it on your zoom.us/profile page!",
                message=message
            )
