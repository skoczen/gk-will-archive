from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class DeployedPlugin(WillPlugin):

    @route("/api/circleci/deployed/")
    def say_listener(self):
        print self.request
        print self.request.json
        # Options: https://circleci.com/docs/api#build
        assert self.request.json and "payload" in self.request.json
        payload = self.request.json["payload"]
        print payload
        if ["branch"] in payload and payload["branch"] == "master":
            message = "%(project_name)s has been <a href='%(build_url)s'>deployed</a>. (%(subject)s)" % payload
            self.say(message, html=True)

        return "OK"