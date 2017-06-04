
from tornado.gen import coroutine, Return

from common.model import Model
from common.validate import validate
from common.deployment import DeploymentError, DeploymentMethods

from settings import NoSuchSettingsError, SettingsError

import os


class DeploymentModel(Model):
    def __init__(self, settings):
        self.settings = settings

    @coroutine
    @validate(gamespace_id="int", account_id="int", file_path="str", file_name="str")
    def deploy(self, gamespace_id, account_id, file_path, file_name):

        try:
            settings = yield self.settings.get_settings(gamespace_id)
        except NoSuchSettingsError:
            raise DeploymentError("Please select deployment method first (in settings)")
        except SettingsError as e:
            raise DeploymentError(e.message)

        m = DeploymentMethods.get(settings.deployment_method)()
        m.load(settings.deployment_data)

        url = yield m.deploy(gamespace_id, file_path, str(account_id), file_name)

        raise Return(url)
