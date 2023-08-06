from distutils.core import setup

setup(
    name='zhufo_tools',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='常用的函数封装',  # 描述
    author='zhufo44',  # 作者
    py_modules=['zhufo_tools.logger', "zhufo_tools.pymysql", "zhufo_tools.random_ua",
                "zhufo_tools.time_tools"],
)
