
from tornado.gen import coroutine, Return

from common.model import Model
from common.database import DatabaseError
from common.validate import validate

import ujson


class SettingsError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NoSuchSettingsError(Exception):
    pass


class SettingsAdapter(object):
    def __init__(self, data):
        self.gamespace_id = data.get("gamespace_id")
        self.deployment_method = data.get("deployment_method")
        self.deployment_data = data.get("deployment_data")


class SettingsModel(Model):
    def __init__(self, db):
        self.db = db

    def get_setup_db(self):
        return self.db

    def get_setup_tables(self):
        return ["settings"]

    @coroutine
    @validate(gamespace_id="int")
    def delete_settings(self, gamespace_id):
        try:
            yield self.db.execute(
                """
                DELETE FROM `settings`
                WHERE `gamespace_id`=%s;
                """, gamespace_id)
        except DatabaseError as e:
            raise SettingsError("Failed to delete settings: " + e.args[1])

    @coroutine
    @validate(gamespace_id="int")
    def get_settings(self, gamespace_id):
        try:
            settings = yield self.db.get(
                """
                SELECT *
                FROM `settings`
                WHERE `gamespace_id`=%s
                LIMIT 1;
                """, gamespace_id)
        except DatabaseError as e:
            raise SettingsError("Failed to get settings: " + e.args[1])

        if not settings:
            raise NoSuchSettingsError()

        raise Return(SettingsAdapter(settings))

    @coroutine
    @validate(gamespace_id="int", deployment_method="str_name", deployment_data="json_dict")
    def update_settings(self, gamespace_id, deployment_method, deployment_data):

        deployment_data = ujson.dumps(deployment_data)

        try:
            yield self.db.insert(
                """
                INSERT INTO `settings`
                (`deployment_method`, `deployment_data`, `gamespace_id`)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY
                UPDATE `deployment_method`=%s, `deployment_data`=%s;
                """, deployment_method, deployment_data, gamespace_id, deployment_method, deployment_data)
        except DatabaseError as e:
            raise SettingsError("Failed to update settings: " + e.args[1])
