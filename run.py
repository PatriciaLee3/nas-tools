import os
import signal
import sys
import warnings

warnings.filterwarnings('ignore')

from config import Config
import log
from web.action import WebAction
from web.main import App
from app.db import init_db, update_db, init_data
from app.helper import init_chrome
from initializer import update_config, check_config,  start_config_monitor, stop_config_monitor
from version import APP_VERSION


def sigal_handler(num, stack):
    """
    信号处理
    """
    log.warn('捕捉到退出信号：%s，开始退出...' % num)
    # 关闭配置文件监控
    log.info('关闭配置文件监控...')
    stop_config_monitor()
    # 关闭服务
    log.info('关闭服务...')
    WebAction.stop_service()
    # 退出主进程
    log.info('退出主进程...')
    # sys.exit(0) -> os._exit(0)
    # fix s6下python进程无法退出的问题
    os._exit(0)


def get_run_config():
    """
    获取运行配置
    """
    _web_host = "::"
    _web_port = 3000
    _ssl_cert = None
    _ssl_key = None
    _debug = False

    app_conf = Config().get_config('app')
    if app_conf:
        if app_conf.get("web_host"):
            _web_host = app_conf.get("web_host").replace('[', '').replace(']', '')
        _web_port = int(app_conf.get('web_port')) if str(app_conf.get('web_port', '')).isdigit() else 3000
        _ssl_cert = app_conf.get('ssl_cert')
        _ssl_key = app_conf.get('ssl_key')
        _ssl_key = app_conf.get('ssl_key')
        _debug = True if app_conf.get("debug") else False

    app_arg = dict(host=_web_host, port=_web_port, debug=_debug, threaded=True, use_reloader=False)
    if _ssl_cert:
        app_arg['ssl_context'] = (_ssl_cert, _ssl_key)
    return app_arg


# 退出事件
signal.signal(signal.SIGINT, sigal_handler)
signal.signal(signal.SIGTERM, sigal_handler)


def init_system():
    # 配置
    log.console('NAStool 当前版本号：%s' % APP_VERSION)
    # 数据库初始化
    init_db()
    # 数据库更新
    update_db()
    # 数据初始化
    init_data()
    # 升级配置文件
    update_config()
    # 检查配置文件
    check_config()


def start_service():
    log.console("开始启动服务...")
    # 启动服务
    WebAction.start_service()
    # 用户认证
    WebAction.auth_user_level()
    # 监听配置文件变化
    start_config_monitor()


# 系统初始化
init_system()

# 启动服务
start_service()


# 本地运行
if __name__ == '__main__':
    # 初始化浏览器驱动
    init_chrome()

    # Flask启动
    App.run(**get_run_config())
