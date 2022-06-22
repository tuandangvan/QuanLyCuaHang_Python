from datetime import date
from re import S
import sys
from kivy.lang import  Builder
from kivymd.app import MDApp
from kivy.core.window import  Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.label import MDLabel
from sqlalchemy import null
import BAL.HandleData as HandleData
import DAL.connect as connect
import BAL.QuanLy as QuanLy
import BAL.HoaDon as HoaDon
import matplotlib.pyplot as plt

DATA_TABLE_CART = None


class FormLogin(Screen):
    def signup(self):
        self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Bạn không thể tạo tài khoản!\nHãy đăng nhập bằng tài khoản Administrator và thử lại nhé!\n[/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                    )
        self.dialog.open()
    
    def check_data_login(self):
        signinUser = self.ids.login_user.text
        signinPassword = self.ids.login_password.text

        conn = connect.connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM taikhoan where  tenTaiKhoan= %s and matKhau=%s"
        adr = (signinUser,signinPassword,)
        cursor.execute(sql,adr)
        temp = cursor.fetchall()
        cursor.close()

        if(len(temp) > 0):
            global user, typeUser
            user = (temp[0])[0]
            typeUser = (temp[0])[2]
            self.manager.current = "main"
            self.manager.transition.direction = "up"  
            self.ids.login_user.text = signinUser
            self.ids.login_password.text = ""
        else:
            self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Sai tài khoản hoặc mật khẩu vui lòng thử lại![/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                    )
            self.dialog.open()
            self.ids.login_user.text = signinUser
            self.ids.login_password.text = ""

class FormSignup(Screen):
    def signup_acc(self):
        signupUser = self.ids.signup_user.text
        signupPassword = self.ids.signup_password.text
        signupConfirmPassword =  self.ids.signup_confirmpassword.text

        if signupUser == "" or signupPassword == "" or signupConfirmPassword == "":
            self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Vui lòng nhập đầy đủ thông tin![/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                    )
            self.dialog.open()
        elif signupPassword != signupConfirmPassword:
            self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Mật khẩu không trùng khớp![/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                    )
            self.dialog.open()
        else:
            conn = connect.connection()
            cursor = conn.cursor()

            sql = "SELECT * FROM taikhoan where tenTaiKhoan = %s"
            adr = (signupUser,)
            cursor.execute(sql,adr)
            if(len(cursor.fetchall()) > 0):
                self.dialog = MDDialog(
                        title = "Thông Báo",
                        text = "[color=#604ad7]Tên tài khoản đã tồn tại![/color]",
                        pos_hint = {'center_x':.5, 'center_y':.5},
                        buttons=[
                            MDFlatButton(
                                text="OK",
                                theme_text_color="Custom",
                                on_press = lambda x: self.dialog.dismiss(),
                            ),
                        ],
                        )
                self.dialog.open()
                
            else:
                sql = "INSERT INTO taikhoan (tenTaiKhoan, matKhau, typeUser) VALUES (%s, %s,'NV')"
                val = (signupUser, signupPassword)
                cursor.execute(sql, val)
                conn.commit() 
                self.dialog = MDDialog(
                        title = "Thông Báo",
                        text = "[color=#604ad7] Tạo tài khoản thành công![/color]",
                        pos_hint = {'center_x':.5, 'center_y':.5},
                        buttons=[
                            MDFlatButton(
                                text="OK",
                                theme_text_color="Custom",
                                on_press = lambda x: self.dialog.dismiss(),
                            ),
                        ],
                        )
                self.ids.signup_user.text = ""
                self.ids.signup_password.text =""
                self.ids.signup_confirmpassword.text =""
                self.dialog.open()
                self.manager.current = "login"
                self.manager.transition.direction = "up"  
            cursor.close()

class FormChangePassword(Screen):
    def change_acc(self):
        newPassword =  self.ids.change_password.text
        confirmPassword =  self.ids.change_confirmpassword.text
        if newPassword == confirmPassword:
            conn = connect.connection()
            cursor = conn.cursor()
            sql = "UPDATE taikhoan set matKhau = %s where tenTaiKhoan = %s"
            adr = (newPassword,user,)
            cursor.execute(sql,adr)
            conn.commit()
            conn.close()
             
            self.dialog = MDDialog(
                        title = "Thông Báo",
                        text = "[color=#604ad7] Đổi mật khẩu thành công![/color]",
                        pos_hint = {'center_x':.5, 'center_y':.5},
                        buttons=[
                            MDFlatButton(
                                text="OK",
                                theme_text_color="Custom",
                                on_press = lambda x: self.dialog.dismiss(),
                            ),
                        ],
                        ) 
            self.dialog.open()
            self.ids.change_password.text = ""
            self.ids.change_confirmpassword.text = ""
            self.manager.current = "main"
            self.manager.transition.direction = "up"

