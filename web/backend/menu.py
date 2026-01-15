# 菜单配置
MENU_CONF = {
    '我的媒体库': {
        'name': '我的媒体库',
        'level': 1,
        'page': 'index',
        'icon': 'home'
    },
    '探索': {
        'name': '探索',
        'level': 2,
        'list': [
            {'name': '榜单推荐', 'level': 2, 'page': 'ranking', 'icon': 'align_box_bottom_center'},
            {'name': '豆瓣电影', 'level': 2, 'page': 'douban_movie', 'icon': 'movie'},
            {'name': '豆瓣电视剧', 'level': 2, 'page': 'douban_tv', 'icon': 'device_tv'},
            {'name': 'TMDB电影', 'level': 2, 'page': 'tmdb_movie', 'icon': 'movie'},
            {'name': 'TMDB电视剧', 'level': 2, 'page': 'tmdb_tv', 'icon': 'device_tv'},
            {'name': 'BANGUMI', 'level': 2, 'page': 'bangumi', 'icon': 'device_tv_old'}
        ]
    },
    '资源搜索': {
        'name': '资源搜索',
        'level': 2,
        'page': 'search',
        'icon': 'search'
    },
    '站点管理': {
        'name': '站点管理',
        'level': 2,
        'list': [
            {'name': '站点维护', 'level': 2, 'page': 'site', 'icon': 'server_2'},
            {'name': '数据统计', 'level': 2, 'page': 'statistics', 'icon': 'chart_pie'},
            {'name': '刷流任务', 'level': 2, 'page': 'brushtask', 'icon': 'checklist'},
            {'name': '站点资源', 'level': 2, 'page': 'sitelist', 'icon': 'cloud_computing'}
        ]
    },
    '订阅管理': {
        'name': '订阅管理',
        'level': 2,
        'list': [
            {'name': '电影订阅', 'level': 2, 'page': 'movie_rss', 'icon': 'movie'},
            {'name': '电视剧订阅', 'level': 2, 'page': 'tv_rss', 'icon': 'device_tv'},
            {'name': '自定义订阅', 'level': 2, 'page': 'user_rss', 'icon': 'file_rss'},
            {'name': '订阅日历', 'level': 2, 'page': 'rss_calendar', 'icon': 'calendar'}
        ]
    },
    '下载管理': {
        'name': '下载管理',
        'level': 2,
        'list': [
            {'name': '正在下载', 'level': 2, 'page': 'downloading', 'icon': 'loader'},
            {'name': '近期下载', 'level': 2, 'page': 'downloaded', 'icon': 'download'},
            {'name': '自动删种', 'level': 2, 'page': 'torrent_remove', 'icon': 'download_off'}
        ]
    },
    '媒体整理': {
        'name': '媒体整理',
        'level': 1,
        'list': [
            {'name': '文件管理', 'level': 1, 'page': 'mediafile', 'icon': 'file_pencil'},
            {'name': '手动识别', 'level': 1, 'page': 'unidentification', 'icon': 'accessible'},
            {'name': '历史记录', 'level': 1, 'page': 'history', 'icon': 'history'},
            {'name': 'TMDB缓存', 'level': 1, 'page': 'tmdbcache', 'icon': 'brand_headlessui'}
        ]
    },
    '服务': {
        'name': '服务',
        'level': 1,
        'page': 'service',
        'icon': 'layout_2'
    },
    '系统设置': {
        'name': '系统设置',
        'also': '设置',
        'level': 1,
        'list': [
            {'name': '基础设置', 'level': 1, 'page': 'basic', 'icon': 'settings'},
            {'name': '用户管理', 'level': 2, 'page': 'users', 'icon': 'users'},
            {'name': '媒体库', 'level': 1, 'page': 'library', 'icon': 'stereo_glasses'},
            {'name': '目录同步', 'level': 1, 'page': 'directorysync', 'icon': 'refresh'},
            {'name': '消息通知', 'level': 2, 'page': 'notification', 'icon': 'bell'},
            {'name': '过滤规则', 'level': 2, 'page': 'filterrule', 'icon': 'filter'},
            {'name': '自定义识别词', 'level': 1, 'page': 'customwords', 'icon': 'a_b'},
            {'name': '索引器', 'level': 2, 'page': 'indexer', 'icon': 'list_search'},
            {'name': '下载器', 'level': 2, 'page': 'downloader', 'icon': 'download'},
            {'name': '媒体服务器', 'level': 2, 'page': 'mediaserver', 'icon': 'server_cog'},
            {'name': '插件', 'level': 1, 'page': 'plugin', 'icon': 'brand_codesandbox'}
        ]
    }
}

# 服务配置
SERVICE_CONF = {
    'rssdownload': {'name': '电影/电视剧订阅', 'svg': 'cloud_download', 'color': 'blue', 'level': 2},
    'subscribe_search_all': {'name': '订阅搜索', 'svg': 'search', 'color': 'blue', 'level': 2},
    'pttransfer': {'name': '下载文件转移', 'svg': 'replace', 'color': 'green', 'level': 2},
    'sync': {'name': '目录同步', 'time': '实时监控', 'svg': 'refresh', 'color': 'orange', 'level': 1},
    'blacklist': {'name': '清理转移缓存', 'time': '手动', 'state': 'OFF', 'svg': 'eraser', 'color': 'red', 'level': 1},
    'rsshistory': {'name': '清理RSS缓存', 'time': '手动', 'state': 'OFF', 'svg': 'eraser', 'color': 'purple', 'level': 2},
    'nametest': {'name': '名称识别测试', 'time': '', 'state': 'OFF', 'svg': 'alphabet_greek', 'color': 'lime', 'level': 1},
    'ruletest': {'name': '过滤规则测试', 'time': '', 'state': 'OFF', 'svg': 'adjustments_horizontal', 'color': 'yellow', 'level': 2},
    'nettest': {'name': '网络连通性测试', 'time': '', 'state': 'OFF', 'svg': 'network', 'color': 'cyan', 'level': 1},
    'backup': {'name': '备份&恢复', 'time': '', 'state': 'OFF', 'svg': 'backup', 'color': 'green', 'level': 1},
    'processes': {'name': '系统进程', 'time': '', 'state': 'OFF', 'svg': 'terminal_2', 'color': 'muted', 'level': 1}
}


def build_user_menus(user_permissions: list) -> list:
    """
    Build menu list based on user permissions.

    Args:
        user_permissions: List of menu permission strings (e.g., ['我的媒体库', '探索'])

    Returns:
        Filtered list of menu dictionaries that the user has permission to access
    """
    menu_list = []
    for permission in user_permissions:
        if permission in MENU_CONF:
            menu_list.append(MENU_CONF[permission])
    return menu_list
