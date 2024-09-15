import wx

from models.alias_metadata import AliasMetadata, generate_command_alias_file_name, get_formatted_aliases_list, save_command_to_file

class MainWindow(wx.Frame):
    def __init__(self, parent, title, command_files_path, alias_metadata_file_path, alias_collection):
        self.command_files_path = command_files_path
        self.alias_collection = alias_collection
        self.alias_metadata_file_path = alias_metadata_file_path

        commands_choices = [get_formatted_aliases_list(alias_data.aliases) for alias_data in alias_collection.get_custom_commands_data()]
        print(alias_collection.get_custom_commands_data())
        wx.Frame.__init__(self, parent, title=title, size=(500, 300))
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)  
        commandFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)  
        self.SetFont(font)

        self.editCommandTextCtrl = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.editCommandTextCtrl.SetFont(commandFont)
        commandsCbxLabel = wx.StaticText(self, label = 'Command Alias')
        self.commandsCbx = wx.ComboBox(self, choices=commands_choices, name='Command Name')
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        addButton = wx.Button(self, label='New')
        addButton.Bind(wx.EVT_BUTTON, self.on_new_click)
        deleteButton = wx.Button(self, label='Delete')
        deleteButton.Bind(wx.EVT_BUTTON, self.on_delete_click)
        saveButton = wx.Button(self, label='Save Changes')
        saveButton.Bind(wx.EVT_BUTTON, self.on_save_click)

        buttonsSizer.Add(addButton, 1, wx.EXPAND)
        buttonsSizer.Add(saveButton, 1, wx.EXPAND)
        buttonsSizer.Add(deleteButton, 1, wx.EXPAND)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer.Add(commandsCbxLabel, 0, wx.ALL ^ wx.BOTTOM, 10)
        self.mainSizer.Add(self.commandsCbx, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        self.mainSizer.Add(buttonsSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)

        editCommandTextCtrlLabel = wx.StaticText(self, label = 'Command')
        self.mainSizer.Add(editCommandTextCtrlLabel, 0, wx.ALL ^ wx.BOTTOM, 10)
        self.mainSizer.Add(self.editCommandTextCtrl, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)


        self.SetSizer(self.mainSizer)
        self.SetAutoLayout(1)

        self.Show(True)
    
    def on_new_click(self, event):
        print('New')
    
    def on_delete_click(self, event):
        print('Delete')

    def on_save_click(self, event):
        if self.commandsCbx.Selection < 0:
            aliases_list = self.commandsCbx.Value
            command_content = self.editCommandTextCtrl.Value

            if aliases_list.strip() == '':
                self.show_error_popup('Command aliases list should not be empty')
                return
            
            if command_content.strip() == '':
                self.show_error_popup('Command should not be empty')
                return

            command_alias_file_name = generate_command_alias_file_name(aliases_list)
            save_command_to_file(self.command_files_path, command_alias_file_name, command_content)

            alias_metadata = AliasMetadata(
                aliases=aliases_list.split(' '), 
                type_value='custom',
                description='todo',
                params=[],
                command=None,
                command_file=command_alias_file_name,
                param_boundary_placeholder=None,
            )

            self.alias_collection.add_alias_metadata(alias_metadata)
            self.alias_collection.save_to_file(self.alias_metadata_file_path)

    def show_error_popup(self, error_message):
        wx.MessageBox(error_message,"Error", wx.OK | wx.ICON_ERROR)

def run_editor(command_files_path, alias_metadata_file_path, alias_collection):
    app = wx.App(False)
    frame = MainWindow(None, "Command Aliases Editor", command_files_path, alias_metadata_file_path, alias_collection)
    frame.Show(True)
    app.MainLoop()
