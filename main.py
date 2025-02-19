from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication,QMessageBox
import pymysql.cursors

connection = pymysql.connect(host='localhost',user='root',password='123456',db='TourBooking',charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
list=['flight_resvKey','bus_resvKey','hotel_resvKey']
class SI:
    m_login = None
    manager_win = None
    user_win = None
    user_name=None
    user_ID=None
    resvNum=1

class login:
    def __init__(self):
        self.ui = QUiLoader().load('login.ui')
        self.ui.btn_login_in.clicked.connect(self.confirm_user)
        self.ui.edt_password.returnPressed.connect(self.confirm_user)
        self.search_user=0
        self.search_user_password=None

    def confirm_user(self):
        with connection.cursor() as cursor:
            self.search_user=0
            user=self.ui.edt_user_name.text().strip()
            SI.user_name=user
            password=self.ui.edt_password.text().strip()
            if user == 'admin' and password == '123456':
                SI.manager_win = win_manager() # 系统管理员界面
                self.ui.edt_password.setText('')
                self.ui.hide()
                SI.manager_win.ui.show()
            elif user != 'admin':
                sql = 'select * from CUSTOMERS;'
                cursor.execute(sql, ())
                for data in cursor.fetchall():
                    if data['custName']==user:
                        self.search_user=1
                        self.search_user_password=data['password']
                        break
                if self.search_user==1 and (self.search_user_password==password):
                    sql='select custID from CUSTOMERS where custName='
                    sql+='\''+SI.user_name+'\';'
                    cursor.execute(sql, ())
                    SI.user_ID=cursor.fetchall()[0]['custID'] # 找用户的id，为之后的函数运行做准备
                    sql='select max(resvNum) from RESERVATIONS;'
                    cursor.execute(sql, ())
                    # print(cursor.fetchall())
                    tt=cursor.fetchall()
                    if(tt==[] or tt[0]['max(resvNum)']==None):
                        SI.resvNum=1
                    else:
                        SI.resvNum=max(1,int(tt[0]['max(resvNum)'])+1) # 找到订单的序号
                    SI.user_win = win_user() # 用户界面
                    self.ui.edt_password.setText('')
                    self.ui.hide()
                    SI.user_win.ui.show()
                elif self.search_user==1 and self.search_user_password!=password:
                    QMessageBox.warning(self.ui, '登陆失败', '密码错误!')
                else:
                    QMessageBox.warning(self.ui, '登陆失败', '用户名不存在')
            else:
                QMessageBox.warning(self.ui,'登陆失败','用户账号或密码错误')
class win_user:
    def __init__(self):
        self.ui = QUiLoader().load('user.ui')
        self.ui.actionExit.triggered.connect(self.signout)
        self.ui.actionFlight.triggered.connect(self.query_flight)
        self.ui.actionBus.triggered.connect(self.query_bus)
        self.ui.actionHotel.triggered.connect(self.query_hotel)
        self.ui.actionUsers.triggered.connect(self.query_myself)
        self.ui.actionRESERVATIONS.triggered.connect(self.query_MyRESERVATIONS)
        self.ui.btn_special.clicked.connect(self.Special_query)
        self.ui.btn_reserve_confirm.clicked.connect(self.Reserve_cancel)
        self.ui.btn_query_user.clicked.connect(self.query_other)

    def query_other(self):
        with connection.cursor() as cursor:
            user=self.ui.edt_other_user.text()
            password=self.ui.edt_other_userpassword.text()
            sql = 'select * from CUSTOMERS;'
            search_user=0
            cursor.execute(sql, ())
            for data in cursor.fetchall():
                if data['custName'] == user:
                    search_user = 1
                    search_user_password = data['password']
                    break
            if search_user == 1 and (search_user_password == password):
                sql='select custID from CUSTOMERS where custName='
                sql+='\'' + user + '\';'
                cursor.execute(sql, ())
                user_ID=cursor.fetchall()[0]['custID']
                sql = 'select * from RESERVATIONS where custID='
                sql += '\'' + user_ID + '\';'
                try:
                    cursor.execute(sql, ())
                    tt=cursor.fetchall()
                    print(tt)
                    # self.ui.edt_other_user.clear()
                    # self.ui.edt_other_userpassword.clear()
                    self.ui.edt_query.clear()
                    self.ui.edt_query.appendPlainText('resvNum:     custID:     resvType:       resvKey:  location')
                    print('resvNum:     custID:     resvType:       resvKey:        location_information:')
                    for data in tt:
                        if data['resvType'] == 1:
                            ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                                 '            ' + data['flight_resvKey'] + '     '+data['location']+'\n'
                        elif data['resvType'] == 2:
                            ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                                 '            ' + data['bus_resvKey'] + '     '+data['location']+'\n'
                        elif data['resvType'] == 3:
                            ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                                 '            ' + data['hotel_resvKey'] + '     '+data['location']+'\n'
                        print(ss)
                        self.ui.edt_query.appendPlainText(ss)
                    QMessageBox.information(self.ui, 'OK!', '查询成功!')

                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的信息！')

            elif search_user == 1 and search_user_password != password:
                QMessageBox.warning(self.ui, '登陆失败', '用户名或密码错误!')

    def Special_query(self):
        with connection.cursor() as cursor:
            type = int(self.ui.edt_special_type.text())
            location1 = self.ui.edt_special_location1.text()
            location2 = self.ui.edt_special_location2.text()
            self.ui.edt_query.clear()
            if type == 1:
                sql = 'select * from flights where FromCity='
                sql += '\'' + location1 + '\' and ArivCity=' + '\'' + location2 + '\';'
                self.ui.edt_query.appendPlainText('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
                print('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
                try:
                    cursor.execute(sql, ())
                    print("查询成功：", type, location1, location2)
                    for data in cursor.fetchall():
                        if data['price'] >= 1000:
                            ss = data['flightNum'] + '         ' + str(data['price']) + '        ' + str(
                                data['numSeats']) + '       ' \
                                 + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data[
                                     'ArivCity'] + '\n'
                        else:
                            ss = data['flightNum'] + '         ' + str(data['price']) + '         ' + str(
                                data['numSeats']) + '       ' \
                                 + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data[
                                     'ArivCity'] + '\n'
                        self.ui.edt_query.appendPlainText(ss)
                        print(ss)
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("查询失败：", type, location1, location2)
                    QMessageBox.critical(self.ui, '查询失败', '请输入正确的信息！')
            elif type == 2:
                sql = 'select * from bus where location='
                sql += '\'' + location1 + '\';'
                self.ui.edt_query.appendPlainText('busNum:   location:   price:   numSeats:   numAvail:')
                print('busNum:   location:  price:   numSeats:   numAvail:')
                try:
                    cursor.execute(sql, ())
                    print("查询成功：", type, location1)
                    for data in cursor.fetchall():
                        sa = 10 - len(data['location'])
                        if len(data['location']) >= 6:
                            sa = sa - 1
                        ss = data['busNum'] + '      ' + data['location'] + sa * ' ' + str(data['price']) \
                             + '        ' + str(data['numSeats']) + '         ' + str(data['numAvail']) + '\n'
                        self.ui.edt_query.appendPlainText(ss)
                        print(ss)
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("查询失败：", type, location1)
                    QMessageBox.critical(self.ui, '查询失败', '请输入正确的信息！')
            elif type == 3:
                sql = 'select * from HOTELS where location='
                sql += '\'' + location1 + '\';'
                self.ui.edt_query.appendPlainText('hotelNum:   location:   price:   numRooms:   numAvail:')
                print('busNum:   location:  price:   numSeats:   numAvail:')
                try:
                    cursor.execute(sql, ())
                    print("查询成功：", type, location1)
                    for data in cursor.fetchall():
                        sa = 10 - len(data['location'])
                        if len(data['location']) >= 6:
                            sa = sa - 1
                        ss = data['hotelNum'] + '      ' + data['location'] + sa * ' ' + '  ' + str(data['price']) \
                             + '        ' + str(data['numRooms']) + '         ' + str(data['numAvail']) + '\n'
                        self.ui.edt_query.appendPlainText(ss)
                        print(ss)
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("查询失败：", type, location1)
                    QMessageBox.critical(self.ui, '查询失败', '请输入正确的信息！')
            else:
                QMessageBox.critical(self.ui, '查询失败', '请输入正确的type！')

    def signout(self):
        SI.user_win.ui.close()
        SI.m_login.ui.show()
    def query_flight(self):
        with connection.cursor() as cursor:
            sql = "select * from flights;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
            print('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
            for data in cursor.fetchall():
                if data['price']>=1000:
                    ss = data['flightNum'] + '         ' + str(data['price']) + '        ' + str(
                        data['numSeats']) + '       ' \
                         + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data['ArivCity'] + '\n'
                else:
                    ss = data['flightNum'] + '         ' + str(data['price']) + '         ' + str(
                        data['numSeats']) + '       ' \
                         + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data['ArivCity'] + '\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_bus(self):
        with connection.cursor() as cursor:
            sql = "select * from BUS;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('busNum:   location:   price:   numSeats:   numAvail:')
            print('busNum:   location:  price:   numSeats:   numAvail:')
            for data in cursor.fetchall():
                sa=10-len(data['location'])
                if len(data['location'])>=6:
                    sa=sa-1
                ss = data['busNum'] + '      ' + data['location'] + sa*' ' + str(data['price']) \
                     + '        '+ str(data['numSeats']) + '         ' + str(data['numAvail']) + '\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_hotel(self):
        with connection.cursor() as cursor:
            sql = "select * from HOTELS;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('hotelNum:   location:   price:   numRooms:   numAvail:')
            print('busNum:   location:  price:   numSeats:   numAvail:')
            for data in cursor.fetchall():
                sa = 10 - len(data['location'])
                if len(data['location']) >= 6:
                    sa = sa - 1
                ss = data['hotelNum'] + '      ' + data['location'] + sa * ' '+'  ' + str(data['price']) \
                     + '        ' + str(data['numRooms']) + '         ' + str(data['numAvail']) + '\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_myself(self):
        with connection.cursor() as cursor:
            sql = "select * from CUSTOMERS where custName="
            sql+='\''+SI.user_name+'\';'
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('custID:      custName:   password:')
            print('custID:      custName:   password:')
            for data in cursor.fetchall():
                ss = data['custID'] + '           ' + data['custName'] + '  ' + data['password']+'\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_MyRESERVATIONS(self):
        with connection.cursor() as cursor:
            sql = "select * from RESERVATIONS where custID="
            sql+='\''+SI.user_ID+'\';'
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('resvNum:     custID:     resvType:       resvKey:  location:')
            print('resvNum:     custID:     resvType:       resvKey:        location:')
            for data in cursor.fetchall():
                if data['resvType']==1:
                    ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                         '            ' + data['flight_resvKey'] +'     '+data['location']+'\n'
                elif data['resvType']==2:
                    ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                         '            ' + data['bus_resvKey'] + '     '+data['location']+'\n'
                elif data['resvType']==3:
                    ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                         '            ' + data['hotel_resvKey'] + '     '+data['location']+'\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def Reserve_cancel(self):
        with connection.cursor() as cursor:
            if self.ui.btn_reserve.isChecked(): # 预订功能
                type = int(self.ui.edt_type.text())
                data = self.ui.edt_data.toPlainText()
                flag=0
                if type==1:
                    sql='select flight_resvKey from RESERVATIONS where custID='
                    sql+='\''+SI.user_ID+'\';'
                    cursor.execute(sql, ())
                    for content in cursor.fetchall():
                        if content['flight_resvKey']==data:
                            flag=1
                            break
                    if flag==1:
                        QMessageBox.information(self.ui, '提示', '您已预定该航班，请不要重复预定!')
                    else:
                        sql='select FromCity,ArivCity from FLIGHTS where flightNum='
                        sql+=data+';'
                        cursor.execute(sql, ())
                        tt=cursor.fetchall()
                        from_location=tt[0]['FromCity']
                        to_location=tt[0]['ArivCity']
                        sql='insert into RESERVATIONS(resvNum,custID,resvType,flight_resvKey,location) values'
                        sql+='(\''+str(SI.resvNum)+'\',\''+SI.user_ID+'\',1,\''+data+'\',\''+from_location+'->'+to_location+'\');'
                        SI.resvNum=SI.resvNum+1
                        try:
                            cursor.execute(sql, ())
                            self.ui.edt_type.clear()
                            self.ui.edt_data.clear()
                            print("预定航班成功：", data)
                            QMessageBox.information(self.ui, 'OK!', '预定航班成功!')
                            connection.commit()
                        except:
                            # 如果发生错误则回滚
                            # cursor.rollback()
                            print("预定航班失败：", data)
                            QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的格式！')
                elif type==2:
                    sql = 'select bus_resvKey from RESERVATIONS where custID='
                    sql += '\'' + SI.user_ID + '\';'
                    cursor.execute(sql, ())
                    for content in cursor.fetchall():
                        if content['bus_resvKey'] == data:
                            flag = 1
                            break
                    if flag == 1:
                        QMessageBox.information(self.ui, '提示', '您已预定该大巴，请不要重复预定!')
                    else:
                        sql = 'select location from BUS where busNum='
                        sql += data + ';'
                        cursor.execute(sql, ())
                        from_location = cursor.fetchall()[0]['location']
                        sql = 'insert into RESERVATIONS(resvNum,custID,resvType,bus_resvKey,location) values'
                        sql += '(\'' + str(SI.resvNum) + '\',\'' + SI.user_ID + '\',2,\'' + data + '\',\''+from_location+'\');'
                        print(sql)
                        SI.resvNum = SI.resvNum + 1
                        try:
                            cursor.execute(sql, ())
                            self.ui.edt_type.clear()
                            self.ui.edt_data.clear()
                            print("预定大巴成功：", data)
                            QMessageBox.information(self.ui, 'OK!', '预定大巴成功!')
                            connection.commit()
                        except:
                            # 如果发生错误则回滚
                            # cursor.rollback()
                            print("预定大巴失败：", data)
                            QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的格式！')
                elif type==3:
                    sql = 'select hotel_resvKey from RESERVATIONS where custID='
                    sql += '\'' + SI.user_ID + '\';'
                    cursor.execute(sql, ())
                    for content in cursor.fetchall():
                        if content['hotel_resvKey'] == data:
                            flag = 1
                            break
                    if flag == 1:
                        QMessageBox.information(self.ui, '提示', '您已预定该宾馆，请不要重复预定!')
                    else:
                        sql = 'select location from HOTELS where hotelNum='
                        sql +=  data + ';'
                        cursor.execute(sql, ())
                        from_location = cursor.fetchall()[0]['location']
                        sql = 'insert into RESERVATIONS(resvNum,custID,resvType,hotel_resvKey,location) values'
                        sql += '(\'' + str(SI.resvNum) + '\',\'' + SI.user_ID + '\',3,\'' + data + '\',\''+from_location+'\');'
                        SI.resvNum = SI.resvNum + 1
                        try:
                            cursor.execute(sql, ())
                            self.ui.edt_type.clear()
                            self.ui.edt_data.clear()
                            print("预定宾馆成功：", data)
                            QMessageBox.information(self.ui, 'OK!', '预定宾馆成功!')
                            connection.commit()
                        except:
                            # 如果发生错误则回滚
                            # cursor.rollback()
                            print("预定宾馆失败：", data)
                            QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的格式！')
                else:
                    QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的type！')

            elif self.ui.btn_cancel.isChecked(): # 取消预定
                type = int(self.ui.edt_type.text())
                data = self.ui.edt_data.toPlainText()
                flag = 0
                if type==1:
                    sql ='select flight_resvKey from RESERVATIONS where custID='
                    sql += '\'' + SI.user_ID + '\';'
                    cursor.execute(sql, ())
                    for content in cursor.fetchall():
                        if content['flight_resvKey']==data:
                            flag=1
                            break
                    if flag==1: # 开始取消
                        sql = 'delete from RESERVATIONS where custID='
                        sql += '\''+SI.user_ID+'\' and flight_resvKey=\''+data+'\';'
                        try:
                            cursor.execute(sql, ())
                            self.ui.edt_type.clear()
                            self.ui.edt_data.clear()
                            print("取消预定航班成功：", data)
                            QMessageBox.information(self.ui, 'OK!', '取消预定航班成功!')
                            connection.commit()
                        except:
                            # 如果发生错误则回滚
                            # cursor.rollback()
                            print("取消预定航班失败：", data)
                            QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的格式！')
                    else:
                        QMessageBox.information(self.ui, '提示', '您未预定该航班，请您确认信息!')
                elif type==2:
                    sql = 'select bus_resvKey from RESERVATIONS where custID='
                    sql += '\'' + SI.user_ID + '\';'
                    cursor.execute(sql, ())
                    for content in cursor.fetchall():
                        if content['bus_resvKey'] == data:
                            flag = 1
                            break
                    if flag == 1:  # 开始取消
                        sql = 'delete from RESERVATIONS where custID='
                        sql += '\'' + SI.user_ID + '\' and bus_resvKey=\'' + data + '\';'
                        try:
                            cursor.execute(sql, ())
                            self.ui.edt_type.clear()
                            self.ui.edt_data.clear()
                            print("取消预定大巴成功：", data)
                            QMessageBox.information(self.ui, 'OK!', '取消预定大巴成功!')
                            connection.commit()
                        except:
                            # 如果发生错误则回滚
                            # cursor.rollback()
                            print("取消预定大巴失败：", data)
                            QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的格式！')
                    else:
                        QMessageBox.information(self.ui, '提示', '您未预定该大巴，请您确认信息!')
                elif type==3:
                    sql = 'select hotel_resvKey from RESERVATIONS where custID='
                    sql += '\'' + SI.user_ID + '\';'
                    cursor.execute(sql, ())
                    for content in cursor.fetchall():
                        if content['hotel_resvKey'] == data:
                            flag = 1
                            break
                    if flag == 1:  # 开始取消
                        sql = 'delete from RESERVATIONS where custID='
                        sql += '\'' + SI.user_ID + '\' and hotel_resvKey=\'' + data + '\';'
                        try:
                            cursor.execute(sql, ())
                            self.ui.edt_type.clear()
                            self.ui.edt_data.clear()
                            print("取消预定宾馆成功：", data)
                            QMessageBox.information(self.ui, 'OK!', '取消预定宾馆成功!')
                            connection.commit()
                        except:
                            # 如果发生错误则回滚
                            # cursor.rollback()
                            print("取消预定宾馆失败：", data)
                            QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的格式！')
                    else:
                        QMessageBox.information(self.ui, '提示', '您未预定该宾馆，请您确认信息!')
                else:
                    QMessageBox.critical(self.ui, 'ERROR!', '请输入正确的type！')
            else:
                QMessageBox.critical(self.ui, '错误', '请至少勾选一项！')

class win_manager:
    def __init__(self):
        self.ui = QUiLoader().load('manager.ui')
        self.ui.actionExit.triggered.connect(self.signout)
        self.ui.actionFlight.triggered.connect(self.query_flight)
        self.ui.actionBus.triggered.connect(self.query_bus)
        self.ui.actionHotel.triggered.connect(self.query_hotel)
        self.ui.actionUsers.triggered.connect(self.query_users)
        self.ui.actionRESERVATIONS.triggered.connect(self.query_RESERVATIONS)
        self.ui.btn_modify.clicked.connect(self.Modify)
        self.ui.btn_create_user.clicked.connect(self.Create_user)
        self.users_count=1
        self.ui.btn_special.clicked.connect(self.Special_query)

    def Special_query(self):
        with connection.cursor() as cursor:
            type=int(self.ui.edt_special_type.text())
            location1=self.ui.edt_special_location1.text()
            location2=self.ui.edt_special_location2.text()
            self.ui.edt_query.clear()
            if type==1:
                sql='select * from flights where FromCity='
                sql+='\''+location1+'\' and ArivCity='+'\''+location2+'\';'
                self.ui.edt_query.appendPlainText('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
                print('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
                try:
                    cursor.execute(sql, ())
                    print("查询成功：", type, location1, location2)
                    for data in cursor.fetchall():
                        if data['price'] >= 1000:
                            ss = data['flightNum'] + '         ' + str(data['price']) + '        ' + str(
                                data['numSeats']) + '       ' \
                                 + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data[
                                     'ArivCity'] + '\n'
                        else:
                            ss = data['flightNum'] + '         ' + str(data['price']) + '         ' + str(
                                data['numSeats']) + '       ' \
                                 + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data[
                                     'ArivCity'] + '\n'
                        self.ui.edt_query.appendPlainText(ss)
                        print(ss)
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("查询失败：", type, location1, location2)
                    QMessageBox.critical(self.ui, '查询失败', '请输入正确的信息！')
            elif type==2:
                sql='select * from bus where location='
                sql+='\''+location1+'\';'
                self.ui.edt_query.appendPlainText('busNum:   location:   price:   numSeats:   numAvail:')
                print('busNum:   location:  price:   numSeats:   numAvail:')
                try:
                    cursor.execute(sql, ())
                    print("查询成功：", type, location1)
                    for data in cursor.fetchall():
                        sa = 10 - len(data['location'])
                        if len(data['location']) >= 6:
                            sa = sa - 1
                        ss = data['busNum'] + '      ' + data['location'] + sa * ' ' + str(data['price']) \
                             + '        ' + str(data['numSeats']) + '         ' + str(data['numAvail']) + '\n'
                        self.ui.edt_query.appendPlainText(ss)
                        print(ss)
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("查询失败：", type, location1)
                    QMessageBox.critical(self.ui, '查询失败', '请输入正确的信息！')
            elif type==3:
                sql='select * from HOTELS where location='
                sql+='\''+location1+'\';'
                self.ui.edt_query.appendPlainText('hotelNum:   location:   price:   numRooms:   numAvail:')
                print('busNum:   location:  price:   numSeats:   numAvail:')
                try:
                    cursor.execute(sql, ())
                    print("查询成功：", type, location1)
                    for data in cursor.fetchall():
                        sa = 10 - len(data['location'])
                        if len(data['location']) >= 6:
                            sa = sa - 1
                        ss = data['hotelNum'] + '      ' + data['location'] + sa * ' ' + '  ' + str(data['price']) \
                             + '        ' + str(data['numRooms']) + '         ' + str(data['numAvail']) + '\n'
                        self.ui.edt_query.appendPlainText(ss)
                        print(ss)
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("查询失败：", type, location1)
                    QMessageBox.critical(self.ui, '查询失败', '请输入正确的信息！')
            else:
                QMessageBox.critical(self.ui, '查询失败', '请输入正确的type！')
    def Create_user(self):
        with connection.cursor() as cursor:
            user_name = self.ui.edt_create_user.text().strip()
            user_password = self.ui.edt_create_userpassword.text().strip()
            if self.ui.btn_create_user_flag.isChecked():
                sql = "select max(custID) from customers;"
                cursor.execute(sql, ())
                try:
                    self.users_count = int(cursor.fetchall()[0]['max(custID)'])
                    self.users_count = self.users_count + 1
                    sql = 'insert into CUSTOMERS(custID,custName,password) values'
                    sql += '(\'' + str(self.users_count) + '\',\'' + user_name + '\',\'' + user_password + '\');'
                    cursor.execute(sql, ())
                    print("创建用户成功：", self.users_count, user_name, user_password)
                    QMessageBox.information(self.ui, '用户创建成功!', 'OK!')
                    self.ui.edt_create_user.clear()
                    self.ui.edt_create_userpassword.clear()
                except:
                    # 如果发生错误则回滚
                    # cursor.rollback()
                    print("创建用户失败：", self.users_count, user_name, user_password)
                    QMessageBox.critical(self.ui, '插入操作失败', '请输入正确的格式！')
            elif self.ui.btn_delete_user_flag.isChecked():
                sql='select password from customers where custName='
                sql+='\''+user_name+'\';'
                cursor.execute(sql, ())
                if user_password==str(cursor.fetchall()[0]['password']):
                    try:
                        sql='delete from customers where custName='
                        sql += '\'' + user_name + '\';'
                        cursor.execute(sql, ())
                        print('用户删除成功！',user_name,user_password)
                        QMessageBox.information(self.ui, 'OK!', '用户删除成功!')
                        self.ui.edt_create_user.clear()
                        self.ui.edt_create_userpassword.clear()
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print('用户删除失败！',user_name,user_password)
                        QMessageBox.critical(self.ui,'ERROR！','用户删除失败！')
                else:
                    QMessageBox.warning(self.ui, 'Warning!', '用户名或密码输入出错!')
            else:
                QMessageBox.warning(self.ui, 'Warning!', '请至少勾选一项！')
    def Modify(self):
        with connection.cursor() as cursor:
            if self.ui.btn_insert.isChecked():
                type = int(self.ui.edt_type.text())
                data = self.ui.edt_data.toPlainText()
                # if 'drop' in data or 'delete' in data or 'truncate' in data or 'update' in data:
                #     QMessageBox.critical(self.ui, 'ERROR!', '请不要输入无关指令！')
                if type==1:
                    try:
                        sql="insert into FLIGHTS(flightNum,price,numSeats,numAvail,FromCity,ArivCity) values"
                        sql+=data
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("插入数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '插入操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("插入数据失败：", data)
                        QMessageBox.critical(self.ui,'插入操作失败','请输入正确的格式！')
                elif type==2:
                    try:
                        sql = "insert into BUS(busNum,location,price,numSeats,numAvail) values"
                        sql += data
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("插入数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '插入操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("插入数据失败：", data)
                        QMessageBox.critical(self.ui, '插入操作失败', '请输入正确的格式！')
                elif type==3:
                    try:
                        sql = "insert into HOTELS(hotelNum,location,price,numRooms,numAvail) values"
                        sql += data
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("插入数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '插入操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("插入数据失败：", data)
                        QMessageBox.critical(self.ui, '插入操作失败', '请输入正确的格式！')
                elif type==4:
                    sql = "insert into RESERVATIONS(resvNum,custID,resvType,"
                    sql += list[int(data[9]) - 1] + ',location) values' + data
                    print(sql)
                    try:
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("插入数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '插入操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("插入数据失败：", data)
                        QMessageBox.critical(self.ui, '插入操作失败', '请输入正确的格式！')
                else:
                    QMessageBox.information(self.ui, '插入操作失败', 'type值输入错误')
                connection.commit()

            elif self.ui.btn_delete.isChecked():
                type = int(self.ui.edt_type.text())
                data = self.ui.edt_data.toPlainText()
                if type==1:
                    try:
                        sql="delete from FLIGHTS where flightNum="
                        sql=sql+'\''+data+'\';'
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("删除数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '删除操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("插入数据失败：", data)
                        QMessageBox.critical(self.ui,'删除操作失败','请输入正确的格式！')
                elif type==2:
                    try:
                        sql = "delete from BUS where busNum="
                        sql = sql + '\'' + data + '\';'
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("删除数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '删除操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("插入数据失败：", data)
                        QMessageBox.critical(self.ui, '删除操作失败', '请输入正确的格式！')
                elif type==3:
                    try:
                        sql = "delete from HOTELS where hotelNum="
                        sql = sql + '\'' + data + '\';'
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("删除数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '删除操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("删除数据失败：", data)
                        QMessageBox.critical(self.ui, '删除操作失败', '请输入正确的格式！')
                elif type==4:
                    sql = "delete from RESERVATIONS where resvNum="
                    sql += data
                    try:
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("删除数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '删除操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("删除数据失败：", data)
                        QMessageBox.critical(self.ui, '删除操作失败', '请输入正确的格式！')
                else:
                    QMessageBox.information(self.ui, '删除操作失败', 'type值输入错误')
                connection.commit()
            elif self.ui.btn_modify_flag.isChecked():
                type = int(self.ui.edt_type.text())
                num,data = self.ui.edt_data.toPlainText().split()
                if type==1:
                    sql='update flights set '+data+' where flightNum='
                    sql+='\''+num+'\';'
                    try:
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("修改数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '修改操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("修改数据失败：", data)
                        QMessageBox.critical(self.ui, '修改操作失败', '请输入正确的格式！')
                elif type==2:
                    sql = 'update bus set ' + data + ' where busNum='
                    sql += '\'' + num + '\';'
                    try:
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("修改数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '修改操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("修改数据失败：", data)
                        QMessageBox.critical(self.ui, '修改操作失败', '请输入正确的格式！')
                elif type==3:
                    sql = 'update HOTELS set ' + data + ' where hotelNum='
                    sql += '\'' + num + '\';'
                    try:
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("修改数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '修改操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("修改数据失败：", data)
                        QMessageBox.critical(self.ui, '修改操作失败', '请输入正确的格式！')
                elif type==4:
                    sql = 'update RESERVATIONS set ' + data + ' where resvNum='
                    sql += '\'' + num + '\';'
                    try:
                        cursor.execute(sql, ())
                        self.ui.edt_type.clear()
                        self.ui.edt_data.clear()
                        print("修改数据成功：", data)
                        QMessageBox.information(self.ui, 'OK!', '修改操作成功!')
                    except:
                        # 如果发生错误则回滚
                        # cursor.rollback()
                        print("修改数据失败：", data)
                        QMessageBox.critical(self.ui, '修改操作失败', '请输入正确的格式！')
                else:
                    QMessageBox.critical(self.ui, '修改操作失败', 'type值输入错误')
                connection.commit()
            else:
                QMessageBox.critical(self.ui, '错误', '请至少勾选一项！')
    def signout(self):
        SI.manager_win.ui.close()
        SI.m_login.ui.show()
    def query_flight(self):
        with connection.cursor() as cursor:
            sql = "select * from flights;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
            print('flightNum:   price:  numSeats:   numAvail:   FromCity:   ArivCity:')
            for data in cursor.fetchall():
                if data['price']>=1000:
                    ss = data['flightNum'] + '         ' + str(data['price']) + '        ' + str(
                        data['numSeats']) + '       ' \
                         + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data['ArivCity'] + '\n'
                else:
                    ss = data['flightNum'] + '         ' + str(data['price']) + '         ' + str(
                        data['numSeats']) + '       ' \
                         + str(data['numAvail']) + '       ' + data['FromCity'] + '        ' + data['ArivCity'] + '\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_bus(self):
        with connection.cursor() as cursor:
            sql = "select * from BUS;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('busNum:   location:   price:   numSeats:   numAvail:')
            print('busNum:   location:  price:   numSeats:   numAvail:')
            for data in cursor.fetchall():
                sa=10-len(data['location'])
                if len(data['location'])>=6:
                    sa=sa-1
                ss = data['busNum'] + '      ' + data['location'] + sa*' ' + str(data['price']) \
                     + '        '+ str(data['numSeats']) + '         ' + str(data['numAvail']) + '\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_hotel(self):
        with connection.cursor() as cursor:
            sql = "select * from HOTELS;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('hotelNum:   location:   price:   numRooms:   numAvail:')
            print('busNum:   location:  price:   numSeats:   numAvail:')
            for data in cursor.fetchall():
                sa = 10 - len(data['location'])
                if len(data['location']) >= 6:
                    sa = sa - 1
                ss = data['hotelNum'] + '      ' + data['location'] + sa * ' '+'  ' + str(data['price']) \
                     + '        ' + str(data['numRooms']) + '         ' + str(data['numAvail']) + '\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_users(self):
        with connection.cursor() as cursor:
            sql = "select * from CUSTOMERS;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('custID:      custName:   password:')
            print('custID:      custName:   password:')
            for data in cursor.fetchall():
                ss = data['custID'] + '           ' + data['custName'] + '  ' + data['password']+'\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)
    def query_RESERVATIONS(self):
        with connection.cursor() as cursor:
            sql = "select * from RESERVATIONS;"
            cursor.execute(sql, ())
            self.ui.edt_query.clear()
            self.ui.edt_query.appendPlainText('resvNum:     custID:     resvType:       resvKey:  location:')
            print('resvNum:     custID:     resvType:       resvKey:')
            for data in cursor.fetchall():
                if data['resvType']==1:
                    ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                         '            ' + data['flight_resvKey'] + '     '+data['location']+'\n'
                elif data['resvType']==2:
                    ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                         '            ' + data['bus_resvKey'] + '     '+data['location']+'\n'
                elif data['resvType']==3:
                    ss = data['resvNum'] + '            ' + data['custID'] + '              ' + str(data['resvType']) + \
                         '            ' + data['hotel_resvKey'] + '     '+data['location']+'\n'
                self.ui.edt_query.appendPlainText(ss)
                print(ss)

app = QApplication([])
SI.m_login = login()
SI.m_login.ui.show()
app.exec_()