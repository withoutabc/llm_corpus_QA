from server.service.user.login import *
from server.service.user.register import *
from server.service.user.refresh import *


def join_user_routes(app):
    create_login_route(app)
    create_register_route(app)
    create_refresh_route(app)
