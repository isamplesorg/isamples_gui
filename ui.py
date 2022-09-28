import os
import wx

from isamples_inabox.isb_lib.data_import import csv_import


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
        self.init_ui()
        self.Show(True)

    def init_ui(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.open_file_button = MainFrame.construct_hbox(pnl, vbox, "")
        self.Bind(wx.EVT_BUTTON, self.open_file_button.on_button_click, self.open_file_button)

        vbox.Add((0, 30))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        action_button = wx.Button(pnl, label="Validate Data")
        hbox.Add(action_button)
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)
        self.Bind(wx.EVT_BUTTON, self.do_validation, action_button)

        pnl.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def do_validation(self, e):
        package = csv_import.create_isamples_package(MainFrame.open_file_button.text)
        report = package.validate()
        if report.valid:
            wx.MessageBox("Validation successful.", 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Validation unsuccessful.", 'Info', wx.OK | wx.ICON_INFORMATION)

    @staticmethod
    def file_path_read_only_text(pnl: wx.Panel) -> wx.TextCtrl:
        return wx.TextCtrl(pnl, size=(275, 25), style=wx.TE_READONLY & wx.TEXT_ALIGNMENT_RIGHT)

    @staticmethod
    def open_file_button(pnl: wx.Panel, text: wx.TextCtrl, button_text: str) -> OpenFileButton:
        return OpenFileButton(pnl, button_text, text)

    @staticmethod
    def construct_hbox(pnl: wx.Panel, vbox: wx.BoxSizer, button_text: str) -> tuple:
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        file_path_text = MainFrame.file_path_read_only_text(pnl)
        open_file_button = MainFrame.open_file_button(pnl, file_path_text, button_text)

        hbox.Add(file_path_text, proportion=1, flag=wx.ALIGN_LEFT)
        hbox.Add(open_file_button, proportion=0.75, flag=wx.RIGHT)

        vbox.Add((0, 30))
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)

        return open_file_button
