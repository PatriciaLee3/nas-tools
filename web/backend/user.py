from flask_login import UserMixin
from werkzeug.security import check_password_hash
from app.helper import DbHelper
from config import Config
from typing import Optional, List, Dict, Any

# 管理员默认权限
ADMIN_PRIS = "我的媒体库,资源搜索,探索,站点管理,订阅管理,下载管理,媒体整理,服务,系统设置"


class User(UserMixin):
    """
    用户类
    """

    id: int
    admin: int
    username: str
    password_hash: Optional[str]
    pris: str
    level: int
    search: int

    def __init__(self, user_id: Optional[int], admin: int, username: Optional[str],
                 password_hash: Optional[str], pris: str, level: int, search: int) -> None:
        """初始化用户对象"""
        self.id = user_id if user_id is not None else 0
        self.admin = admin
        self.username = username if username is not None else ""
        self.password_hash = password_hash
        self.pris = pris
        self.level = level
        self.search = search

    @property
    def menu_permissions(self) -> List[str]:
        """
        Get user menu permissions as a list.
        :return: List of permission strings
        """
        return [p.strip() for p in self.pris.split(",")] if self.pris else []

    def verify_password(self, password: str) -> bool:
        """
        验证密码是否正确
        :param password: 明文密码
        :return: True/False
        """
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        """
        Flask-Login 要求的方法: 返回用户ID
        :return: 用户ID字符串
        """
        return str(self.id)

    @staticmethod
    def _get_admin_user_from_config() -> Optional['User']:
        """
        从配置文件获取管理员用户
        :return: 管理员User对象
        """
        config = Config().get_config('app')
        if not config:
            return None

        login_password = config.get('login_password', '')
        # 去除 [hash] 前缀
        if login_password and login_password.startswith('[hash]'):
            login_password = login_password[6:]

        return User(
            user_id=0,
            admin=1,
            username=config.get('login_user', 'admin'),
            password_hash=login_password,
            pris=ADMIN_PRIS,
            level=1,
            search=1
        )

    @staticmethod
    def get_user(username: Optional[str]) -> Optional['User']:
        """
        根据用户名获取用户对象
        :param username: 用户名
        :return: User对象或None
        """
        if not username:
            return None

        # 先检查配置文件中的管理员用户
        config = Config().get_config('app')
        if config:
            config_user = config.get('login_user')
            if config_user == username:
                return User._get_admin_user_from_config()

        # 查询数据库用户
        user = DbHelper().get_users(name=username)
        if user:
            return User(
                user_id=user.ID,
                admin=0,
                username=user.NAME,
                password_hash=user.PASSWORD,
                pris=user.PRIS if user.PRIS else "",
                level=1,
                search=1
            )
        return None

    @staticmethod
    def get(user_id: Optional[str]) -> Optional['User']:
        """
        根据用户ID获取用户对象(Flask-Login 回调）
        :param user_id: 用户ID
        :return: User对象或None
        """
        if user_id is None:
            return None

        # ID 为 0 表示配置文件中的管理员
        # 注意: Flask-Login传递的user_id是字符串类型
        if int(user_id) == 0:
            return User._get_admin_user_from_config()

        # 查询数据库用户
        user = DbHelper().get_users(uid=int(user_id))
        if user:
            return User(
                user_id=user.ID,
                admin=0,
                username=user.NAME,
                password_hash=user.PASSWORD,
                pris=user.PRIS if user.PRIS else "",
                level=2,
                search=1
            )
        return None

    @staticmethod
    def get_users() -> List[Any]:
        """
        获取所有用户
        :return: 用户列表
        """
        return DbHelper().get_users()

    @staticmethod
    def add_user(name: str, password: str, pris: str) -> bool:
        """
        添加用户
        :param name: 用户名
        :param password: 密码（已哈希）
        :param pris: 权限（逗号分隔的字符串）
        :return: True/False
        """
        if not name or not password:
            return False

        # 检查用户是否已存在
        if DbHelper().is_user_exists(name):
            return False

        # 添加用户
        DbHelper().insert_user(name, password, pris)
        return True

    @staticmethod
    def delete_user(name: str) -> bool:
        """
        删除用户
        :param name: 用户名
        :return: True/False
        """
        if not name:
            return False

        # 检查用户是否存在
        if not DbHelper().is_user_exists(name):
            return False

        # 删除用户
        DbHelper().delete_user(name)
        return True

    @staticmethod
    def check_user(site: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        检查用户权限（占位方法，返回True）
        :param site: 站点
        :param params: 参数
        :return: True
        """
        return True
