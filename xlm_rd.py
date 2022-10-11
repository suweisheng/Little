# encoding: utf8

import xlrd
import xlwt
import xlsxwriter
import datetime
# lwt只能写.xls文件，存储的数量非常少;
# xlsxwriter只能写.xlsx文件,可以存储100万条记录

# xlrd cell datatype
# XL_CELL_EMPTY	0	empty string ''
# XL_CELL_TEXT	1	a Unicode string
# XL_CELL_NUMBER	2	float
# XL_CELL_DATE	3	float
# XL_CELL_BOOLEAN	4	int; 1 means TRUE, 0 means FALSE
# XL_CELL_ERROR	5

def test_xlrd():
    # 官方文档：https://xlrd.readthedocs.io/en/latest/ 支持 xls, xlsb, xlsx, ods
    # ===============  workbook
    filename = "xlrdtest.xlsx"
    logfile = "" # 日志文件, verbosity
    file_contents = "xx" # 存在时忽略filename
    formatting_info = False # 是否加载单元格格式信息，关闭可以节省内存，提高性能
    on_demand = False # 控制工作表是在最初加载还是在调用者要求时加载
    ragged_rows = False # 默认值为 False 表示所有行都用空单元格填充，以便所有行的大小与 ncols 中的大小相同
    ignore_workbook_corruption = False # 允许读取损坏的工作簿

    workbook = xlrd.open_workbook(filename=filename, ragged_rows=ragged_rows) # 打开工作簿，返回 xlrd.book.book对象

    print workbook
    # print workbook.user_name # 最后修改文件的作者
    # print workbook.nsheets # 工作表数量

    sheet_list = workbook.sheets() # 获取所有工作表对象
    sheetname_list = workbook.sheet_names() # 获取所有工作表对象

    sheet = workbook.sheet_by_index(0) # 获取指定工作表 索引
    sheet = workbook.sheet_by_name(u"Sheet1") # 获取指定工作表 名称

    workbook.unload_sheet(sheet_name_or_index=2) # 卸载指定工作表
    is_has = workbook.sheet_loaded(sheet_name_or_index=2) # 查询是否有对应工作表

    # ===============  sheet
    # 一般不会手动实例化这个类。您可以通过调用 xlrd.open_workbook() 时返回的 Book 对象访问 Sheet 对象
    # sheet = xlrd.sheet.Sheet(book=workbook, position=0, name="Sheet1", number=1)
    sheet = workbook.sheet_by_name(u"Sheet1")
    print sheet

    # rowx 是行索引，从零开始计数，colx 是列索引，从零开始计数
    # print sheet.nrows, sheet.ncols # 有效行、列数
    # print sheet.col(colx=0) # 获取指定列中 Cell 对象的序列 len 为 ncols
    # print sheet.row(rowx=6) # 获取指定行中 Cell 对象的序列 len 为 nrows
    # print sheet.book # 所属工作簿对象
    # print sheet.name # 工作表名称
    # print sheet.visibility # 工作表是否可见 0可见, 1隐藏
    # print sheet.cell(rowx=3, colx=1) # 获取单元格对象
    # print sheet.cell_value(rowx=3, colx=1) # 获取单元格内容
    # print sheet.cell_type(rowx=3, colx=1) # 获取单元格数据类型
    # print sheet.row_len(rowx=1) # 该行有效单元格数量, ragged_rows=true才生效, 否则时永远等于ncols
    # print sheet.get_rows() # 迭代器，可以迭代每一行

    # print sheet.row_values(rowx=3, start_colx=0, end_colx=3) # 获取某行的cell内容切片, 类似row[start_colx:end_colx]
    # print sheet.row_types(rowx=3, start_colx=0, end_colx=3) # 获取某行的cell类型切片, array('B', [0, 1, 1])
    # print sheet.row_slice(rowx=3, start_colx=0, end_colx=3) # 获取某行的cell对象切片
    # print sheet.col_values(colx=3, start_rowx=0, end_rowx=3) # 获取某列的cell内容切片, 类似row[start_rowx:end_rowx]
    # print sheet.col_types(colx=3, start_rowx=0, end_rowx=3) # 获取某列的cell类型切片, array('B', [0, 1, 1])
    # print sheet.col_slice(colx=3, start_rowx=0, end_rowx=3) # 获取某列的cell对象切片


    # ===============  cell
    # 一般不会手动实例化这个类。您可以通过调用 xlrd.open_workbook() 时返回的 Book 对象访问 Sheet 对象
    # cell = xlrd.sheet.Cell(ctype=xlrd.XL_CELL_TEXT, value="value", xf_index=None)
    cell = sheet.cell(rowx=3, colx=1)
    print cell.value # 单元格内容
    print cell.ctype # 单元格数据类型

