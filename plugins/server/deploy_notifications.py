from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class DeployedPlugin(WillPlugin):

    @route("/api/circleci/deployed/", method="POST")
    def say_listener(self):
        # Options: https://circleci.com/docs/api#build
        assert self.request.json and "payload" in self.request.json
        payload = self.request.json["payload"]
        if "branch" in payload and payload["branch"] == "master":
            payload["project_name"] = payload["reponame"].title()
            message = "%(project_name)s has been <a href='%(build_url)s'>deployed</a>. <i>%(subject)s</i>" % payload
            self.say(message, html=True)

        return "OK"