import logging.config
import os
from datetime import datetime
from logging import Logger

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s][line:%(lineno)d]:%(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
        },
        # "time": {
        #     "class": "logging.handlers.TimedRotatingFileHandler",
        #     "level": "DEBUG",
        #     "encoding": "utf8",
        #     "filename": f"./log/{datetime.now().strftime('%Y%m%d')}/app.log",
        #     "formatter": "default",
        # },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "encoding": "utf8",
            "filename": f"./log/{datetime.now().strftime('%Y%m%d')}/app.log",
            "formatter": "default",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10
        },
        "mail": {
            "class": "logging.handlers.SMTPHandler",
            "level": "ERROR",
            "mailhost": ("smtp.qq.com"),
            "subject": '【自动化辅助工具】日志通知',
            "fromaddr": "84845615@qq.com",
            "toaddrs": "314666979@qq.com",
            "credentials": ("84845615@qq.com", "enyjdbtxxzqabjih"),
            "formatter": "default",
        },
    },
    "loggers": {
        "console_logger": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "file_logger": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "mail_logger": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            # 是否继续打印更高等级的日志
            "propagate": False,
        }
    },
    "disable_existing_loggers": False,
}


# def my_log(log_path=".", app="mail_logger"):
#     if not os.path.exists(f"{log_path}/log/{datetime.now().strftime('%Y%m%d')}/"):
#         os.makedirs(f"{log_path}/log/{datetime.now().strftime('%Y%m%d')}/")
#     logging.config.dictConfig(LOGGING_CONFIG)
#     log = logging.getLogger(app)
#     return log
#
#
# # log = my_log(log_path=".", app="mail_logger")


class Log(Logger):
    def __init__(self, log_root_dir=".", app="mail_logger"):
        self.log_path = f"{log_root_dir}/{datetime.now().strftime('%Y%m%d')}/"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        LOGGING_CONFIG["handlers"]["file"]["filename"] = os.path.join(self.log_path, "app.log")
        logging.config.dictConfig(LOGGING_CONFIG)
        self.log = logging.getLogger(app)



if __name__ == "__main__":
    log2 = Log(r"D:\workspace\ruirenyunlibrary\RuirenyunLibrary\log2").log
    for x in range(0, 1):
        log2.setLevel(logging.NOTSET)
        log2.debug(f"Hello log11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111你好：{x}!")
        log2.info(f"Hello log11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111你好：{x}!")
        log2.warning(f"Hello log11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111你好：{x}!")
        log2.error(f"Hello log11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111你好：{x}!")
