"""Subclass of pnlExisting, which is generated by wxFormBuilder."""

import wx
from odmtools.view import clsExisting
from odmtools.odmdata import series

# Implementing pnlExisting
class pnlExisting(clsExisting.pnlExisting):
    def __init__(self, parent):
        clsExisting.pnlExisting.__init__(self, parent)

    # Handlers for pnlExisting events.
    def OnOLVItemSelected(self, event):
        # TODO: Implement OnOLVItemSelected
        pass

    def getSeries(self):
        selectedObject = self.olvSeriesList.GetSelectedObject()
        return selectedObject.method, selectedObject.quality_control_level, selectedObject.variable

    def initTable(self, dbservice, site_id):
        """Set up columns and objects to be used in the objectlistview to be visible in the series selector"""

        seriesColumns = [clsExisting.ColumnDefn(key, align="left", minimumWidth=-1, valueGetter=value)
                         for key, value in series.returnDict().iteritems()]

        self.olvSeriesList.SetColumns(seriesColumns)
        objects = dbservice.get_series_by_site(site_id= site_id)
        self.olvSeriesList.SetObjects(objects)
