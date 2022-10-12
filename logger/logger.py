import datetime


class Logger:
    def __init__(self):
        self.start_logger()

    def start_logger(self) -> str:
        """initializing of logger"""
        global current_log
        name = f'/{new_log}.txt'
        path = logs_path + name
        with open(path, 'w') as text:
            text.write(
                f"{new_log} - session started;\n")
        print(f'Logger started. Current log - {name}')
        current_log = path
        return path

    def log(self, *args) -> None:
        """
        record new line to current log file
        :param data: object of action
        :param action: action done with object
        :return: data argument
        """
        with open(current_log, 'a') as text:
            text.write('{0} - {1};'.format(now, args) + '\n')


logs_path = r'logger/logs'
current_log = ''
date = datetime.datetime.now()
now = date.strftime("%d%m%Y_%H%M%S")
new_log = date.strftime("%d%m%Y")
