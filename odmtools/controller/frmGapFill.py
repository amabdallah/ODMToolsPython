"""Subclass of dlgFill, which is generated by wxFormBuilder."""

from odmtools.view import clsGapFill


# Implementing dlgFill
class frmGapFill(clsGapFill.dlgFill):
    def __init__(self, parent, record_service):
        self.record_service = record_service
        clsGapFill.dlgFill.__init__(self, parent)

    # Handlers for dlgFill events.
    def onOKBtn(self, event):
        #TODO add validation
        gapvalue= self.txtGap.Value
        gaptime = self.cbGap.Value
        fillvalue = self.txtFill.Value
        filltime= self.cbFill.Value

        self.record_service.fill_gap(gap=[gapvalue, gaptime], fill=[fillvalue, filltime])
        self.Close()

    def OnCancelBtn(self, event):

        self.Close()
        self.Destroy()
