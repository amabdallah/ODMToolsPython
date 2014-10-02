"""
    Bulk Insert of points
"""
import wx
import odmtools.view.clsBulkInsert as clsBulkInsert
import odmtools.controller.olvAddPoint as olv
import pandas as pd
from pandas.parser import CParserError

__author__ = 'Jacob'


class BulkInsert(clsBulkInsert.BulkInsert):
    def __init__(self, parent):
        clsBulkInsert.BulkInsert.__init__(self, parent)
        self.parent = parent

    def onUpload(self, event):
        """Reads csv into pandas object

        Parameters
        ----------
        filepath : string
            path to csv file
        """

        ## Obtain CSV filepath
        openFileDialog = wx.FileDialog(self, "Open CSV file", "", "", "CSV files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        value = openFileDialog.ShowModal()

        if value == wx.ID_CANCEL:
            return

        filepath = openFileDialog.GetPath()

        try:
            data = pd.read_csv(filepath, converters={
                "DataValue": self.checkDataValue,
                "Date": self.checkDate,
                "CensorCode": self.checkCensorCode,
                "ValueAccuracy": self.checkValueAcc,
                "OffSetValue": self.checkOffsetValue,
                "OffSetType": self.checkOffsetType,
                "QualifierCode": self.checkQualifierCode,
                "LabSampleCode": self.checkLabSample},
                skiprows=1
            )
        except CParserError as e:
            msg = wx.MessageDialog(None, "There was an issue trying to parse your file. "
                                         "Please compare your csv with the template version as the file"
                                         " you provided "
                                         "doesn't work", 'Issue with csv', wx.OK | wx.ICON_WARNING |
                                   wx.OK_DEFAULT)
            value = msg.ShowModal()
            return

        pointList = []
        for i in data.columns[3:]:
            data[i] = data[i].astype(str)

        dlg = wx.ProgressDialog("Upload Progress", "Uploading %s values" % len(data), maximum=len(data),
                                parent=self,
                                style=0 | wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME |
                                      wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)

        keepGoing = True
        for count, row in data.iterrows():
            if not keepGoing:
                break
            try:
                values = row.tolist()
                pointList.append(olv.Points(*values))
                (keepGoing, _) = dlg.Update(count, "%s/%s Objects Uploaded" % (count, len(data)))

            except TypeError as e:
                dlg.Destroy()
                msg = wx.MessageDialog(None, "There was an issue trying to parse your file. "
                                             "Please check to see if there could be more columns or"
                                             " values than"
                                             " the program expects",
                                       'Issue with csv', wx.OK | wx.ICON_WARNING | wx.OK_DEFAULT)
                value = msg.ShowModal()
                return

        dlg.Destroy()
        self.parent.olv.AddObjects(pointList)
        pointList = None
        self.Hide()
        self.parent.Raise()

        event.Skip()
    def onTemplate(self, event):
        """
                DataValues: Floats or -9999 (No data value)
                Date: --+ String
                        |-- Later to be combined into one
                Time: --+ String

                UTFOffSet: -12 - 12
                CensorCode: 'gt|nc|lt|nd|pnq'
                ValueAccuracy: Float
                OffsetValue: Float
                OffsetType: String
                QualifierCode: String

        :param event:
        :return:
        """
        saveFileDialog = wx.FileDialog(self, "Save Bulk Insert Template", "", "", "CSV files (*.csv)|*.csv", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        value = saveFileDialog.ShowModal()
        if value == wx.ID_CANCEL:
            return
        filepath = saveFileDialog.GetPath()
        col = ['DataValue', 'Date', 'Time', 'UTCOffSet', 'CensorCode', 'ValueAccuracy', 'OffSetValue',
               'OffSetType', 'QualifierCode', 'LabSampleCode']
        df = pd.DataFrame(columns=col)
        df.loc[0] = ['FLOAT|INT', 'YYYY-MM-DD', 'HH:MM:SS', 'INT', 'gt|nc|lt|nd|pnq', 'FLOAT', 'FLOAT',
                     'String', 'String', 'String']
        df.loc[1] = ['-9999', '2005-06-29', '14:20:15', '-7', 'nc', "1.2", "1", "NULL", "NULL", "NULL"]
        df.to_csv(filepath, index=False)

        self.Hide()
        self.parent.Raise()

    def onClose(self, event):
        self.Hide()
        self.parent.Raise()

    def checkDataValue(self, item):
        try:
            value = int(item)
            if isinstance(value, int):
                return value
            value = float(item)
            if isinstance(value, float):
                return value
        except:
            return item

    def checkDate(self, item):
        return item

    def checkCensorCode(self, item):
        try:
            return str(item)
        except:
            return item

    def checkLabSample(self, item):
        try:
            return str(item)
        except:
            return "NULL"
    def checkQualifierCode(self, item):
        try:
            return str(item)
        except:
            return "NULL"
    def checkOffsetType(self, item):
        try:
            return str(item)
        except:
            return "NULL"

    def checkOffsetValue(self, item):
        try:
            value = int(item)
            if isinstance(value, int):
                return value
            value = float(item)
            if isinstance(value, float):
                return value
        except:
            return item

    def checkValueAcc(self, item):
        try:
            return str(item)
        except:
            return "NULL"

if __name__ == '__main__':
    app = wx.App(useBestVisual=True)
    m = BulkInsert(None)
    m.Show()
    app.MainLoop()
