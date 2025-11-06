# from dbquery import *
from reudbquery import *
# from dotenv import load_dotenv
import os
# import panel as pn
import ipywidgets as widgets
from ipywidgets_jsonschema import Form
from ipyfilechooser import FileChooser
from IPython.display import display, SVG
from IPython.display import IFrame
from IPython import display as dsp
import json
import glob
import csv
import tempfile

from appdirs import user_data_dir


# eventually, the markdown package will not be needed anymore
import markdown

from rpy2.robjects.packages import importr
from rpy2.ipython.ggplot import image_png

from rpy2.robjects import conversion
from rpy2.robjects import default_converter
import rpy2.robjects.numpy2ri as numpy2ri
import rpy2.robjects.pandas2ri as pandas2ri

# Compose a converter
my_converter = conversion.Converter('my converter')
my_converter += default_converter
my_converter += numpy2ri.converter
my_converter += pandas2ri.converter

class dsp_app(object):
    def __init__(self):
        self.rugplot = importr('rugplot')
        self.jl = importr('jsonlite')

        self.appname = 'dsp'
        self.author = 'rug'
        self.dspver = '0.0.1'

        # load_dotenv()
        # self.db_user = os.getenv("DB_USER")
        # self.db_pass = os.getenv("DB_PASS")
        # self.p_host = os.getenv("P_HOST") 
        # self.p_port = os.getenv("P_PORT")
        # self.db = os.getenv("DB")
        # self.pgres = Postgresql_connect(pgres_host=self.p_host, pgres_port=self.p_port, db=self.db, ssh_user=self.db_user, db_pass=self.db_pass)
        
        # datalinkage schemas
        # exclude_temp = self.pgres.schemas(db=self.db)
        # self.schemas = exclude_temp["schema name"].tolist()
        # self.schemas.pop(0)
        
        # technique json schemas
        self.jsfiles = self.rugplot.list_rugplots()
        # self.csvfiles = glob.glob('../**/*.{}'.format('csv'),recursive=True)

        # self.jsfiles = glob.glob('../**/*{}'.format('schema.json'),recursive=True)
        # self.jsfiles = [(os.path.split(f)[-1].split('_', 1)[0],f) for f in self.jsfiles]
        # self.jsfilesdict = dict((x, y) for x, y in jsfiles)
        
        self.declare_widgets()
        self.observe_and_click()

        # sqlite

        self.data_dir = user_data_dir(self.appname, self.author, version=self.dspver)
        self.sqlitedb = SQlite_connect(self.data_dir, self.appname)
        # self.sqlitedb = {'drivername':'sqlite','database':self.data_dir+'/'+self.appname+'.sqlite3'}
        # self.sqlite_uri=URL.create(**self.sqlitedb)
                    
        # ipywidgets
        
    def declare_widgets(self):
        self.output_form = widgets.Output()
        self.output_results = widgets.Output()

        # self.datasources = widgets.Dropdown(
        #     options = ['Datalinkage','Filesystem'],
        #     value = 'Filesystem',
        #     description='Datasource:',
        #     disabled = False,
        # )
        # self.menuDbSchemas = widgets.Dropdown(
        #     options=[],
        #     value=None,
        #     description='DB schema:',
        #     disabled=True,
        # )

        # self.menuTables = widgets.Dropdown(
        #     options= self.csvfiles, # as initally filesystem is selected by default
        #     value=None,
        #     description='Table:',
        #     disabled=False,
        # )

        self.filechooser = FileChooser()

        
        self.select_experiment = widgets.Dropdown(
            options= [], # as initally filesystem is selected by default
            value=None,
            description='Experiment:',
            disabled=False,
        )
        
        self.button_display_types = widgets.Button(
            description='Types',
            disabled=False,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Display column data types',
            # icon='list',
            layout=widgets.Layout(display='flex', align_items='flex-end')
        )

        self.button_display_header = widgets.Button(
            description='Header',
            disabled=False,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Display the first 7 rows of a table',
            # icon='list',
            layout=widgets.Layout(display='flex', align_items='flex-end')
        )

        self.menuSchemas = widgets.Dropdown(
            options=self.jsfiles,
            value=None,
            description='Technique:',
            disabled=False,
        )

        self.selectCols = widgets.SelectMultiple(
            options = [],
            # value=None,
            # rows=10,
            description='Select columns',
            disabled=False
        )

        self.button_run_technique = widgets.Button(
            description='Run technique',
            disabled=False,
            button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Runs the selected technique using the provided data and parameters',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )

        self.button_help = widgets.Button(
            description='Help',
            disabled=False,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Displays help on the panel on the right',
            icon='' # (FontAwesome names without the `fa-` prefix)
        )

        self.button_reproducible = widgets.Button(
            description='Reproducible',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save parameters, data and technique for reproducibility',
            # icon='check' # (FontAwesome names without the `fa-` prefix)
        )

        self.button_save_params = widgets.Button(
                description='Save',
                disabled=False,
                button_style='success', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Save parameters, data and technique for reproducibility',
            # icon='check' # (FontAwesome names without the `fa-` prefix)
            )

        self.button_RDMS = widgets.Button(
            description='RDMS',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save reproducible results in the RDMS long term  storage system',
            icon='' # (FontAwesome names without the `fa-` prefix)
        )

        self.button_MyResults = widgets.Button(
            description='My results',
            disabled=False,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Reproducible-results tasks',
            icon='' # (FontAwesome names without the `fa-` prefix)
        )

        # self.rimage = widgets.Image(
        #                 )

        self.button_Load = widgets.Button(
            description='Load',
            disabled=False,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Reproducible-results tasks',
            icon='' # (FontAwesome names without the `fa-` prefix)
        )

        self.button_Habrok = widgets.Button(
            description='Habrok',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Run the technique as a long asynchronous process in Habrok',
            icon='' # (FontAwesome names without the `fa-` prefix)
        )

        self.button_request = widgets.Button(
            description='Request',
            disabled=False,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Request a new technique',
            icon='' # (FontAwesome names without the `fa-` prefix)
        )

        # Eventually, this widget will be replaced by sphinx documentation
        self.md = widgets.HTML(
            value="Hello <b>HTML widget</b>",
            # placeholder='Some HTML',
            # description='Some HTML',
        )
        
        tabChildren = [self.output_form, self.output_results]
        self.tab = widgets.Tab()
        self.tab.children = tabChildren
        self.tab.titles = ["Parameters", "Results"]
        self.tab.selected_index = 1    
        with self.output_results:
            display(IFrame(src= 'https://docker-cds.readthedocs.io/en/latest/reusable_techniques.html',
                           width=700, height=600))

        self.disp_buttons = widgets.HBox(children =[self.button_display_types, self.button_display_header])
        self.hr_buttons = widgets.HBox(children =[self.button_help, self.button_run_technique])
        self.reproH_buttons = widgets.HBox(children =[self.button_reproducible, self.button_Habrok])
        self.MyRDMS_buttons = widgets.HBox(children =[self.button_MyResults, self.button_RDMS])

        self.header = widgets.HTML("<h1>Reproducible results and reusable techniques</h1>", layout=widgets.Layout(height='auto'))
        self.header.style.text_align='center'
        self.lsidebar = widgets.VBox(children = [#self.datasources, self.menuDbSchemas, self.menuTables, 
                                                 self.filechooser, self.disp_buttons, 
                                                 self.selectCols, self.menuSchemas, self.hr_buttons, self.reproH_buttons, 
                                                 self.MyRDMS_buttons,
                                                 self.button_request])
        
        # end of declare widgets
    
    def setcolnames(self, jschema, fcolumns):
        if isinstance(jschema, dict):
            if "$comment" in jschema:
                jschema['enum'] = fcolumns
            for key, value in jschema.items():
                self.setcolnames(value, fcolumns)
        elif isinstance(jschema, list):
            for item in jschema:
                self.setcolnames(item, fcolumns)

    def delete_none(self, d):
        """Delete None values recursively from all of the dictionaries"""
        if isinstance(d, dict):
            return {
                k: v 
                for k, v in ((k, self.delete_none(v)) for k, v in d.items())
                if isinstance(v, bool) or v
            }
        if isinstance(d, list):
            return [v for v in map(self.delete_none, d) if isinstance(v, bool) or v]
        return d
                

    def get_csv_colnames(self, csvfile):
        # TODO: validate that the columns can be extracted
        with open(csvfile, 'r', newline='') as f_headers:
            fcols = next(csv.reader(f_headers))
        return(fcols)

    def new_empty_form(self):
        if self.menuSchemas.value:
            raw_schema = self.rugplot.rug_jsonschema(self.menuSchemas.value)
            self.fschema = json.loads(''.join(raw_schema))
        
            self.jsform = Form(self.fschema)
            with self.output_form:
                self.output_form.clear_output()
                self.jsform.show(width="600px")
                
    # on change functions

    # def on_datasource_change(self, change):
    #     if change["new"] == "Datalinkage":
    #         self.menuDbSchemas.disabled = False
    #         self.menuDbSchemas.options = self.schemas
    #         self.menuTables.options = []
    #         self.menuTables.value = None
    #         self.selectCols.options = []
    #     else:
            
    #         self.menuDbSchemas.options = []
    #         self.menuDbSchemas.value = None
    #         self.menuDbSchemas.disabled = True
    #         self.menuTables.options = self.csvfiles
    #         self.menuTables.value = None
    #         self.selectCols.options = []
            
    #         # self.selectCols.value = tuple()

    #     self.new_empty_form()
    
    # a new db schema ha been selected
    # def on_schema_change(self, change):
    #     tables = self.pgres.tables(self.db, schema=change["new"])
    #     self.menuTables.options = tables["table name"].tolist()

    #     self.new_empty_form()

    # a new table has been selected
    # def on_table_change(self, change):

    #     if change["new"]:
    #         if not self.menuDbSchemas.disabled:
    #             tcols = self.pgres.tcolumns(self.db, self.menuDbSchemas.value, change["new"])
    #             self.selectCols.options = tcols['column_name'].tolist()
    #         else:
    #             # extract columns from the csv file
    #             self.selectCols.options = self.get_csv_colnames(change["new"])
    #     self.selectCols.value = tuple()
    
    #     # display a new empty form
    #     self.new_empty_form()


    def on_filechooser_change(self):

        self.selectCols.options = self.get_csv_colnames(self.filechooser.selected)
        self.selectCols.value = tuple()
        self.new_empty_form()
    
    def on_cols_change(self, change):
    
        if change["new"]:    
            if self.menuSchemas.value is not None:
                self.setcolnames(self.fschema,list(change["new"]))
                self.fschema['properties']['filename']['default'] = self.filechooser.selected
        
                self.jsform = Form(self.fschema)
                with self.output_form:
                    self.output_form.clear_output()
                    self.jsform.show(width="600px")



# def on_technique_change(self, change):
#     with conversion.localconverter(my_converter):
#         raw_schema = self.rugplot.rug_jsonschema(change['new'])
#     self.fschema = json.loads(''.join(raw_schema))                    
        
    def on_technique_change(self, change):

        with conversion.localconverter(my_converter):
            raw_schema = self.rugplot.rug_jsonschema(change['new'])
        self.fschema = json.loads(''.join(raw_schema))
    
        if self.filechooser.selected != None:
            self.setcolnames(self.fschema,list(self.selectCols.value))
            # update filename
            self.fschema['properties']['filename']['default'] = self.filechooser.selected

        self.tab.selected_index = 0
        self.jsform = Form(self.fschema)
        with self.output_form:
            self.output_form.clear_output()
            self.jsform.show(width="600px")

    def on_click_Habrok(self, b):
        # global outputf
    
        self.output_results.clear_output()
        self.tab.selected_index = 1

        mdtext = """### This feature will submit a job on Habrok 
        """

        htmltext = markdown.markdown(mdtext)
    
        with self.output_results:
            self.md.value = htmltext
            display(self.md)

    def on_click_MyResults(self, b):
        # global outputf
    
        self.output_results.clear_output()
        self.tab.selected_index = 1


        # TODO: consider including other libraries than 'rugplot'
        exps = self.sqlitedb.experiments()

        self.output_results.clear_output()
        self.tab.selected_index = 1
        
        with self.output_results:
            if len(exps) > 0:
                print("Select an experiment to load")
                self.select_experiment.options = list(exps["experiment_id"])
                display(widgets.HBox(children =[self.select_experiment, self.button_Load]))
                display(exps[["experiment_id", "tlibrary", "tname", "params"]])
            else:
                print("No experiments found")
        
        
        mdtext = """### This feature will perform 'reproducible-results' tasks such as:   
        * List reproducible results
        * Search reproducible results
        * Display results
        """

        htmltext = markdown.markdown(mdtext)
    
        with self.output_results:
            # print(htmltext)
            self.md.value = htmltext
            display(self.md)

    def display_result(self, save_params):
        imgdevice = save_params["device"]
        fname = save_params["outputfilename"]

        if imgdevice == "tikz":
            imgdevice = "pdf"

        if fname is None:
            print("The result is in the folder of the dataset")
            return
        elif not fname.endswith("."+imgdevice):
            fname = fname + "." + imgdevice
            
            if imgdevice in ["png","jpeg", "tiff","bmp"]:
                display(dsp.Image(fname))
            elif imgdevice == "svg":
                display(SVG(fname))
            elif imgdevice == "pdf":
                display(IFrame(fname, width = save_params["width"]*30, height= save_params["height"]*30))
            elif imgdevice == "html":
                display(IFrame(fname, width = save_params["width"]*30, height= save_params["height"]*30))        
    
    
    def on_click_Load(self, b):
        # global outputf

        with self.output_results:
            if self.select_experiment.value:
                self.output_results.clear_output()

                exp = self.sqlitedb.get_experiment(self.select_experiment.value)
                
                tmp_params = exp["params"]
                tmp_params = json.loads(''.join(tmp_params))
                fpath = os.path.split(tmp_params["filename"])
                self.filechooser._select_default = True
                self.filechooser.reset(path=fpath[0], filename=fpath[1])
                self.on_filechooser_change()                
                
                self.selectCols.value = tmp_params["variables"]
                self.menuSchemas.value = exp["tname"][0]
                self.tab.selected_index = 1
                self.jsform.data = tmp_params
                
                if not tmp_params["save"]["save"]:
                    print("Parameters loaded but no file was saved, please click on the 'Run technique' button to display the results.")
                    # print("Technique: '{}'".format(exp["tname"][0]))
                    # print("Variables: '{}'".format(tmp_params["variables"]))
                    # 
                else:
                    print("Result")
                    self.display_result(tmp_params["save"])
                    print(json.dumps(tmp_params, indent = 4))        
                
    
    def on_click_reproducible(self, b):
        # global outputf
    
        self.output_results.clear_output()
        self.tab.selected_index = 1

        mdtext = """### This feature will store the following metadata for local reproducibility:        
        * environment
            - method (selected by the user)
            - container (stored in Docker Hub or Zenodo)
        * input
            - file (selected by the user)
            - parameters of the method (provided in the form)
        * output
            - results (filepath)

        NOTE: This reproducibility method is sensitive to filepath/name changes.
        """

        htmltext = markdown.markdown(mdtext)

        self.tmp_params = self.jsform.data

        self.tmp_params = self.delete_none(self.tmp_params)
        self.tmp_params["variables"] = self.selectCols.value
        # self.tmp_params["datasource"] = self.datasources.value
        # if self.datasources.value == 'Datalinkage':
        #     self.tmp_params["dbschema"] = self.menuDbSchemas.value
    
        with self.output_results:
            print("The current parameters and the current '{}' technique will be stored in the database".format(self.menuSchemas.value))
            display(self.button_save_params)
            print(json.dumps(self.tmp_params, indent = 4))
            self.md.value = htmltext
            display(self.md)

    def on_click_save_params(self, b):
        """
        Save metadata in a database for reproducibility
        """
        
        # TODO: consider including other libraries than 'rugplot'
        new_exp = self.sqlitedb.save_params(json.dumps(self.tmp_params), "rugplot", self.menuSchemas.value)

        self.output_results.clear_output()
        self.tab.selected_index = 1
        
        with self.output_results:
            if new_exp:
                print("Parameters saved with key: '{}'",new_exp.inserted_primary_key)
            else:
                print("ERROR: parameters not saved")
        
        

    def on_click_RDMS(self, b):
    
        self.output_results.clear_output()
        self.tab.selected_index = 1

        mdtext = """### This feature will store reproducible results in the RDMS for long term storage

        * information collected in the 'reproducible' feature
        * data
        * additional information

        """

        htmltext = markdown.markdown(mdtext)
        
        with self.output_results:
            self.md.value = htmltext
            display(self.md)
        
    def on_click_request(self, b):
    
        self.output_results.clear_output()
        self.tab.selected_index = 1

        mdtext = """### Requests 

        * New features in the GUI
        * New techniques
        * Fix bugs
        * ...
        """

        htmltext = markdown.markdown(mdtext)
        
        with self.output_results:
            self.md.value = htmltext
            display(self.md)

    def on_click_help(self, b):
    
        self.output_results.clear_output()
        self.tab.selected_index = 1
    
        # TODO: verify that the 'help' field exists
        with self.output_results:
            if self.menuSchemas.value:
                display(IFrame(src=self.fschema['description'], width=900, height=600))
            else:
                print("A technique must be selected")

                
    def on_click_header(self, b):
        self.output_results.clear_output()
        self.tab.selected_index = 1

        with self.output_results:
            if self.filechooser.value:
                # if self.datasources.value == "Filesystem":
                tcols = pd.read_csv(self.filechooser.selected, nrows=7)            
                display(tcols)
                # else:
                #     tab_head = f'SELECT * FROM {self.menuDbSchemas.value}.{self.filechooser.value} LIMIT 7 ;'
                #     query_df = self.pgres.query(self.db, query=tab_head)
            else:
                query_df = "A file must be selected"
                display(query_df) 
        
    def on_click_types(self, b):
        self.output_results.clear_output()
        self.tab.selected_index = 1

        with self.output_results:
            if self.filechooser.selected:
                # if self.datasources.value == "Filesystem":
                tcols = pd.read_csv(self.filechooser.selected, nrows=7)
                tcols.info()
            # else: 
            #     tcols = self.pgres.tcolumns(self.db, self.menuDbSchemas.value, self.menuTables.value)
            else:
                tcols = "A file must be selected"
                display(tcols) 

    def on_click_technique(self, b):
    
        # schema = self.menuDbSchemas.value
        # table = self.menuTables.value
        table = self.filechooser.selected
        cols = self.selectCols.value
        tech = self.menuSchemas.value
    
        self.tab.selected_index = 1
        self.output_results.clear_output()
        
        with self.output_results:
            # if schema is None:
            #     print("Please select a schema")
            #     return
            print(table)
            if table is None:
                print("Please select a table")
                return
            if len(cols) < 1:
                print("Please select at least one column")
                return
            if tech is None:
                print("Please select an appropriate technique")
                return

#         if self.datasources.value == "Datalinkage":
#             # selected columns
#             scols = ''.join([str(ele) + ", " for ele in cols])
#             scols = scols[:len(scols)-2]
    
#             # sql statement to retrieve the data
#             sqlst = 'SELECT {} FROM {}.{} LIMIT 100 ;'.format(scols, schema, table)
    
#             # retrieve the data
#             query_df = self.pgres.query(self.db, query=sqlst)
    
#             # temporary file
#             with tempfile.NamedTemporaryFile() as temp:
#                 query_df.to_csv(temp.name + '.csv', index = False)
        
#             table = temp.name + '.csv'
#             print(table)
    
        
        with self.output_results:
            try:
                js = self.jsform.data
            except (self.jsform.data.ValidationError, Exception) as e:
                # print(e)
                pass
                return

        # if self.datasources.value == "Filesystem":
        #     js["variables"] = cols
    
        js["filename"] = table

        save = js["save"]
    
        # print(js)

        js = json.dumps(js)
        plot = self.menuSchemas.label    
    
        with self.output_results:
            self.output_results.clear_output()
            with conversion.localconverter(my_converter):
                lp = self.jl.fromJSON(js)
                p = self.rugplot.create_rugplot(lp,plot)
            
                if save["save"]:
                    # TODO: redesign the save function
                    #       the fileoutput predefined in the front end, not back end
                    self.output_results.clear_output()
                    print("Output file: {}".format(save["outputfilename"]))
                    self.display_result(save)
                    print("For a better representation, open the file using the browser on the left")
                else:
                    display(image_png(p))
            # print(dir(p))
            # print(p)
        
    def observe_and_click(self):
        # self.datasources.observe(self.on_datasource_change,names='value')
        # self.menuDbSchemas.observe(self.on_schema_change, names='value')
        # self.menuTables.observe(self.on_table_change,names='value')
        # self.filechooser.observe(self.on_filechooser_change,names='value')
        # Register callback function
        self.filechooser.register_callback(self.on_filechooser_change)
        self.menuSchemas.observe(self.on_technique_change, names = 'value')
        self.selectCols.observe(self.on_cols_change, names = 'value')
        self.button_run_technique.on_click(self.on_click_technique)
        self.button_display_types.on_click(self.on_click_types)
        self.button_display_header.on_click(self.on_click_header)
        self.button_help.on_click(self.on_click_help)
        self.button_reproducible.on_click(self.on_click_reproducible)
        self.button_RDMS.on_click(self.on_click_RDMS)
        self.button_request.on_click(self.on_click_request)
        self.button_Habrok.on_click(self.on_click_Habrok)
        self.button_MyResults.on_click(self.on_click_MyResults)
        self.button_save_params.on_click(self.on_click_save_params)
        self.button_Load.on_click(self.on_click_Load)
        
    def run_app(self):
        app = widgets.AppLayout(header = self.header,
                 left_sidebar = self.lsidebar,
                 center = self.tab,
                 footer = None,
                 height='700px'
                 )
        display(app)
