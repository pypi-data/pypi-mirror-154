# _*_ coding: utf-8 _*_
import inspect
import logging
import os.path
import re
import time


class mylog(object):

    def __init__(self, logger='my_log', log_path=None, log_level=None, file_log_level=None, stream_log_level=None):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
               log_path：日志路径，默认为空，将保存至当前项目
               file_log_level：日志文件日志级别
               stream_log_level：控制台日志级别
        """
        self.__log_level = log_level
        self.__file_log_level = file_log_level
        self.__stream_log_level = stream_log_level

        # 初始化，不指定日志级别，默认为Debug,此时，会打印出debug级别及以上的全部日志，并保存至日期-debug文件中
        '''
        日志一共分成5个等级，从低到高分别是：
            DEBUG
            INFO
            WARNING
            ERROR
            CRITICAL
        '''
        if self.__log_level is None:
            self.__log_level = logging.DEBUG
        if self.__file_log_level is None:
            self.__file_log_level = self.__log_level
        if self.__stream_log_level is None:
            self.__stream_log_level = self.__log_level

        # 创建一个logger
        self.__logger = logging.getLogger(logger)
        self.__logger.setLevel(self.__log_level)
        # 设置日志路径
        self.__log_path = log_path

        # 如果不存在已经设置日志路径
        if self.__log_path is None:
            # os.getcwd()获取当前文件的路径，
            path_dir = os.path.dirname(__file__) + '/log'
            # 如果该项目下没有log目录，创建log目录
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            # os.path.dirname()获取指定文件路径的上级路径
            log_path = os.path.abspath(os.path.dirname(path_dir)) + '/log'
        else:
            # 否则，设置了路径就使用用户设置的路径
            path_dir = self.__log_path
            # 最后为目录，不存在则创建
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

        # 创建日志名称。
        rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 拼接日志文件路径名称
        log_name = os.path.join(path_dir, rq + '-' + 'ALL' + '.log')
        info_log_name = os.path.join(path_dir, rq + '-' + str(logging.getLevelName(logging.INFO)) + '.log')
        error_log_name = os.path.join(path_dir, rq + '-' + str(logging.getLevelName(logging.ERROR)) + '.log')
        debug_log_name = os.path.join(path_dir, rq + '-' + str(logging.getLevelName(logging.DEBUG)) + '.log')

        # 创建一个通用的handler，用于写入日志文件，写入所有的日志级别
        fh = logging.FileHandler(log_name, encoding='utf-8')
        fh.setLevel(self.__file_log_level)
        # 创建一个info_handler，用于写入INFO日志文件，只写入info级别及以上的日志
        info_fh = logging.FileHandler(info_log_name, encoding='utf-8')
        info_fh.setLevel(logging.INFO)
        # 创建一个error_handler，用于写入ERROR日志文件，只写入error级别及以上的日志
        error_fh = logging.FileHandler(error_log_name, encoding='utf-8')
        error_fh.setLevel(logging.ERROR)
        # 创建一个debug_handler，用于写入DEBUG日志文件，写入debug级别及以上的日志
        debug_fh = logging.FileHandler(debug_log_name, encoding='utf-8')
        debug_fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(self.__stream_log_level)

        # 定义handler的输出格式  #日志输出的格式
        '''
        logging.basicConfig函数中，可以指定日志的输出格式format，这个参数可以输出很多有用的信息，如下:
            %(levelno)s: 打印日志级别的数值
            %(levelname)s: 打印日志级别名称
            %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
            %(filename)s: 打印当前执行程序名
            %(funcName)s: 打印日志的当前函数,如果在main方法调用，会输出<moudle>
            %(lineno)d: 打印日志的当前行号
            %(asctime)s: 打印日志的时间
            %(thread)d: 打印线程ID
            %(threadName)s: 打印线程名称
            %(process)d: 打印进程ID
            %(message)s: 打印日志信息
        '''
        format_str = 'time:%(asctime)s -log_name:%(name)s -level:%(levelname)-s -file_name:%(filename)-8s -fun_name:%(funcName)s - %(lineno)d line -message: %(message)s'
        formatter = logging.Formatter(format_str)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        info_fh.setFormatter(formatter)
        error_fh.setFormatter(formatter)
        debug_fh.setFormatter(formatter)
        # 避免重复日志
        if not self.__logger.handlers:
            # 给logger添加handler
            self.__logger.addHandler(fh)
            self.__logger.addHandler(ch)
            self.__logger.addHandler(info_fh)
            self.__logger.addHandler(error_fh)
            self.__logger.addHandler(debug_fh)

    def get_logger(self):
        return self.__logger

    @staticmethod
    def __get_file_name_in_full_path(file_path):
        return file_path.split('/')[-1]

    # 以下方法来源于https://github.com/frankyaorenjie/Python-CLog
    def get_meta_data(self):
        frames = inspect.stack()
        chain_list = []
        for i in range(0, len(frames)):
            _, file_path, _, func_name, _, _ = frames[i]
            file_name = self.__get_file_name_in_full_path(file_path)
            try:
                args = re.findall('\((.*)\)', frames[i + 1][-2][0])[0]
            except IndexError as e:
                func_result = self.__get_class_from_frame(frames[2][0])
                if func_result is None:
                    func_name = ''
                    args = ''
                else:
                    func_name = self.__get_class_from_frame(frames[2][0]).__name__
                    args = ''
            current_chain = '%s:%s(%s)' % (file_name, func_name, args)
            chain_list.append(current_chain)
        chain_list.reverse()
        return ' --> '.join(chain_list[:-2])

    @staticmethod
    def __get_class_from_frame(fr):
        args, _, _, value_dict = inspect.getargvalues(fr)
        if len(args) and args[0] == 'self':
            instance = value_dict.get('self', None)
            if instance:
                return getattr(instance, '__class__', None)
        return None


__self_my_log = mylog(logger='self_my_log')

__myLogger = None


def get_log(logger='my_log', log_path=None, log_level=None, file_log_level=None, stream_log_level=None):
    global __self_my_log
    __self_my_log = mylog(logger, log_path, log_level, file_log_level, stream_log_level)
    return __self_my_log


def getLogger(logger='my_log', log_path=None, log_level=None, file_log_level=None, stream_log_level=None):
    global __self_my_log
    __self_my_log = get_log(logger, log_path, log_level, file_log_level, stream_log_level)
    global __myLogger

    if __self_my_log is None:
        raise Exception('The global self_my_log is none,please set self_my_log')

    __myLogger = __self_my_log.get_logger()
    return __myLogger


def get_chain():
    global __self_my_log
    if __self_my_log is None:
        return None
    else:
        my_chain = __self_my_log.get_meta_data()
        return my_chain


def log_info(message, my_logger=None):
    if my_logger is None:
        my_logger = my_logger

    my_logger.info(message, extra={'chain': get_chain()})


def log_error(message, my_logger=None):
    if my_logger is None:
        my_logger = my_logger

    my_logger.error(message, extra={'chain': get_chain()})


if __name__ == '__main__':
    test_looger = getLogger(logger='test', log_level=logging.INFO)
    log_info('testacasca', my_logger=test_looger)

# error_log = mylog(logger='error').get_logger()

# error_log.error('错误日志测试')  #

# debug_log = mylog(logger='debug').get_logger()

# debug_log.debug('debug')
