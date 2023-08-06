from .xls import xls


from datetime import date
import pandas as pd

from IPython.display import HTML, Latex, display, clear_output
import ipywidgets as widgets

class reference(xls):
    method = ''
    file_path = ''
    def __init__(self, material, method):
        # set temperary code as 'tmp'
        reference.method = method
        reference.file_path = xls.root_folder + "/reference/" + method + ".xlsx"
        
        super().__init__(code = 'tmp', sheet = material, sheet_type = 'reference', file_type = method, file_path = reference.file_path)
        
        self.record['code'] = self.records_on_sheet.shape[0] + 1
        print("A new code has been generated: r.record['code'] = " + str(self.record['code']))
    
    @staticmethod
    def search():
        material = 'MoS2'
        method = 'raman'
        xls.search(material, 'material', 'reference', method, 'method', xls.root_folder + "/reference/" + method + ".xlsx")
    
    def get_peak(self, code):
        data = self.records_on_sheet[self.records_on_sheet['code'] == code]
        display(data)
        data = data.iloc[0]
        return {'label': data['label'], 'cen': float(data['cen']), 'wid': float(data['wid']), 'amp': float(data['amp'])}

        

         