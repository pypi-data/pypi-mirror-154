"""
@Time ： 2022/5/26 10:58
@Auth ： 朱晓东
@File ：write_excel.py
@IDE ：PyCharm

"""
import xlsxwriter
import xlwt,xlrd,os,sys,re
import xlutils.copy

class WriteExcel():
    def write_excel(self,file_excel):
        file = xlwt.Workbook()
        table = file.add_sheet("功能测试结果", cell_overwrite_ok=True)
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40
        style = xlwt.XFStyle()
        style.borders = borders
        table.write(0, 0, "序号", style)
        table.write(0, 1, "功能点描述", style)
        table.write(0, 2, "开始运行时间", style)
        table.write(0, 3, "结束运行时间", style)
        table.write(0, 4, "测试日期", style)
        table.write(0, 5, "测试结果", style)
        file.save(file_excel)


    def Get_ID(self):
        #用于检查写了几行数据、然后取得后行数
        filepath = self.excel_path
        xlrd.book.ensure_unicode="utf-8"
        data = xlrd.open_workbook(filepath)
        sheet_names = data.sheet_names()
        table = data.sheet_by_index(0)
        self.rows_count = table.nrows #取总行数
        cols_count = table.ncols #取总列数
        ID = table.cell(self.rows_count-1, 0).value  # 获取第x行第一列的值
        # print(ID)
        if ID == "序号":
            Right_ID = 0
            # print(Right_ID)
            return Right_ID
        else:
            # print(ID)
            return ID


    def Check_Date(self):
        #用于检查写了几行数据、然后取得后行数
        filepath = self.excel_path
        xlrd.book.ensure_unicode="utf-8"
        data = xlrd.open_workbook(filepath)
        sheet_names = data.sheet_names()
        table = data.sheet_by_index(0)
        self.rows_count = table.nrows #取总行数
        cols_count = table.ncols #取总列数
        # print(self.rows_count,cols_count)
        return  self.rows_count

    def wtrte_Data(self, Function_point, Start_runtime, End_runtime, Time, Result):
        filepath = sys.argv[0]
        [dirname, filename] = os.path.split(filepath)
        [dirname_real, filename_real] = os.path.split(dirname)
        excelpath = dirname_real + "/test_case_result"
        print(excelpath)
        isExists = os.path.exists(excelpath)
        if not isExists:
            os.makedirs(excelpath)
        filenames = os.listdir(excelpath)
        if filenames == []:
            self.excel_path = dirname_real + "/test_case_result/IHU_result.xls"
            self.write_excel(self.excel_path)
        for filename in filenames:
            # print(filename)
            searchObj = re.search(r'.xls', filename, re.M | re.I)
            if searchObj is not None:
                self.excel_path = excelpath + "/" + filename
                # print(self.excel_path)
                break

        print(self.excel_path)
        self.FP = Function_point
        self.start_runtime = Start_runtime
        self.end_runtime = End_runtime
        self.result = Result
        self.time = Time

        # 格式模板
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40
        style = xlwt.XFStyle()
        style.borders = borders

        rb = xlrd.open_workbook(self.excel_path)
        wb = xlutils.copy.copy(rb)
        table = wb.get_sheet(0)

        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40
        style = xlwt.XFStyle()
        style.borders = borders

        rb = xlrd.open_workbook(self.excel_path)
        wb = xlutils.copy.copy(rb)
        table = wb.get_sheet(0)

        rows = self.Check_Date()
        # print(rows)
        self.num = self.Get_ID()
        num_id = self.num + 1

        table.write(rows, 0, num_id)
        table.write(rows, 1, self.FP)
        table.write(rows, 2, self.start_runtime)
        table.write(rows, 3, self.end_runtime)
        table.write(rows, 4, self.time)
        table.write(rows, 5, self.result)


        # 写数据
        wb.save(self.excel_path)


write_excel = WriteExcel()
