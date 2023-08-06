from importlib import resources
import io
import os
import numpy as np
import pandas as pd
from datetime import date

from IPython.display import HTML, Latex, display, clear_output
import ipywidgets as widgets

class xls():
    researcher = ''
    root_folder = ''
    setup_file = ''
    record_selected = pd.DataFrame()
    tmp_selected = pd.DataFrame()
    
    def __init__(self, code, sheet, sheet_type, file_type, file_path):
        # Create the file name in the TEAM Project folder
        if xls.root_folder == '':
            print('Warning: please set the full path of the TEAM/Projects folder: record.root_folder = your_folder_path')
            return None
        xls.setup_file = xls.root_folder + '/record/.utilities/setup.xlsx' # full_path for the setup file, which contains the fields
        self.file_path = file_path # The full path of the xls file that stores the information
        self.file_type = file_type # The type of the xlsx file: record, project, member, ...
        self.sheet = sheet # The sheet name of the instance
        self.sheet_type = sheet_type # The sheet type: e.g. "generic" - all sheets in the xlxs has the same fields
        
        # Initiate the records
        self.fields, self.record = self.init_records(code)  #self.record is the record of this instance (i.e. one row in the sheet)
        # Read the record from the spreadsheet
        self.records_on_sheet, self.record = self.get_records()
        # Set the modified status
        self.record['modifiedby'] = self.researcher
        self.record['modifiedon'] = date.today().strftime("%d/%m/%Y")

    def __repr__(self):
        return "\033[1mcode\033[0m={}, \033[1msheet\033[0m={}, \033[1msheet type\033[0m={}, \033[1mfile type\033[0m={}\n\033[1mfile path\033[0m={}.".format(self.record['code'], self.sheet, self.sheet_type, self.file_type, self.file_path)

    @staticmethod
    def get_fields(file_type, sheet_type):
        # Get the fields of the spreadsheet from /record/.utilities/setup.xlsx
        with resources.open_binary('zhangTCD', 'setup.xlsx') as fp:
            file = fp.read()
        io.BytesIO(file)
        try:
            setup = pd.read_excel(io.BytesIO(file), engine='openpyxl', names=["file_type", "sheet_type", "fields"]) # setup reads in all the fields in the setup.xlsx file
            this = setup[(setup['file_type']==file_type) & (setup['sheet_type']==sheet_type)] # this extract the record that is specified for the instance
            fields = this['fields'].to_list()[0].replace(" ", "") # Convert to list and remove space from the records 
            fields = ['code'] + ([] if fields == 'As_defined' else fields.split(","))+ ['modifiedby','modifiedon'] # add three universial fields: code, modifiedby, modifiedon
            return fields
        except:
            print('Check your inputs. No field can be extracted from the setup.xlsx.')
            return []
    
    @staticmethod
    def list_records(sheet, sheet_type, file_type, file):
        fields = xls.get_fields(file_type, sheet_type)
        if len(fields) == 0:
            return pd.DataFrame()
        try:
            record_on_sheet = pd.read_excel(file, engine='openpyxl', sheet_name=sheet, names = fields)
            return record_on_sheet
        except:
            print("No record found.")
            return pd.DataFrame()
    
    @staticmethod
    def search(sheet, sheet_name, sheet_type, file_type, file_type_name, file_path):
        fields = xls.get_fields(file_type, sheet_type)
        if len(fields) == 0:
            print('Check file_type and sheet_type (setup.xlsx)')
            return False

        txt_sheet = widgets.Text(value=sheet, placeholder='sheet', description=sheet_name,
                                 disabled=False, continuous_update=True, orientation='horizontal',readout=True, readout_format='.1f',
                                 style = {'description_width': 'initial'}, layout=widgets.Layout(width='90%', height='100%'))
        txt_file_type = widgets.Text(value=file_type, placeholder='file type name', description=file_type_name,
                                 disabled=False, continuous_update=True, orientation='horizontal',readout=True, readout_format='.1f',
                                 style = {'description_width': 'initial'}, layout=widgets.Layout(width='90%', height='100%'))
        dp_c=[]
        txt_c=[]
        num_c = 3
        for i in range(num_c):
            dp_c.append(widgets.Dropdown(placeholder='criterion ' + str(i),options=fields, value=fields[0],
                                       description='criterion ' + str(i) + ':',
                                       disabled=False, continuous_update=True, orientation='horizontal',readout=True, readout_format='.1f',
                                       style = {'description_width': 'initial'}, layout=widgets.Layout(width='100%', height='90%')))
            txt_c.append(widgets.Text(value=None, placeholder='', description=' ',
                                 disabled=False, continuous_update=True, orientation='horizontal',readout=True, readout_format='.1f',
                                 style = {'description_width': 'initial'}, layout=widgets.Layout(width='100%', height='100%')))
        btn_select = widgets.Button(description='select record', disabled=False, button_style='', tooltip='Click me', layout=widgets.Layout(width='60%', height='80%'))
            
        controls = widgets.interactive(xls.found, sheet=txt_sheet, sheet_type=sheet_type, file_type=txt_file_type, file =file_path,
                                       dc0=dp_c[0], c0 = txt_c[0], dc1=dp_c[1], c1 = txt_c[1],
                                       dc2=dp_c[2], c2 = txt_c[2]);
        
        output = controls.children[-1]
        grid =  widgets.GridspecLayout(2+num_c, 5)
        grid[0, :1]=txt_sheet
        grid[0, 1:2]=txt_file_type
        grid[0, 2]=btn_select
        for i in range(num_c):
            grid[i+1, :1] = dp_c[i]
            grid[i+1, 1:2] = txt_c[i]
        
        display(grid)
        display(widgets.VBox([output]))
        def on_btn_clicked_select(b):
            clear_output(wait=True)
            with output:
                if len(xls.tmp_selected.index) ==1:
                    xls.record_selected = xls.tmp_selected
                    print("record selected (.record_selected).")
                else:
                    print("Please select 1 record.")
        btn_select.on_click(on_btn_clicked_select)
    
    @staticmethod
    def found(sheet, sheet_type, file_type, file, dc0, c0, dc1, c1, dc2, c2):
        xls.tmp_selected = xls.list_records(sheet=sheet, sheet_type=sheet_type, file_type=file_type, file=file)
        if len(xls.tmp_selected.index) !=0:
            records = xls.tmp_selected.applymap(str)
            c = [c0, c1, c2]
            dc = [dc0, dc1, dc2]
            for i in range(len(c)):
                if len(c[i]) !=0:
                    records = records[records[dc[i]].isin([c[i]])]
            if len(records.index) != 0:
                display(HTML(records.to_html(index=False)))  
                xls.tmp_selected = records
            else:
                print("no record is found.")
                xls.tmp_selected = pd.DataFrame()
        else:
            print("no record is found.")
            xls.tmp_selected = pd.DataFrame()
            
    # Initiate the fields and records
    def init_records(self, code):
        # Get the fields of the spreadsheet from /record/.utilities/setup.xlsx
        fields = xls.get_fields(self.file_type, self.sheet_type)
        
        # initilise the values for each field and convert it into a dictionary
        values = [None] * len(fields)        
        record = dict(zip(fields, values))
        record['code'] = code
        return fields, record
    
    # Show current record, not saved yet
    def current(self):
        display(pd.DataFrame(self.record, index=[0]))

    # Get sheet from the file
    def get_records(self):
        try:
            record_on_sheet = pd.read_excel(self.file_path, engine='openpyxl', sheet_name=self.sheet, names = self.fields)
            if self.record['code'] in record_on_sheet.code.tolist():
                # Get the record from the file, and update self.record
                return record_on_sheet, record_on_sheet.loc[record_on_sheet['code'] == self.record['code']].to_dict('records')[0] # Convert the record into dict
            else:
                #print(record['code'])
                #print(record['code'] + " is a new record.")
                return record_on_sheet, self.record
        except:
            #print("This is a new record and I cannot find the datafile")
            return pd.DataFrame(self.record, index=[0]), self.record # No file can be found and/or no record on the sheet, create the sheet record

    def create(self):
        newdata = pd.DataFrame(self.record, index =[0]); 
        # Read the record from the spreadsheet
        try:
            self.records_on_sheet = pd.read_excel(self.file_path, engine='openpyxl', sheet_name=self.sheet, names = self.fields)
            if self.record['code'] in self.records_on_sheet.code.tolist():
                print("A record with the same code is on record. Please choose a new code if you wish to create a new record.")
                return False
            else:
                pass
        except:
            self.records_on_sheet = newdata
        self.save()
        
    def save(self):
        newdata = pd.DataFrame(self.record, index =[0]); 
        # Read the record from the spreadsheet
        try:
            self.records_on_sheet = pd.read_excel(self.file_path, engine='openpyxl', sheet_name=self.sheet, names = self.fields)
        except:
            self.records_on_sheet = newdata    
        
        self.records_on_sheet = pd.concat([self.records_on_sheet, newdata]).drop_duplicates(['code'], keep='last') #.sort_values(self.record['start'][0])
        self.records_on_sheet.reset_index(drop=True)
        
        try:
            writer = pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace' )
        except:
            writer = pd.ExcelWriter(self.file_path)
        self.records_on_sheet.to_excel(writer, sheet_name=self.sheet, index=False)
        writer.save()
        print("We have saved the record: ")
        display(HTML(newdata.to_html(index=False)))
    
    def delete(self):
        # Read the record from the spreadsheet
        self.records_on_sheet, self.record = self.get_records()
        
        self.records_on_sheet = self.records_on_sheet[~self.records_on_sheet['code'].isin([self.record['code']])]
        try:
            writer = pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace' )
        except:
            writer = pd.ExcelWriter(self.file_path)
        self.records_on_sheet.to_excel(writer, sheet_name=self.sheet, index=False)
        writer.save()
        print("The record is deleted")
        
        # Read the record from the spreadsheet
        self.all_records, self.record = self.get_records()
        

