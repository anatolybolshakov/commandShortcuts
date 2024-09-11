import wx

from models.alias_metadata import get_formatted_aliases_list

class MainWindow(wx.Frame):
    def __init__(self, parent, title, command_files_path, alias_collection):
        self.command_files_path = command_files_path
        self.alias_collection = alias_collection

        commands_choices = [get_formatted_aliases_list(alias_data.aliases) for alias_data in alias_collection.get_custom_commands_data()]
        print(alias_collection.get_custom_commands_data())
        wx.Frame.__init__(self, parent, title=title, size=(500, 300))
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)  
        commandFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)  
        self.SetFont(font)

        editCommandTextCtrl = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        editCommandTextCtrl.SetFont(commandFont)
        commandsCbxLabel = wx.StaticText(self, label = 'Command Alias')
        commandsCbx = wx.ComboBox(self, choices=commands_choices, name='Command Name')
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        addButton = wx.Button(self, label='New')
        deleteButton = wx.Button(self, label='Delete')
        saveButton = wx.Button(self, label='Save Changes')

        buttonsSizer.Add(addButton, 1, wx.EXPAND)
        buttonsSizer.Add(saveButton, 1, wx.EXPAND)
        buttonsSizer.Add(deleteButton, 1, wx.EXPAND)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer.Add(commandsCbxLabel, 0, wx.ALL ^ wx.BOTTOM, 10)
        self.mainSizer.Add(commandsCbx, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        self.mainSizer.Add(buttonsSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)

        editCommandTextCtrlLabel = wx.StaticText(self, label = 'Command')
        self.mainSizer.Add(editCommandTextCtrlLabel, 0, wx.ALL ^ wx.BOTTOM, 10)
        self.mainSizer.Add(editCommandTextCtrl, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)


        self.SetSizer(self.mainSizer)
        self.SetAutoLayout(1)

        self.Show(True)

def run_editor(command_files_path, alias_collection):
    app = wx.App(False)
    frame = MainWindow(None, "Command Aliases Editor", command_files_path, alias_collection)
    frame.Show(True)
    app.MainLoop()
