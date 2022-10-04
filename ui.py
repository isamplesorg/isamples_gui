import os
import wx
import csv_import


class OpenFileButton(wx.Button):
    def __init__(self, panel: wx.Panel, label: str, text: wx.TextCtrl):
        super().__init__(parent=panel, label=label)
        self.text = text

    def on_button_click(self, e):
        wildcard = "TSV (*.tsv)|*.tsv"
        dlg = wx.FileDialog(self, "Choose", os.getcwd(), "No file selected", wildcard, wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.text.SetValue(dlg.GetPath())


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(450, 200))
        self.open_file_button = None
        self.validate_button = None
        self.init_ui()
        self.Show(True)

    def init_ui(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.open_file_button = MainFrame.construct_hbox(pnl, vbox, "Choose File")
        self.Bind(wx.EVT_BUTTON, self.open_file_button.on_button_click, self.open_file_button)
        self.Bind(wx.EVT_TEXT, self.validate_file_path_text, self.open_file_button.text)

        vbox.Add((0, 30))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.validate_button = wx.Button(pnl, label="Validate Data")
        self.validate_button.Enable(False)
        hbox.Add(self.validate_button)
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)
        self.Bind(wx.EVT_BUTTON, self.validate_package, self.validate_button)

        pnl.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def validate_package(self, e):
        package = csv_import.create_isamples_package(self.open_file_button.text.Value)
        report = package.validate()
        if report.valid:
            wx.MessageBox("Validation successful.", 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Validation unsuccessful.", 'Info', wx.OK | wx.ICON_INFORMATION)

    def validate_file_path_text(self, e):
        validate_button_enabled = False
        file_path = e.EventObject.Value
        if os.path.exists(file_path):
            validate_button_enabled = True
        self.validate_button.Enable(validate_button_enabled)

    @staticmethod
    def file_path_read_only_text(pnl: wx.Panel) -> wx.TextCtrl:
        return wx.TextCtrl(pnl, size=(275, 25), style=wx.TEXT_ALIGNMENT_RIGHT)

    @staticmethod
    def open_file_button(pnl: wx.Panel, text: wx.TextCtrl, button_text: str) -> OpenFileButton:
        return OpenFileButton(pnl, button_text, text)

    @staticmethod
    def construct_hbox(pnl: wx.Panel, vbox: wx.BoxSizer, button_text: str) -> tuple:
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        file_path_text = MainFrame.file_path_read_only_text(pnl)
        open_file_button = MainFrame.open_file_button(pnl, file_path_text, button_text)

        label = wx.StaticText(pnl)
        label.SetLabel("File Path:")

        hbox.Add(label, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(file_path_text, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(open_file_button, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)

        vbox.Add((0, 30))
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)

        return open_file_button
