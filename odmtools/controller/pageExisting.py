"""Subclass of pnlExisting, which is generated by wxFormBuilder."""

import wx
from odmtools.view import clsExisting
from odmtools.odmdata import returnDict
import wx.wizard as wiz
import datetime

# Implementing pnlExisting
#class pnlExisting(clsExisting.pnlExisting):
#    def __init__(self, parent):
#        clsExisting.pnlExisting.__init__(self, parent)

########################################################################
class pageExisting(wiz.WizardPageSimple):
    def __init__(self, parent, title, series_service , site):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
        #self.series_service = series_service

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND | wx.ALL, 5)
        self.pnlExisting = clsExisting.pnlExisting(self)  #, id=wxID_PNLEXISTING, name=u'pnlExisting',
        #pos=wx.Point(536, 285), size=wx.Size(439, 357),
        #style=wx.TAB_TRAVERSAL)#, sm = service_man, series_service = series_service)
        self.sizer.Add(self.pnlExisting, 85, wx.ALL, 5)
        self._init_data(series_service, site.id)


        self.pnlExisting.olvSeriesList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnOLVItemSelected)
        self.pnlExisting.rbOverwrite.Bind(wx.EVT_RADIOBUTTON, self.onOverwrite)
        self.pnlExisting.rbAppend.Bind(wx.EVT_RADIOBUTTON, self.onAppend)

    def _init_data(self, series_serv, site_id):
        index = 0
        self.initTable(series_serv, site_id)

        #if q.code == self.qcl.code:
        #    index = i

        self.pnlExisting.olvSeriesList.Focus(index)
        self.pnlExisting.olvSeriesList.Select(index)



    # Handlers for pnlExisting events.
    def OnOLVItemSelected(self, event):
        # TODO: Implement OnOLVItemSelected
        pass

    def onOverwrite(self, event):
        self.enableButtons(False)
        # event.skip()

    def onAppend(self, event):
        self.enableButtons(True)
        # event.Skip()

    def enableButtons(self, isEnabled):
        self.pnlExisting.rbNew.Enable(isEnabled)
        self.pnlExisting.rbOriginal.Enable(isEnabled)
        self.pnlExisting.lblOverlap.Enable(isEnabled)

    def getSeries(self):
        selectedObject = self.pnlExisting.olvSeriesList.GetSelectedObject()
        return selectedObject.method, selectedObject.quality_control_level, selectedObject.variable

    def initTable(self, dbservice, site_id):
        """Set up columns and objects to be used in the objectlistview to be visible in the series_service selector"""

        seriesColumns = [clsExisting.ColumnDefn(key, align="left",
                                                minimumWidth=-1, valueGetter=value,
                                                stringConverter= '%Y-%m-%d %H:%M:%S' if 'date' in key.lower() else '%s')
                         for key, value in returnDict().iteritems()]

        self.pnlExisting.olvSeriesList.SetColumns(seriesColumns)
        objects = dbservice.get_series_by_site(site_id= site_id)
        self.pnlExisting.olvSeriesList.SetObjects(objects)
