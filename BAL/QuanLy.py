
from turtle import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from matplotlib.pyplot import box
import DAL.connect as connect

def add_product(self, code, name, price, type):
    if code == "" or name == "" or price == "" or type =="":
        self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Vui lòng nhập đầy đủ thông tin sản phẩm![/color]",
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
        try:
            conn = connect.connection()
            sql = ("insert into sanpham(maSP, tenSP, giaSP, maPhanLoai) values (%s, %s, %s, %s)")
            val = (code,name,price,type)
            cursor = conn.cursor()
            cursor.execute(sql, val)
            conn.commit()
            conn.close()
            self.dialog = MDDialog(
                            title = "Thông Báo",
                            text = "[color=#604ad7]Thêm sản phẩm thành công![/color]",
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
            target = self.ids.ops_fields_p
            target.clear_widgets()
            self.ShowQL()
        except:
            self.dialog = MDDialog(
                            title = "Thông Báo",
                            text = "[color=#604ad7]Mã sản phẩm đã có hoặc không có mã phân loại này![/color]",
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

def update_product(self, code, name, price, type):
    if code == "" or name == "" or price == "" or type =="":
        self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Vui lòng nhập đầy đủ thông tin sản phẩm![/color]",
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
        try:
            conn = connect.connection()
            sql_check=("select * from sanpham where maSP=%s")
            val_check=(code,)
            cursor_check = conn.cursor()
            cursor_check.execute(sql_check, val_check,)
            listdata = cursor_check.fetchall()
            if len(listdata)>0:
                sql = ("update sanpham set tenSP=%s,giaSP=%s,maPhanLoai=%s where maSP=%s")
                val = [name, price, type, code]
                cursor = conn.cursor()
                cursor.execute(sql, val)
                conn.commit()
                conn.close()

                self.dialog = MDDialog(
                                title = "Thông Báo",
                                text = "[color=#604ad7]Cập nhật sản phẩm thành công![/color]",
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
                target = self.ids.ops_fields_p
                target.clear_widgets()
                self.ShowQL()
            else:
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
        except:
            self.dialog = MDDialog(
                            title = "Thông Báo",
                            text = "[color=#604ad7]Không tìm thấy loại sản phẩm này![/color]",
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

def remove_product(self, code):
    if code == "":
        self.dialog = MDDialog(
                    title = "Thông Báo",
                    text = "[color=#604ad7]Vui lòng nhập mã sản phẩm cần xóa![/color]",
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
        try:
            conn = connect.connection()
            sql_check=("select * from sanpham where maSP=%s")
            val_check=(code,)
            cursor_check = conn.cursor()
            cursor_check.execute(sql_check, val_check,)
            listdata = cursor_check.fetchall()
            if len(listdata)>0:
                sql = ("delete from sanpham where maSP = %s")
                val = (code,)
                cursor = conn.cursor()
                cursor.execute(sql, val)
                conn.commit()
                conn.close()

                self.dialog = MDDialog(
                                title = "Thông Báo",
                                text = "[color=#604ad7]Xóa sản phẩm thành công![/color]",
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
                target = self.ids.ops_fields_p
                target.clear_widgets()
                self.ShowQL()
            else:
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
        except:
            self.dialog = MDDialog(
                            title = "Thông Báo",
                            text = "[color=#604ad7]Không tìm thấy loại sản phẩm này![/color]",
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