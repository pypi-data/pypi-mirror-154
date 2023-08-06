from datetime import datetime

class Logger:
    def __init__(self, logfile='log.txt', interrupt=True):
        if type(logfile) == str:
            self.file = open(logfile, 'a')
        else:
            self.file = logfile
        self.interrupt = interrupt

    def log(self, msg):
        time = datetime.now().strftime('%d-%m-%Y  %H:%M:%S:%f')
        print(f'{time}\t{msg}', file=self.file)  
        
    def run(self, function, parameters=(), secret=False):
        if not secret:
            self.log(f'executing {function} with parameters: {parameters}')
        else:
            self.log(f'executing {function}')
        try:
            result = function(*parameters)
            self.log(f'concluded {function}')
            return result
        except Exception as e:
            self.log(f'Error: {e}')
            if self.interrupt:
                exit()
            else:
                return None

