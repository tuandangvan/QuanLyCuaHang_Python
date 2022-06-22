
from pickle import NONE
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from matplotlib.pyplot import get
from sympy import root
import DAL.connect as DataMysql

listItemCart = []

def Cart():
    listData = DataMysql.ShowDataTable("select *from giohang")
    listItemCart.clear()
    for i in range(0,len(listData)):
        listItemCart.append(listData[i])
        
    DataTable = MDDataTable(
        size_hint=(1,1),
        rows_num = 10,
        column_data=[
            ("[size=12]Mã SP", dp(15)),
            ("[size=12]Tên SP", dp(40)),
            ("[size=12]Giá", dp(30)),
            ("[size=12]Loại SP", dp(20)),
            ("[size=12]Số lượng", dp(15)),
            ("[size=12]Thành tiền", dp(35)),
            
        ],
        row_data = listData,
    )    

    return DataTable

def Shopping():
    listData = DataMysql.ShowDataTable("Select maSP, tenSP, giaSP, tenLoai from sanpham, phanloai where sanpham.maPhanLoai=phanloai.maPhanLoai")
    data_tables = MDDataTable(
        size_hint=(1,1),
        rows_num = 100,
        column_data=[
            ("[size=12]Mã SP", dp(30)),
            ("[size=12]Tên SP", dp(40)),
            ("[size=12]Giá", dp(30)),
            ("[size=12]Loại SP", dp(50)),
        ],
        row_data =  listData,
        check = True
    )
    data_tables.bind(on_check_press = on_check_press)
    return data_tables

def ListItem():
    listData = DataMysql.ShowDataTable("Select maSP, tenSP, giaSP, tenLoai from sanpham, phanloai where sanpham.maPhanLoai=phanloai.maPhanLoai")
    data_tables = MDDataTable(
        size_hint=(1,1),
        rows_num = 100,
        column_data=[
            ("[size=12]Mã SP", dp(30)),
            ("[size=12]Tên SP", dp(50)),
            ("[size=12]Giá", dp(30)),
            ("[size=12]Loại SP", dp(50)),
        ],
        row_data =  listData,
    )
    return data_tables
def DoanhThu():
    listData = DataMysql.ShowDataTable("Select * from doanhso")
    data_tables = MDDataTable(
        size_hint=(1,1),
        rows_num = 100,
        column_data=[
            ("[size=12]Ngày", dp(50)),
            ("[size=12]Tổng doanh thu", dp(80)),
        ],
        row_data =  listData,
    )
    return data_tables

def SearchItem(tenSP):
    listData = DataMysql.ShowDataTable("Select maSP ,tenSP, giaSP, tenLoai from sanpham,phanloai\
                                        where sanpham.maPhanLoai = phanloai.maphanloai and tenSP LIKE %s",tenSP)
    data_tables = MDDataTable(
        pos_hint = {'center_x':0.5, 'center_y':0.5},
        size_hint= (1,1),
        rows_num = 10,
        column_data=[
            ("[size=12]Mã SP", dp(30)),
            ("[size=12]Tên SP", dp(40)),
            ("[size=12]Giá", dp(30)),
            ("[size=12]Loại SP", dp(50)),
        ],
        row_data =  listData,
        check = True
    )
    data_tables.bind(on_check_press = on_check_press)
    return data_tables

def SearchNgay(ngay):
    listData = DataMysql.ShowDataTable("Select * from doanhso where ngayXuatHD LIKE %s",ngay)
    data_tables = MDDataTable(
        pos_hint = {'center_x':0.5, 'center_y':0.5},
        size_hint= (1,1),
        rows_num = 10,
        column_data=[
            ("[size=12]Ngày", dp(50)),
            ("[size=12]Tổng doanh thu", dp(80)),
        ],
        row_data =  listData,
    )
    return data_tables

def on_check_press(instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        DataMysql.AddItemCart(current_row[0],current_row[1],current_row[2],current_row[3],1)
    
