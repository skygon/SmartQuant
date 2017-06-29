
class Utils(object):
    def __init__(self):
        pass
    
    @staticmethod
    def save2CSVFile(df, full_path, enc='utf-8'):
        df.to_csv(full_path, encoding=enc)