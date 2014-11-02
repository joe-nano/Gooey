

__author__ = 'Chris'

import wx
from abc import ABCMeta, abstractmethod
from calender_dialog import CalendarDlg


class WidgetPack(object):
  """
  Interface specifying the contract to which
  all `WidgetPack`s will adhere
  """
  __metaclass__ = ABCMeta

  @abstractmethod
  def build(self, parent, data):
    pass

  @abstractmethod
  def getValue(self):
    pass

  def onResize(self, evt):
    pass



class BaseChooser(WidgetPack):
  def __init__(self, button_text='Browse'):
    self.button_text = button_text

    self.parent = None
    self.text_box = None
    self.button = None

  def build(self, parent, data=None):
    self.parent = parent
    self.text_box = wx.TextCtrl(self.parent)
    self.button = wx.Button(self.parent, label=self.button_text, size=(73, 23))

    widget_sizer = wx.BoxSizer(wx.HORIZONTAL)
    widget_sizer.Add(self.text_box, 1, wx.EXPAND)
    widget_sizer.AddSpacer(10)
    widget_sizer.Add(self.button, 0)

    parent.Bind(wx.EVT_BUTTON, self.onButton, self.button)
    return widget_sizer

  def getValue(self):
    return self.text_box.GetValue()

  def onButton(self, evt):
    raise NotImplementedError


class FileChooserPayload(BaseChooser):
  def __init__(self):
    BaseChooser.__init__(self)

  def onButton(self, evt):
    dlg = wx.FileDialog(self.parent, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    result = (dlg.GetPath()
              if dlg.ShowModal() == wx.ID_OK
              else None)
    if result:
      # self.text_box references a field on the class this is passed into
      # kinda hacky, but avoided a buncha boilerplate
      self.text_box.SetLabelText(result)


class DirChooserPayload(BaseChooser):
  def __init__(self):
    BaseChooser.__init__(self)

  def onButton(self, evt):
    dlg = wx.DirDialog(self.parent, 'Select directory', style=wx.DD_DEFAULT_STYLE)
    result = (dlg.GetPath()
              if dlg.ShowModal() == wx.ID_OK
              else None)
    if result:
      self.text_box.SetLabelText(result)


class DateChooserPayload(BaseChooser):
  def __init__(self):
      BaseChooser.__init__(self, button_text='Pick Date')

  def onButton(self, evt):
    dlg = CalendarDlg(self.parent)
    dlg.ShowModal()
    if dlg.GetPath():
      self.text_box.SetLabelText(dlg.GetPath())


class TextInputPayload(WidgetPack):
  def __init__(self):
    self.widget = None

  def build(self, parent, data):
    self.widget = wx.TextCtrl(parent)
    return self.widget

  def getValue(self):
    return self.widget.GetValue()


class DropdownPayload(WidgetPack):
  default_value = 'Select Option'
  def __init__(self):
    self.option_string = None
    self.widget = None

  def build(self, parent, data):
    self.option_string = data['commands'][0]
    self.widget = wx.ComboBox(
        parent=parent,
        id=-1,
        value=self.default_value,
        choices=data['choices'],
        style=wx.CB_DROPDOWN
    )
    return self.widget

  def getValue(self):
    if self.widget.GetValue() == self.default_value:
      return None
    return ' '.join([self.option_string, self.widget.GetValue()])


class CounterPayload(WidgetPack):
  def __init__(self):
    self.option_string = None
    self.widget = None

  def build(self, parent, data):
    self.option_string = data['option_strings'][0]
    self.widget = wx.ComboBox(
      parent=parent,
      id=-1,
      value='',
      choices=[str(x) for x in range(1, 7)],
      style=wx.CB_DROPDOWN
    )
    return self.widget

  def getValue(self):
    '''
    Returns
      str(option_string * DropDown Value)
      e.g.
      -vvvvv
    '''
    dropdown_value = self.widget.GetValue()
    if not str(dropdown_value).isdigit():
      return None
    arg = str(self.option_string).replace('-', '')
    repeated_args = arg * int(dropdown_value)
    return '-' + repeated_args