class WindowManager(ScreenManager):
    pass

class Cart(Screen):
    def ListCart(self):
        boxCart = self.ids.boxCart
        listdata = HandleData.Cart()
        DATA_TABLE_CART = listdata
        boxCart.clear_widgets()
        boxCart.add_widget(DATA_TABLE_CART)

        
    def Pay(self):
        sumPrice = 0
        for i in range(0,len(HandleData.listItemCart)):
            sumPrice+= int((HandleData.listItemCart[i])[5])

        boxPay = self.ids.boxPay
        boxPay.clear_widgets()
        boxPay.add_widget(
            MDLabel(
                text = "Thành tiền........................................................." 
                        +str(sumPrice),
                halign="center",
                font_style = 'Subtitle1'

            )  
        )
        
        return sumPrice

    def UpdateItem(self, maSP, sl,widget):
        try:
            con = connect.connection()
            cursor = con.cursor()
            sql = "select * from giohang where maSP = %s"
            val = (maSP,)
            cursor.execute(sql,val)
            a = cursor.fetchall()
            if(len(a)==0):
                self.dialog = MDDialog(
                title = "Thông Báo",
                text = "[color=#604ad7]Không tìm thấy mã sản phẩm này![/color]",
                pos_hint = {'center_x':.5, 'center_y':.5},
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                )
                self.dialog.open()
            else:
                value = (int(sl),maSP)
                query = ("Update giohang SET soLuong = %s, thanhTien = soLuong*giaSP where maSP = %s")
                connect.Update(query,value)
                widget.clear_widgets()
                self.ListCart()
                self.Pay()
            con.close()
        except:
            self.dialog = MDDialog(
                title = "Thông Báo",
                text = "[color=#604ad7]Vui lòng nhập số lượng![/color]",
                pos_hint = {'center_x':.5, 'center_y':.5},
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                )
            self.dialog.open()
        
    def DeleteItem(self, maSP, widget):
        query = "Delete from giohang where maSP = %s"
        connect.Update(query,(maSP,))
        widget.clear_widgets()
        self.ListCart()
        self.Pay()
        
    def UpdateBtn(self):
        item = self.ids.payCart
        item.clear_widgets()
        
        txt_code = TextInput(hint_text='Mã sản phẩm',multiline=False)
        txt_number = TextInput(hint_text='Số lượng sản phẩm',multiline=False)
        btn_update = Button(text="Cập nhật",on_release=lambda x: self.UpdateItem(txt_code.text,txt_number.text,item))
        btn_delete = Button(text='Xóa',on_release=lambda x: self.DeleteItem(txt_code.text,item))
        item.add_widget(txt_code)
        item.add_widget(txt_number)
        item.add_widget(btn_update)
        item.add_widget(btn_delete)
        
    def ResetCart(self):
        connect.DeleteTableCart()
        connect.AddTableCart()

    def add_HoaDon(self):
        if(len(HandleData.listItemCart)==0):
            self.dialog = MDDialog(
                title = "Thông Báo",
                text = "[color=#604ad7]Giỏ hàng bạn không có sản phẩm nào![/color]",
                pos_hint = {'center_x':.5, 'center_y':.5},
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                )
            self.dialog.open()
        else:
            sumPrice = self.Pay()
            conn = connect.connection()
            cursor = conn.cursor()
            sql = "INSERT into hoadon (ngayXuatHD,thanhtien) VALUES (now(),%s)"
            cursor.execute(sql,(sumPrice,))
            conn.commit()
            conn.close()
            self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Thanh toán thành công![/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                            ),
                        ],
                    )
            self.dialog.open()

    def tong_DoanhSo(self):
        conn = connect.connection()
        cursor = conn.cursor()
        sql = "SELECT DATE(ngayXuatHD), SUM(thanhTien) FROM hoadon GROUP BY DATE(ngayXuatHD)"
        cursor.execute(sql)
        a=cursor.fetchall()
        for i in range(0,len(a)):
            date = (a[i])[0]
            sumPrice = (a[i])[1]
            try:
                sql_is = "insert into doanhso(ngayXuatHD,tongTien) values (DATE(%s),%s)"
                val = (date,sumPrice,)
                cursor.execute(sql_is,val)
            except:
                sql_is = "update doanhso set tongTien=%s where ngayXuatHD=%s"
                val = (sumPrice,date,)
                cursor.execute(sql_is,val)
            conn.commit()

        conn.close()
        