def test_xlsxwriter():
    # 官方文档: https://xlsxwriter.readthedocs.io/
    filename = 'xlsxwriter.xlsx'
    sheetname = "haha"
    # ============================ book
    # strings_to_numbers  worksheet.write(), 将字符串数字写入时转数字类型, 默认false
    # strings_to_formulas worksheet.write(), 将字符串写入时转公式, 默认true
    # strings_to_urls worksheet.write(), 将字符串写入时转url, 默认true
    workbook  = xlsxwriter.Workbook(filename, {'strings_to_numbers': False}) # 创建新文件

    # 工作表属性
    workbook.set_properties({
        'title':    'This is an example spreadsheet',
        'subject':  'With document properties',
        'author':   'John McNamara',
        'manager':  'Dr. Heinz Doofenshmirtz',
        'company':  'of Wolves',
        'category': 'Example spreadsheets',
        'keywords': 'Sample, Example, Properties',
        'created':  datetime.date(2018, 1, 1),
        'comments': 'Created with Python and XlsxWriter'
    })
    workbook.set_custom_property('Reference number', 1.2345)
    workbook.set_custom_property('Has review',       True)
    workbook.set_custom_property('Signed off',       False)

    # workbook.read_only_recommended() # 设置工作簿只读

    cell_format = workbook.add_format({"font_color":'red'}) # 创建单元格格式化对象,这些对象用于将格式应用于单元格
    # 字体、颜色、图案、边框、对齐方式和数字格式, 如'num_format': '$#,##0.00'
    # https://xlsxwriter.readthedocs.io/format.html#format
    cell_format.set_bold() # 加粗
    cell_format.set_font_color('red')
    cell_format.set_font_name('Times New Roman')

    # ============================ sheet
    worksheet = workbook.add_worksheet(sheetname) # haha
    # worksheet = workbook.add_worksheet() # Sheet2
    worksheet = workbook.get_worksheet_by_name(sheetname)
    worksheet_list = workbook.worksheets() # 工作表对象列表

    # worksheet.get_name() # 工作表名称
    # worksheet.activate() # 使工作表激活可见
    # worksheet.hide() # 使工作表隐藏
    # worksheet.select() # 使工作表选中
    # worksheet.set_first_sheet()


    # row col 从0开始
    worksheet.write(0, 0, 'Hello Excel') # worksheet.write('A1', 'Hello world')
    worksheet.write("A1", 'Foo', cell_format)
    worksheet.write_string("A3", 'Bar', cell_format)
    worksheet.write_number(2, 3, 3, cell_format)
    worksheet.write_blank (3, 4, '', cell_format)
    worksheet.write_formula(2, 0, '=SUM(B1:B5)')
    worksheet.write_url('A2', 'https://www.python.org/')

    # 为某行或某列设置格式, 参数后面有可选参数hidden,level,collapsed
    worksheet.set_row(row=0, height=10, cell_format=cell_format) 
    worksheet.set_column('A:D', 20, cell_format)
    worksheet.set_column(first_col=0, last_col=3, width=20,cell_format=cell_format)


    def write_uuid(worksheet, row, col, uuid, format=None):
        string_uuid = str(uuid)
        return worksheet.write_string(row, col, string_uuid, format)

    worksheet.add_write_handler(str, write_uuid)
    worksheet.write(0, 0, 'Hello Excel')
    worksheet.write_array_formula('A1:A3', '{=TREND(C1:C3,B1:B3)}')
    worksheet.write_rich_string(0, 0, 'This is ', 'red', 'bold') # 富文本

    worksheet.write_row("A1", [1,2,3,4,4]) # 一次性写一行
    worksheet.write_row(0, 0, [1,2,3,4,4]) # 一次性写一列
    worksheet.write_comment('A1', 'This is a comment') # 写注释

    # 合并单元格
    merge_format = workbook.add_format({'align': 'center'})
    # worksheet.merge_range(2, 1, 3, 3, 'Merged Cells', merge_format)
    # worksheet.merge_range('D22:G25',    'Merged Cells', merge_format)

    # worksheet.autofilter('A1:D11') # 加数据筛选
    # worksheet.filter_column('A', 'x > 2000')

    
    # worksheet.set_selection('G7:D4') # 选中单元格

    # worksheet.hide_zero() # 隐藏工作表中的零值


    workbook.close()






# test_xlrd()
test_xlsxwriter()