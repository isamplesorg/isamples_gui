import os
import wx
import isamples_frictionless


class ValidationErrorsDialog(wx.Frame):
   def __init__(self, parent, title, errors_text: str):
      super(ValidationErrorsDialog, self).__init__(parent, title = title, size = (1000, 200))
      pnl = wx.Panel(self)
      vbox = wx.BoxSizer(wx.VERTICAL)
      hbox1 = wx.BoxSizer(wx.HORIZONTAL)

      self.text = wx.TextCtrl(pnl, size=(1000, 200), style=wx.TE_MULTILINE)
      self.text.Value = errors_text
      hbox1.Add(self.text, proportion=1, flag=wx.EXPAND)
      vbox.Add(hbox1, proportion=1, flag=wx.EXPAND)

      pnl.SetSizer(vbox)
      self.Centre()
      self.Show(True)



class OpenFileButton(wx.Button):
    def __init__(self, panel: wx.Panel, label: str, text: wx.TextCtrl):
        super().__init__(parent=panel, label=label)
        self.text = text

    def on_button_click(self, e):
        wildcard = "TSV (*.tsv)|*.tsv"
        dlg = wx.FileDialog(self, "Choose", os.getcwd(), "No file selected", wildcard, wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.text.SetValue(dlg.GetPath())


HORIZONTAL_SPACER_PIXELS = 5

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 200))
        self.open_schema_button = None
        self.open_file_button = None
        self.validate_button = None
        self.accel_tbl = None
        self._schema = None
        self.init_ui()
        self.Show(True)

    def init_ui(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.open_schema_button = MainFrame.construct_hbox(pnl, vbox, "Schema File Path:", "Choose Schema File")
        resource_path = os.environ.get("RESOURCEPATH") or ""
        self.open_schema_button.text.Value = os.path.join(resource_path, isamples_frictionless.DEFAULT_SCHEMA_FILE_NAME)
        self.open_file_button = MainFrame.construct_hbox(pnl, vbox, "Data File Path:", "Choose Data File")
        self.Bind(wx.EVT_BUTTON, self.open_file_button.on_button_click, self.open_file_button)
        self.Bind(wx.EVT_TEXT, self.validate_file_path_text, self.open_file_button.text)
        self.Bind(wx.EVT_CHAR_HOOK, self.key_down, self.open_file_button.text)

        vbox.Add((0, 30))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.validate_button = wx.Button(pnl, label="Validate Data File")
        self.validate_button.Enable(False)
        hbox.Add(self.validate_button)
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)
        self.Bind(wx.EVT_BUTTON, self.validate_package, self.validate_button)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        quit_menu_item = file_menu.Append(wx.NewId(), item="Quit     ⌘Q")
        self.Bind(wx.EVT_MENU, self.on_exit, quit_menu_item)

        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord("Q"), quit_menu_item.GetId())])
        self.SetAcceleratorTable(self.accel_tbl)

        pnl.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def on_exit(self, event):
        self.Close()

    def validate_package(self, e):
        package = isamples_frictionless.create_isamples_package(self._schema, self.open_file_button.text.Value)
        report = package.validate()
        if report.valid:
            wx.MessageBox("Validation successful.", 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            errors = isamples_frictionless.report_errors_as_str(report)
            ValidationErrorsDialog(self, "Validation Errors", errors)

    def validate_file_path_text(self, e):
        date_file_valid = False
        file_path = self.open_file_button.text.Value
        if os.path.exists(file_path):
            date_file_valid = True
        schema_path = self.open_schema_button.text.Value
        schema = isamples_frictionless.check_valid_schema_json(schema_path)
        self._schema = schema

        valid = date_file_valid and schema is not None
        self.validate_button.Enable(valid)

    def key_down(self, e):
        if e.GetKeyCode() == wx.WXK_RETURN:
            self.validate_file_path_text(e)
            if self.validate_button.Enabled:
                self.validate_package(e)
        else:
            e.Skip()

    @staticmethod
    def file_path_read_only_text(pnl: wx.Panel) -> wx.TextCtrl:
        return wx.TextCtrl(pnl, size=(275, 25), style=wx.TEXT_ALIGNMENT_RIGHT)

    @staticmethod
    def open_file_button(pnl: wx.Panel, text: wx.TextCtrl, button_text: str) -> OpenFileButton:
        return OpenFileButton(pnl, button_text, text)

    @staticmethod
    def construct_hbox(pnl: wx.Panel, vbox: wx.BoxSizer, label_text: str, button_text: str) -> tuple:
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        file_path_text = MainFrame.file_path_read_only_text(pnl)
        open_file_button = MainFrame.open_file_button(pnl, file_path_text, button_text)

        label = wx.StaticText(pnl)
        label.SetLabel(label_text)

        hbox.Add(label, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbox.AddSpacer(HORIZONTAL_SPACER_PIXELS)
        hbox.Add(file_path_text, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbox.AddSpacer(HORIZONTAL_SPACER_PIXELS)
        hbox.Add(open_file_button, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)

        vbox.Add((0, 30))
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)

        return open_file_button
