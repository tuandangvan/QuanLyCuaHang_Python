from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
import DAL.connect as connect

dataHoaDon = None
def ShowDbs(query):  
    conn = connect.connection()
    cursor = conn.cursor()
    cursor.execute(query)
    listdata = cursor.fetchall()
    
    conn.close()
    
    return listdata

def HoaDon():
    listData = ShowDbs("Select * from hoadon")
    data_tables = MDDataTable(
        size_hint=(1,1),
        rows_num = 100,
        column_data=[
            ("[size=12]Mã hóa đơn", dp(30)),
            ("[size=12]Ngày xuất hóa đơn", dp(70)),
            ("[size=12]Thành tiền", dp(50)),
        ],
        row_data =  listData,
    )
    dataHoaDon = data_tables
    return data_tables

