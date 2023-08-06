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
