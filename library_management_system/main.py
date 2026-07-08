import pymysql
import sqlite3 
import string
import pyqtgraph as pg
import pandas as pd 
import random as ra

from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools, QtMultimedia
from PySide2.QtCore import QUrl
    
class MyWidget (QtWidgets.QWidget) :
    def __init__(self) :
        super().__init__()
        
        self.initDataBase()
        self.PlayMusic()
        
        self.ui_login = QtUiTools.QUiLoader().load("login.ui")

        self.ui_login.stackedWidget.setCurrentWidget(self.ui_login.page_login)
        # self.ui_login.resize(891, 621)
        self.ui_login.pushButton_register.clicked.connect(self.GoRegisterPage)
        self.ui_login.pushButton_back.clicked.connect(self.GoLoginPage)

        self.ui_login.pushButton_submit.clicked.connect(self.onRegjster)
        self.ui_login.pushButton_login.clicked.connect(self.onLongin)
        self.ui_login.pushButton_back.clicked.connect(self.GoLoginPage1)
        self.ui_login.pushButton_yz.clicked.connect(self.yz)
        self.ui_login.pushButton_yz.setText('6M44bn')

    #获取注册用户名称
    def onRegjster(self) :
        name = self.ui_login.lineEdit_name.text()
        reg_pass = self.ui_login.lineEdit_reg_pass.text()
        reg_pass1 = self.ui_login.lineEdit_reg_pass1.text()
        real_name = self.ui_login.lineEdit_real_name.text()
        phone = self.ui_login.lineEdit_phone.text()
        stu_id = self.ui_login.lineEdit_stu_id.text()

        print(stu_id)

        if name == "" or reg_pass == "" or reg_pass1 == "" or real_name == "" or phone == "" or stu_id == "":
            QtWidgets.QMessageBox.warning(self, "警告", "信息未填写完全!请重新填写")
            return
        # else :
        if reg_pass != reg_pass1 :
            QtWidgets.QMessageBox.warning(self, "警告", "两次密码不一致!请重新填写")
            return 
        
        if self.doRegister(name, reg_pass, real_name, phone, stu_id) :
            QtWidgets.QMessageBox.information(self, "提示", "注册成功!")
        else :
            QtWidgets.QMessageBox.information(self, "提示", "注册失败!")

    def onLongin(self) :
        id = self.ui_login.lineEdit_id.text()
        ps = self.ui_login.lineEdit_ps.text()
        yzm = self.ui_login.lineEdit_ps_2.text()
        sure = self.ui_login.pushButton_yz.text()

        # print(yzm, self.s)
        if id == "" or ps == "" :
            QtWidgets.QMessageBox.critical(self, "错误", "登录失败!")
            return 
        if yzm != sure :
            QtWidgets.QMessageBox.critical(self, "错误", "验证码错误!")
            return
        if not self.doLogin(id, ps) :
            QtWidgets.QMessageBox.critical(self, "错误", "登录失败!")

        
    
        QtUiTools.QUiLoader().registerCustomWidget(pg.PlotWidget)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        self.main_ui = QtUiTools.QUiLoader().load("main.ui")
        
        self.x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #x轴
        self.y = [130, 132, 134, 132, 133,131, 129, 132, 135, 145]#y轴
        
        pen = pg.mkPen(color=(0, 255, 255), width=2, style=QtCore.Qt.SolidLine)
        
        styles ={'color':'r' , 'font-size':'15px'} # 设置标签的颜色和大小
        self.main_ui.widget_plot.setLabel('bottom'  , '借阅时间' , **styles)
        self.main_ui.widget_plot.setLabel('left'  , '人数' , **styles)

        self.main_ui.widget_plot.showGrid(x = True, y = True)
        self.main_ui.widget_plot.setTitle('借阅人数')
        # self.main_ui.widget_plot.getPlotItem().getAxis('bottom').setTicks([list(enumerate(self.x))])
        self.main_ui.widget_plot.plot(self.x, self.y, pen = pen, symbol = 'o')

        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.page_welcome)

        self.main_ui.toolButton_user.clicked.connect(self.GoUserPage)
        self.main_ui.toolButton_book.clicked.connect(self.GoBookPage)
        self.main_ui.toolButton_borrow.clicked.connect(self.GoBorrowPage)
        self.main_ui.toolButton_back.clicked.connect(self.GoLoginPage)

        self.main_ui.pushButton_query_user.clicked.connect(self.QueryUser)
        self.main_ui.pushButton_modify_user.clicked.connect(self.ModifyUser)
        self.main_ui.pushButton_delete_user.clicked.connect(self.DeleteUser)
        self.main_ui.pushButton_modify_pwd.clicked.connect(self.ModifyPwd)
        self.main_ui.pushButton_query_book.clicked.connect(self.QueryBook)
        self.main_ui.pushButton_add_book.clicked.connect(self.OnBook)
        self.main_ui.pushButton_delete_book.clicked.connect(self.DelBook)
        self.main_ui.pushButton_borrow.clicked.connect(self.BrrowBook)
        self.main_ui.pushButton_query_all.clicked.connect(self.QuertAll)
        self.main_ui.pushButton_query.clicked.connect(self.QueryBorrow)
        self.main_ui.pushButton_modify_book.clicked.connect(self.ModifyBook)
        self.main_ui.pushButton_return.clicked.connect(self.ReturnBook)
        self.main_ui.pushButton_add_all.clicked.connect(self.AddAllBook)

        if self.login_user_role == '普通用户' :
            self.main_ui.lineEdit_user.hide()
            self.main_ui.pushButton_query_user.hide()
            self.main_ui.pushButton_modify_user.hide()
            self.main_ui.pushButton_delete_user.hide()
            self.main_ui.toolButton_book.hide()
            self.main_ui.toolButton_4.hide()
            self.main_ui.toolButton_5.hide()


        self.main_ui.show()
        self.ui_login.close()
    #跳转user界面    
    def GoUserPage(self) :
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.page_user)
        pass
    #跳转book界面
    def GoBookPage(self) :
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.page_book)
        pass
    #跳转brrow界面
    def GoBorrowPage(self) :
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.page_borrow)
        pass
    #点击注册 -> 跳转到注册页面
    def GoRegisterPage(self) :
        self.ui_login.stackedWidget.setCurrentWidget(self.ui_login.page_register)
        #设置注册页面高度
        pass
    def GoLoginPage1(self) :
        self.ui_login.stackedWidget.setCurrentWidget(self.ui_login.page_login)
        #设置注册页面高度
        pass
    #点击返回 -> 回到登录页面
    def GoLoginPage(self) :
        self.ui_login.show()
        self.main_ui.close()
        pass
    
    #自动播放音乐
    def PlayMusic(self) :
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile("D:\py_project\image\岑宁儿 - 追光者.mp3")))
        self.player.play()
        
    #初始化数据库(游标对象执行sql语句)
    def initDataBase(self) :
        self.sql = sqlite3.connect("book.db")
        self.cursor = self.sql.cursor()
        self.cursor.execute("create table if not exists user(name varchar(15), passWord varchar(15), realName varchar(15), phone char(11), stu_id char(13) primary key, role varchar(15))")
        self.cursor.execute("create table if not exists t_book(isbn varchar(13) primary key, title varchar(100), author varchar(60), publisher varchar(100), publishdate varchar(10), number int)")
        self.cursor.execute("create table if not exists t_borrow(user_id char(13), book_isbn varchar(13), borrow_date char(10), return_date char(10), time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, primary key(user_id, book_isbn, time), foreign key(user_id) references user, foreign key(book_isbn) references t_book)")
    #注册
    def doRegister(self, name, reg_pass, real_name, phone, stu_id) :
        sql = f"insert into user values('{name}', '{reg_pass}', '{real_name}', '{phone}', '{stu_id}', '普通用户')"
        try :
            self.cursor.execute(sql)
            self.sql.commit()
        except sqlite3.Error as e :
            print("insert error:", e)
            return False
        return True
    #登录
    def doLogin(self, id, passWord) :
        self.cursor.execute(f"select stu_id, name, passWord, role from user where name = '{id}' and passWord = '{passWord}'")
        record = self.cursor.fetchone()
        
        if record is None:
            return False
        
        self.login_user_id = record[0]
        self.login_user_name = record[1]
        self.login_user_role = record[3]
        print(self.login_user_role)

        return True
    #查询用户
    def QueryUser(self) :
        judge = self.main_ui.lineEdit_user.text()
        print(judge)
        sql = f"select * from user where name like '%{judge}%'"
        # print(sql)
        self.cursor.execute(sql)
        #获取结果
        res = self.cursor.fetchall()
        #建立模型
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['用户名称', '密码', '真实姓名', '联系方式', '学号', '用户权限'])
        for i in range(len(res)) :
            for j in range(6) :
                item = QtGui.QStandardItem(res[i][j])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        self.main_ui.tableView_user.setModel(model)
    #删除用户
    def DeleteUser(self) :
        row = self.main_ui.tableView_user.currentIndex().row()
        model = self.main_ui.tableView_user.model()
        id = model.item(row, 0).text()
        if row == -1 :
            return
        # print(id)
        choose = QtWidgets.QMessageBox.question(self, "删除", f"是否确认删除{id}?")
        print(choose)
        # PySide2.QtWidgets.QMessageBox.StandardButton.Yes
        if choose is QtWidgets.QMessageBox.StandardButton.No :
            return
        sql = f"delete from user where name = '{id}'"
        # print(sql)
        self.cursor.execute(sql)
        self.sql.commit()
        if self.cursor.rowcount == 1 :
            QtWidgets.QMessageBox.information(self, "提示", "删除成功!")
        else :
            QtWidgets.QMessageBox.critical(self, "错误", "删除失败!")        
    #修改用户信息
    def ModifyUser(self) :
        row = self.main_ui.tableView_user.currentIndex().row()
        if row == -1 :
            return
        model = self.main_ui.tableView_user.model()
        id = model.item(row, 4).text()
        Rname = model.item(row, 2).text()
        pwd = model.item(row, 1).text()
        phone = model.item(row, 3).text()
        user = model.item(row, 0).text()
        role = model.item(row, 5).text()

        self.modify = QtUiTools.QUiLoader().load("modify.ui")

        self.modify.pushButton_sure.clicked.connect(self.Sure)

        self.modify.lineEdit_id.setText(id)
        self.modify.lineEdit_name.setText(Rname)
        self.modify.lineEdit_pass.setText(pwd)
        self.modify.lineEdit_phone.setText(phone)
        self.modify.lineEdit_user.setText(user)
        self.modify.comboBox.setCurrentText(role)
        
        self.modify.show()
    #提交更新数据
    def Sure(self) :
        id = self.modify.lineEdit_id.text()
        name = self.modify.lineEdit_name.text()
        psd = self.modify.lineEdit_pass.text()
        phone = self.modify.lineEdit_phone.text()
        user = self.modify.lineEdit_user.text()
        role = self.modify.comboBox.currentText()

        sql = f"update user set name = '{user}', passWord = '{psd}', realName = '{name}',phone = '{phone}', role = '{role}' where stu_id = '{id}'"
        self.cursor.execute(sql)
        self.sql.commit()

        if self.cursor.rowcount == 1 :
            QtWidgets.QMessageBox.information(self, "提示", "修改成功!")
        else :
            QtWidgets.QMessageBox.critical(self, "错误", "修改失败!")
    #修改密码
    def ModifyPwd(self) :
        self.modifyPwd = QtUiTools.QUiLoader().load("modifyPassword.ui")
        
        self.modifyPwd.pushButton_sure.clicked.connect(self.SurePwd)

        self.modifyPwd.show()
    #提交修改
    def SurePwd(self) :
        id = self.modifyPwd.lineEdit_id.text()
        # print(id)
        pwd1 = self.modifyPwd.lineEdit_pwd1.text()
        pwd2 = self.modifyPwd.lineEdit_pwd2.text()
        # print(pwd1, pwd2)
        sql1 = f"select name, passWord from user where stu_id = '{id}'"
        self.cursor.execute(sql1)
        self.sql.commit()
        record = self.cursor.fetchone()
        if pwd1 == '' or pwd2 == '' or id == '' :
            QtWidgets.QMessageBox.critical(self, "错误", "输入不全，请重新输入！")
            return
        if record is None :
            QtWidgets.QMessageBox.critical(self, "错误", "学号错误，请重新输入！")
            return
        if record[1] == pwd1:
            sql = f"update user set passWord = '{pwd2}' where stu_id = '{id}'"
            self.cursor.execute(sql)
            self.sql.commit()
            QtWidgets.QMessageBox.information(self, "提示", "修改成功！")
        else :
            QtWidgets.QMessageBox.critical(self, "错误", "原密码错误！")
    #增加书籍
    def OnBook(self) :
        self.addBook = QtUiTools.QUiLoader().load("addBook.ui")
        
        self.addBook.pushButton_sure.clicked.connect(self.SureAdd)

        self.addBook.show()
    #确认增加
    def SureAdd(self) :
        isbn = self.addBook.lineEdit_isbn.text()
        title = self.addBook.lineEdit_title.text()
        author = self.addBook.lineEdit_author.text()
        publisher = self.addBook.lineEdit_publisher.text()
        publishdate = self.addBook.lineEdit_publishdate.text()
        number = self.addBook.lineEdit_number.text()
        
        sql = f"insert into t_book values('', '{isbn}', '{title}', '{author}', '{publisher}', '{publishdate}', {number})"
        
        try :
            self.cursor.execute(sql)
            self.sql.commit()
            QtWidgets.QMessageBox.information(self, "提示", "添加成功！")
        except sqlite3.Error as e :
            print("insert error:", e)
            QtWidgets.QMessageBox.critical(self, "错误", "添加失败！")
            return
    # 查询书籍
    def QueryBook(self) :
        judge = self.main_ui.lineEdit_book.text()
        
        sql = f"select isbn, title, author, publisher, publishdate, number from t_book where title like '%{judge}%'"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        #建立模型
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['书号', '书名', '作者', '出版社', '出版时间', '数量'])
        for i in range(len(res)) :
            for j in range(6) :
                item = QtGui.QStandardItem(str(res[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        self.main_ui.tableView_book.setModel(model)
    #删除书籍
    def DelBook(self) :
        row = self.main_ui.tableView_book.currentIndex().row()
        model = self.main_ui.tableView_book.model()
        isbn = model.item(row, 0).text()
        # print(isbn)
        sql = f"delete from t_book where isbn = '{isbn}'"
        # print("ok")
        self.cursor.execute(sql)
        self.sql.commit()
        if self.cursor.rowcount == 1 :
            QtWidgets.QMessageBox.information(self, "提示", "删除成功!")
        else :
            QtWidgets.QMessageBox.critical(self, "错误", "删除失败!")
    #修改书籍
    def ModifyBook(self) :
        # print("sb")
        row = self.main_ui.tableView_book.currentIndex().row()
        if row == -1 :
            return
        model = self.main_ui.tableView_book.model()

        isbn = model.item(row, 0).text()
        title = model.item(row, 1).text()
        author = model.item(row, 2).text()
        publisher = model.item(row, 3).text()
        publishdate = model.item(row, 4).text()
        number = model.item(row, 5).text()
        # print(author)
        self.modifyBook = QtUiTools.QUiLoader().load("modifyBook.ui")
        
        self.modifyBook.lineEdit_isbn.setText(isbn)
        self.modifyBook.lineEdit_title.setText(title)
        self.modifyBook.lineEdit_author.setText(author)
        self.modifyBook.lineEdit_publisher.setText(publisher)
        self.modifyBook.lineEdit_publishdate.setText(publishdate)
        self.modifyBook.lineEdit_number.setText(number)

        self.modifyBook.pushButton_sure.clicked.connect(self.SureModifyBook)

        self.modifyBook.show()
    #确定修改书籍
    def SureModifyBook(self) :
        isbn = self.modifyBook.lineEdit_isbn.text()
        title = self.modifyBook.lineEdit_title.text()
        author = self.modifyBook.lineEdit_author.text()
        publisher = self.modifyBook.lineEdit_publisher.text()
        publishdate = self.modifyBook.lineEdit_publishdate.text()
        number = self.modifyBook.lineEdit_number.text()
        # print(isbn)
        if title == '' or author == '' or publisher == '' or publishdate == '' or number == '' :
            QtWidgets.QMessageBox.critical(self, "提示", "填写不完整 修改失败!")
            return
        sql = f"update t_book set title = '{title}', author = '{author}', publisher = '{publisher}', publishdate = '{publishdate}', number = '{number}' where isbn = '{isbn}'"
        # sql = f"insert into t_book(isbn, title, author, publisher, publishdate, number) values('{isbn}', '{title}', '{author}', '{publisher}','{publishdate}', '{number}')"
        self.cursor.execute(sql)
        self.sql.commit()
        if self.cursor.rowcount != 0 :
            QtWidgets.QMessageBox.information(self, "提示", "修改成功!")
        else :
            QtWidgets.QMessageBox.critical(self, "提示", "修改失败!")
    #查询所有书籍
    def QuertAll(self) :
        judge = self.main_ui.lineEdit_book_borrow.text()
        
        sql = f"select isbn, title, author, publisher, publishdate, number from t_book where title like '%{judge}%'"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        #建立模型
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['书号', '书名', '作者', '出版社', '出版时间', '数量'])
        for i in range(len(res)) :
            for j in range(6) :
                item = QtGui.QStandardItem(str(res[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        self.main_ui.tableView_borrow.setModel(model)
    #批量导入
    def AddAllBook(self) :
        FileDirectory = QtWidgets.QFileDialog.getOpenFileName(self.main_ui.pushButton_add_all, "选择文件")                #选择目录，返回选中的路径
        print(FileDirectory[0])
        data = pd.read_excel(FileDirectory[0])

        # print(data)append
        data.to_sql('t_book', self.sql, if_exists='replace')
        QtWidgets.QMessageBox.information(self, "提示", "导入成功!")
    #查询借阅
    def QueryBorrow(self) :
        judge = self.main_ui.lineEdit_book_borrow.text()
        sql = f"SELECT stu_id, name, isbn, title, borrow_date, return_date, time FROM t_borrow JOIN user ON user_id = stu_id JOIN t_book ON book_isbn = isbn WHERE name LIKE '%{judge}%';"      
        
        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        # print(res[0][6])

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['学号', '姓名', '书号', '书名', '借书日期', '还书日期', '借阅时间'])

        for i in range(len(res)) :
            for j in range(7) :
                print(res[i][j])
                item = QtGui.QStandardItem(str(res[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(i, j, item)
        # print(self.x, self.y)
        self.main_ui.tableView_borrow.setModel(model)
    #借阅书籍
    def BrrowBook(self) :
        # print(1)
        row = self.main_ui.tableView_borrow.currentIndex().row()
        if row == -1 :
            return
        model = self.main_ui.tableView_borrow.model()
        isbn = model.item(row, 0).text()
        number = model.item(row, 5).text()
        borrow_data = QtCore.QDate.currentDate().toString("yyyy/MM/dd")

        if number == '0' :
            QtWidgets.QMessageBox.critical(self, "错误", "借书失败!")
            return
        
        sql = f"insert into t_borrow(user_id, book_isbn, borrow_date, return_date) values('{self.login_user_id}', '{isbn}', '{borrow_data}', '')"
        try :
            self.cursor.execute(sql)
            self.sql.commit()
            if self.cursor.rowcount == 1 :
                QtWidgets.QMessageBox.information(self, "提示", "借书成功!")
                sql = f"update t_book set number = number - 1 where isbn = '{isbn}' and number > 0"
                self.cursor.execute(sql)
                self.sql.commit()
        except sqlite3.Error as e :
            QtWidgets.QMessageBox.critical(self, "错误", "借书失败!")
            return 
    #归还书籍
    def ReturnBook(self) :
        row = self.main_ui.tableView_borrow.currentIndex().row()
        if row == -1 :
            return
        model = self.main_ui.tableView_borrow.model()
        isbn = model.item(row, 2).text()
        time = model.item(row, 6).text()

        # print(time)

        retrun_data = QtCore.QDate.currentDate().toString("yyyy/MM/dd")

        sql = f"update t_borrow set return_date = '{retrun_data}' where book_isbn = '{isbn}' and return_date == '' and time = '{time}';"
        
        try :
            self.cursor.execute(sql)
            if self.cursor.rowcount == 1 :
                QtWidgets.QMessageBox.information(self, "提示", "还书成功!")
                sql = f"update t_book set number = number + 1 where isbn = '{isbn}';"
                self.cursor.execute(sql)
            else :
                QtWidgets.QMessageBox.critical(self, "错误", "还书失败!")
            self.sql.commit()
        except sqlite3.Error as e :
            QtWidgets.QMessageBox.critical(self, "错误", "还书失败!")  
        # print(6)
    # 生成由数字和小写字母随机字符串
    def generate_lower_code(self, length):
        characters = string.digits + string.ascii_lowercase
        verification_code = ''.join(ra.choice(characters) for _ in range(length))
        return verification_code
    def yz(self) :
        self.s = self.generate_lower_code(6)
        self.ui_login.pushButton_yz.setText(self.s)
        # print(s)


if __name__ == "__main__" :
    #基本框架
    app = QtWidgets.QApplication([])
    #实例化空白界面对象
    w = MyWidget()
    #显示界面对象
    w.ui_login.show()

    app.exec_() # =死循环
    #基本框架D:\Python\Lib\site-packages\PySide2\designer.exe
