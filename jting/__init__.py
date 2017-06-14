# coding: utf-8

"""
                     _ooOoo_
                    o8888888o
                    88" . "88
                    (| -_- |)
                     O\ = /O
                 ____/`---'\____
               .   ' \\| |// `.
                / \\||| : |||// \
              / _||||| -:- |||||- \
                | | \\\ - /// | |
              | \_| ''\---/'' |_/  |
               \ .-\__ `-` ___/-. /
            ___`. .' /--.--\ `. . __
         ."" '< `.___\_<|>_/___.' >'"".
        | | : `- \`.;`\ _ /`;.`/ - ` : | |
          \ \ `-. \_ __\ /__ _/ .-` / /
  ======`-.____`-.___\_____/___.-`____.-'======
                     `=---='

  .............................................
           佛祖保佑             永无BUG
"""


def register_app_blueprints(app):
    from jting.api import init_app
    init_app(app)


def register_not_found(app):
    from jting.libs.errors import NotFound

    @app.errorhandler(404)
    def handle_not_found(e):
        return NotFound('URL')


def create_app(config=None):
    from .app import create_app
    app = create_app(config)
    register_app_blueprints(app)
    return app
