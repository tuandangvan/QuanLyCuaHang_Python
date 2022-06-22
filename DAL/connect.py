import mysql.connector
from sqlalchemy import null

def connection():
    conn = mysql.connector.connect(
            host='localhost',
            user='tuandv',
            passwd='12345',
            database='dbs_qlch',
            auth_plugin='mysql_native_password'
    )
    return conn

def ShowDataTable(query, tenSPsearch=null):
    conn = connection()
    cursor = conn.cursor()
    
    if(tenSPsearch==null):
        cursor.execute(query)
    else:
        tenSP = ("%" + tenSPsearch + "%",)
        cursor.execute(query, tenSP)
        
    listdata = cursor.fetchall()
    
    conn.close()
    
    return listdata
  
def Update(query, values):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query,values,)
    conn.commit()
    #     conn.commit()conn.close()  
  
    
    conn.close()

def AddTableCart():
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE giohang( maSP varchar(5) Primary Key, tenSP varchar(50) NOT NULL, giaSP int(10) NOT NULL,"
        +"tenLoai varchar(50) NOT NULL,"
        +"soLuong int(3) NOT NULL,"
        +"thanhTien int(15) NULL,"
        +"FOREIGN KEY (maSP) REFERENCES sanpham(maSP))")
    except:
        conn.rollback()
    
    conn.close()
    
def DeleteTableCart():
    conn = connection()
    cursor = conn.cursor() 
    try:
        cursor.execute("Drop table giohang")
    except:
        conn.rollback()
    
    conn.close()
        
def AddItemCart(maSP, TenSP, giaSP, tenLoai, sl):
    conn = connection()
    thanhTien= sl*int(giaSP)
    cursor = conn.cursor()
    try:
        query = "Insert into giohang(maSP,tenSP,giaSP,tenLoai,soLuong,thanhTien) values (%s,%s,%s,%s,%s,%s)"
    
        
        value = (maSP,TenSP,giaSP,tenLoai,sl,thanhTien)
        cursor.execute(query,value,)
    
        conn.commit()
    except:
        query = "Update giohang SET soLuong = %s, thanhTien = soLuong*giaSP where maSP = %s"
        sl = sl+1
        cursor.execute(query,(sl,maSP),)
        conn.commit()
        
    conn.close()
    