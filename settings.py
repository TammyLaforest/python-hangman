import os
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG= True
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


# class MyFlask(flask.Flask):
#     @property
#     def static_folder(self):
#         if self.config.get('STATIC_FOLDER') is not None:
#             return os.path.join(self.root_path, 
#                 self.config.get('STATIC_FOLDER'))
#     @static_folder.setter
#     def static_folder(self, value):
#         self.config.get('STATIC_FOLDER') = value


