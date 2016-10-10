import wx
from odmtools.view.WizardVariableView import WizardVariableView
from wx.wizard import WizardPageSimple
from odmtools.odmdata import Variable


class WizardVariableController(WizardPageSimple):
    def __init__(self, parent, service_manager, current_variable):
        WizardPageSimple.__init__(self, parent)

        self.service_manager = service_manager
        self.current_variable = current_variable
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.variable_view = WizardVariableView(self)
        main_sizer.Add(self.variable_view, 1, wx.EXPAND | wx.RIGHT, -16)
        self.SetSizer(main_sizer)

        table_columns = ["Code", "Name", "Speciation", "Units",
                         "Sample Medium", "Value Type", "IsRegular", "Time Support",
                         "Time Units", "DataType", "Genaral Category", "NoDataValue", "ID"]
        self.variable_view.variable_table.set_columns(table_columns)
        self.on_current_radio(None)

        self.__fetch_data()
        self.variable_view.current_variable_radio.Bind(wx.EVT_RADIOBUTTON, self.on_current_radio)
        self.variable_view.existing_variable_radio.Bind(wx.EVT_RADIOBUTTON, self.on_existing_radio)
        self.variable_view.create_variable_radio.Bind(wx.EVT_RADIOBUTTON, self.on_create_radio)

    def on_current_radio(self, event):
        self.variable_view.variable_table.Enable(False)
        self.__set_create_variable_section(False)

    def on_create_radio(self, event):
        self.variable_view.variable_table.Enable(False)
        self.__set_create_variable_section(True)

    def on_existing_radio(self, event):
        self.variable_view.variable_table.Enable(True)
        self.__set_create_variable_section(False)

    def __set_create_variable_section(self, active):
        if not isinstance(active, bool):
            raise Exception("active must be type bool")

        self.variable_view.variable_code_text_ctrl.Enable(active)
        self.variable_view.variable_name_combo.Enable(active)
        self.variable_view.variable_type_combo.Enable(active)
        self.variable_view.no_data_value_text_ctrl.Enable(active)
        self.variable_view.speciation_combo.Enable(active)
        self.variable_view.definition_text_ctrl.Enable(active)

    def __fetch_data(self):
        self.__populate_variable_table()

        cv_service = self.service_manager.get_cv_service()
        name_list = [x.term for x in cv_service.get_variable_name_cvs()]
        var_unit = [x.name for x in cv_service.get_units_names()]
        spec_list = [x.term for x in cv_service.get_speciation_cvs()]

        self.variable_view.variable_name_combo.AppendItems(name_list)
        self.variable_view.speciation_combo.AppendItems(spec_list)
        self.variable_view.variable_type_combo.AppendItems(var_unit)

    def __populate_variable_table(self):
        series_serivce = self.service_manager.get_series_service()
        variables = series_serivce.get_all_variables()
        data = []
        for var in variables:
            data.append([var.code,
                         var.name,
                         var.speciation,
                         var.variable_unit.name,
                         var.sample_medium,
                         var.value_type,
                         var.is_regular,
                         var.time_support,
                         var.time_unit.name,
                         var.data_type,
                         var.general_category,
                         var.no_data_value,
                         var.id])

        self.variable_view.variable_table.set_table_content(data=data)

    def get_variable(self):
        v = Variable()
        if self.variable_view.current_variable_radio.GetValue():
            v = self.current_variable
        elif self.variable_view.existing_variable_radio.GetValue():
            row = self.variable_view.variable_table.get_selected_row()
            code = row[0]
            v = self.service_manager.get_series_service().get_variable_by_code(code)

        elif self.variable_view.create_variable_radio.GetValue():
            # v = self.createdVar
            pass

        return v





