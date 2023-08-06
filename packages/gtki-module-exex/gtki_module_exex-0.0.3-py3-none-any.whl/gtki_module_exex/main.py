from gtki_module_exex.mixins import XlsCreator, TemplateCreator, DataFiller


class CreateExcel(XlsCreator, TemplateCreator, DataFiller):
    def __init__(self, file_name, data_list, column_names=None):
        if column_names:
            self.column_names = column_names
        self.data_list = data_list
        self.file_name = file_name
        self.workbook = self.create_workbook()
        self.worksheet = self.create_worksheet()

    def create_document(self):
        self.create_template()
        row_num = 1
        for row in self.data_list:
            self.create_row(row, row_num)
            row_num += 1
        self.workbook.close()


class CreateExcelActs(CreateExcel):
    def __init__(self, file_name, acts_list, amount_info,
                 column_names=None):
        super().__init__(file_name, acts_list, column_names)
        self.amount_info = amount_info

    def create_amount(self, amount_info):
        merge_format = self.workbook.add_format({'align': 'center',
                                                 'bold': True})
        merge_format.set_font_size(14)
        self.worksheet.merge_range('A2:L2', amount_info, merge_format)

    def create_document(self):
        self.create_template()
        self.create_amount(self.amount_info)
        row_num = 2
        for row in self.data_list:
            self.create_row(row, row_num)
            row_num += 1
        self.workbook.close()
