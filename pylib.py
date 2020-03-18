import logging
import pkgutil
import coloredlogs
import importlib

def initlog(logger=None,use_color=True):
    """
    :param logger: 记录器logging.getLogger("记录器名称")创建
    :type logger:object
    :param use_color: 是否在控制台中显示
    :type use_color:bool
    """
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logpath = r"./log.txt"
    if(use_color):
        """此方法仅在控制台输出"""
        coloredlogs.install(logger=logger,fmt=fmt, datefmt=datefmt)
    """basicConfig是默认配置，配置文件存放记录器位置，输出格式"""
    logging.basicConfig(filename=logpath, format=fmt, datefmt=datefmt)

# 加载模块下所有的子模块
def load_plugins(namespace):
    """
    :param namespace:命名空间，与import plugins,调用返回值plugins.baseexcept(所要模块__name__).相应的类或方法
    :type namespace: Any
    :return:
    """
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules(namespace.__path__, namespace.__name__ + '.')
    }
