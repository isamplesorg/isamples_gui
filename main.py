import wx
from ui import MainFrame

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None, "iSamples GUI")
    app.MainLoop()
