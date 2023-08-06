from .xls import xls
from datetime import date
import pandas as pd

class record(xls):
    file_path = ''
    def __init__(self, code, record_type):
        record.file_path = xls.root_folder + '/record/record.xlsx'
        super().__init__(code = code, sheet = record_type, sheet_type = record_type, file_type='record', file_path = record.file_path)
    
    @staticmethod
    def search(sheet):
        xls.search(sheet, 'record type', sheet, 'record', 'file', record.file_path)