import wx
from ui import MainFrame

app = wx.App(False)
frame = MainFrame(None, "iSamples GUI")
app.MainLoop()