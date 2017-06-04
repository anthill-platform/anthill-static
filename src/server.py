
from tornado.gen import coroutine
from common.options import options

import common.server
import common.handler
import common.database
import common.access
import common.sign
import common.ratelimit

from model.deploy import DeploymentModel
from model.settings import SettingsModel

import handler
import admin
import options as _opts


class StaticServer(common.server.Server):
    def __init__(self):
        super(StaticServer, self).__init__()

        self.db = common.database.Database(
            host=options.db_host,
            database=options.db_name,
            user=options.db_username,
            password=options.db_password)

        self.deployment_settings = SettingsModel(self.db)
        self.deployment = DeploymentModel(self.deployment_settings)

        self.ratelimit = common.ratelimit.RateLimit({
            "file_upload": options.rate_file_upload
        })

    def get_models(self):
        return [self.deployment_settings, self.deployment]

    def get_admin(self):
        return {
            "index": admin.RootAdminController,
            "settings": admin.SettingsController
        }

    def get_metadata(self):
        return {
            "title": "Static",
            "description": "Static file hosting service for players to upload",
            "icon": "file-text-o"
        }

    def get_handlers(self):
        return [
            (r"/upload", handler.UploadFileHandler),
        ]

if __name__ == "__main__":
    stt = common.server.init()
    common.access.AccessToken.init([common.access.public()])
    common.server.start(StaticServer)