class QLMatHang(Screen):

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Mã sản phẩm',multiline=False)
        crud_name = TextInput(hint_text='Tên sản phẩm',multiline=False)
        crud_price = TextInput(hint_text='Giá',multiline=False)
        crud_type = TextInput(hint_text='Loại sản phẩm',multiline=False)
        crud_submit = Button(text='Thêm',size_hint_x=None,width=100,on_release=lambda x: QuanLy.add_product(self,crud_code.text,crud_name.text,crud_price.text,crud_type.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_type)
        target.add_widget(crud_submit)
    
    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Mã sản phẩm',multiline=False)
        crud_name = TextInput(hint_text='Tên sản phẩm',multiline=False)
        crud_price = TextInput(hint_text='Giá',multiline=False)
        crud_type = TextInput(hint_text='Loại sản phẩm',multiline=False)
        crud_submit = Button(text='Cập nhật',size_hint_x=None,width=100,on_release=lambda x: QuanLy.update_product(self,crud_code.text,crud_name.text,crud_price.text,crud_type.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_type)
        target.add_widget(crud_submit)


    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Mã sản phẩm')
        crud_submit = Button(text='Xóa',size_hint_x=None,width=100,on_release=lambda x: QuanLy.remove_product(self,crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)


    def ShowQL(self):
        boxQL = self.ids.boxQL
        dt1 = HandleData.ListItem()
        boxQL.clear_widgets()
        boxQL.add_widget(dt1)
  
    

class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    pass

class FormMain(Screen):
    def check_admin(self):
        if user == "admin" and typeUser == "AD":
            self.manager.current = "signup"
            self.manager.transition.direction = "left"
        else:
            self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Bạn không thể tạo tài khoản!\nHãy đăng nhập bằng tài khoản Administrator và thử lại nhé![/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                    )
            self.dialog.open()
    def ShowSearchItem(self):
        boxShop = self.ids.boxShop
        if(self.ids.txtSearch.text!=null):
            listdata  = HandleData.SearchItem(self.ids.txtSearch.text)
        else:
            listdata = HandleData.Shopping()
        
        boxShop.clear_widgets()
        boxShop.add_widget(listdata)

        
    def ShowShopping(self):
        boxShop = self.ids.boxShop
        dt = HandleData.Shopping()

        boxShop.clear_widgets()
        boxShop.add_widget(dt)
     

    def ShowHoaDon(self):
        boxHD = self.ids.boxHD
        dt = HoaDon.HoaDon()
        boxHD.clear_widgets()
        boxHD.add_widget(dt)

    def ShowDoanhThu(self):
        boxSales = self.ids.boxSales
        dt = HandleData.DoanhThu()
        boxSales.clear_widgets()
        boxSales.add_widget(dt)

    def ShowSearchNgay(self):
        boxSales = self.ids.boxSales
        if(self.ids.txtgroud.text!=null):
            listdata  = HandleData.SearchNgay(self.ids.txtgroud.text)
        else:
            listdata = HandleData.DoanhThu()
        
        boxSales.clear_widgets()
        boxSales.add_widget(listdata)
    
    def Sale_Chart(self):
        conn = connect.connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM doanhso"
        cursor.execute(sql)
        a=cursor.fetchall()
        date= []
        sumPrice = []
        for i in range(0,len(a)):
            date.append(str((a[i])[0]))
            sumPrice.append((a[i])[1])
        width = 0.30
        plt.bar(date, sumPrice, width,color = 'hotpink')
        plt.title('Doanh thu theo ngày')
        plt.xlabel('Ngày')
        plt.ylabel('Doanh Thu/Ngày')
        plt.show()

class ManageStore(MDApp):
    def build(self):
        return Builder.load_file("ManagerStore.kv")

    def set_screen(self, screen_name, direction):
        self.root.current = screen_name
        self.root.transition.direction = direction

    
    def check_user(self):
        if user == "admin" and typeUser == "AD":
            self.root.current = "scrn_product_content"
            self.root.transition.direction = "left"
        else:
            self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Bạn không có quyền truy cập!\nVui lòng đăng nhập bằng tài khoản Administrator![/color]",
                    pos_hint = {'center_x':.5, 'center_y':.5},
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            on_press = lambda x: self.dialog.dismiss(),
                        ),
                    ],
                    )
            self.dialog.open()
            

        

if '__main__' == __name__:
    ManageStore().run()
