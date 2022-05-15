import sys
import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import psycopg2

conn = psycopg2.connect(database="Project", user="postgres", password="010504", host="127.0.0.1", port="5432")

global ID
ID = ' '


class CustomTabBar(QTabBar):
    def tabSizeHint(self, index):
        s = super(CustomTabBar, self).tabSizeHint(index)
        s.transpose()
        return s

    def paintEvent(self, _):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()
        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()
            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r
            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class Mainwindow(QTabWidget):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setWindowTitle("Tasks")

        self.setTabBar(CustomTabBar())
        self.setGeometry(QRect(400, 200, 750, 400))
        style = "QTabBar::tab{background-color:rgb(79,75,75,0);}" + \
                "QTabBar::tab:selected{background-color:rgb(200,200,200);}" + \
                "QLineEdit{border:1px solid " \
                "gray;width:300px;border-radius:10px;padding:2px 4px;"
        self.setStyleSheet(style)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.tab1_init()
        self.tab2_init()
        self.tab3_init()
        self.tab4_init()
        self.tab5_init()

        self.addTab(self.tab1, 'User Info')
        self.addTab(self.tab2, 'Stu management')
        self.addTab(self.tab3, 'Stu application')
        self.addTab(self.tab4, 'Teacher comment')
        self.addTab(self.tab5, 'Search')

        self.setTabPosition(self.West)


    def tab1_init(self):
        global ID
        id_label = QLabel('ID:', self.tab1)
        id_lab = QLabel(ID, self.tab1)
        self.tab1.id_lab = id_lab
        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        id_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        id_lab.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))

        g_layout = QGridLayout()
        g_layout.addWidget(id_label, 0, 0, 1, 1)
        g_layout.addWidget(id_lab, 0, 1, 1, 1)
        g_layout.addItem(spacerItem, 1, 0, 1, 1)

        self.tab1.setLayout(g_layout)

    def tab2_init(self):
        app_label = QLabel('Application ID:', self.tab2)
        app_line = QLineEdit(self.tab2)

        status_label = QLabel('Status:', self.tab2)
        items = ['Please choose the status of the application','cancelled']
        status_combo = QComboBox(self.tab2)
        status_combo.addItems(items)

        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        submit_button_2 = QPushButton('Submit', self.tab2)
        submit_button_2.clicked.connect(self.submit_info_2)

        g_layout = QGridLayout()
        g_layout.addWidget(app_label, 0, 0, 1, 1)
        g_layout.addWidget(app_line, 0, 1, 1, 1)
        g_layout.addWidget(status_label, 1, 0, 1, 1)
        g_layout.addWidget(status_combo, 1, 1, 1, 1)
        g_layout.addWidget(submit_button_2, 3, 0, 1, 1)
        g_layout.addItem(spacerItem, 2, 0, 1, 1)

        self.tab2.setLayout(g_layout)

        app_line.textChanged.connect(self.check_input_func_2)

        self.tab2.app_line = app_line
        self.tab2.status_combo = status_combo
        self.tab2.submit_button_2 = submit_button_2

    def check_input_func_2(self):
        if self.tab2.app_line.text() and self.tab2.status_combo.currentText():
            self.tab2.submit_button_2.setEnabled(True)
        else:
            self.tab2.submit_button_2.setEnabled(False)

    def submit_info_2(self):
        cur_app_id = self.tab2.app_line.text()
        cursor = conn.cursor()
        cursor.execute("SELECT app_creator_id FROM Application WHERE app_id LIKE %s",
                       (cur_app_id, ))
        result = cursor.fetchall()
        creator_id = result[0][0]
        print(creator_id)
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM Application WHERE app_id LIKE %s",
                       (self.tab2.app_line.text(),))
        results = cursor.fetchall()
        app_state = results[0][0]
        print(app_state)

        if ((creator_id == self.tab1.id_lab.text())
                and (app_state == 'passed' or app_state == 'refused')
                and (self.tab2.status_combo.currentText() == 'cancelled')):
            cursor.execute("UPDATE Application SET state = %s WHERE app_id LIKE %s",
                           (self.tab2.status_combo.currentText(),
                            self.tab2.app_line.text()))
            cursor.close()
            conn.commit()
            QMessageBox.information(self, 'Information', 'You have updated the state of your application!')
            print('submit')
            self.tab2.app_line.clear()
        else:
            QMessageBox.critical(self, 'Wrong', 'Only creator can manage this application in passed or refused state!')

    def tab3_init(self):

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(app_id) FROM Application")
        app_num = cursor.fetchall()
        app_ID = app_num[0][0]
        self.tab3.app_ID = app_ID+1

        out_label = QLabel('OUT time:', self.tab3)
        out_line = QLineEdit(self.tab3)
        in_label = QLabel('IN time:', self.tab3)
        in_line = QLineEdit(self.tab3)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        submit_button_3 = QPushButton('Submit', self.tab3)
        submit_button_3.clicked.connect(self.submit_info_3)

        g_layout = QGridLayout()
        g_layout.addWidget(out_label, 0, 0, 1, 1)
        g_layout.addWidget(out_line, 0, 1, 1, 1)
        g_layout.addWidget(in_label, 1, 0, 1, 1)
        g_layout.addWidget(in_line, 1, 1, 1, 1)
        g_layout.addItem(spacerItem, 2, 0, 1, 1)
        g_layout.addWidget(submit_button_3, 3, 0, 1, 1)
        self.tab3.setLayout(g_layout)

        out_line.textChanged.connect(self.check_input_func_3)
        in_line.textChanged.connect(self.check_input_func_3)

        self.tab3.out_line = out_line
        self.tab3.in_line = in_line
        self.tab3.submit_button = submit_button_3

    def check_input_func_3(self):
        if self.tab3.out_line.text() and self.tab3.in_line.text():
            self.tab3.submit_button.setEnabled(True)
        else:
            self.tab3.submit_button.setEnabled(False)

    def submit_info_3(self):
        cur_ID = self.tab1.id_lab.text()
        leaving_time = self.tab3.out_line.text()
        return_time = self.tab3.in_line.text()
        print(cur_ID)
        # 把字符串转为时间类型
        leaving_datetime = datetime.datetime.strptime(leaving_time,'%Y-%m-%d %H:%M:%S')
        return_datetime = datetime.datetime.strptime(return_time,'%Y-%m-%d %H:%M:%S')
        print(leaving_datetime)
        print(return_datetime)
        # 检查时间差不超过48h
        inter = return_datetime - leaving_datetime
        flag = (inter <= datetime.timedelta(days=2))

        # 检查时间重叠部分
        cursor = conn.cursor()
        cursor.execute("SELECT app_id FROM Application "
                       "WHERE "
                       "    (state LIKE 'pending' OR state LIKE 'passed' OR state LIKE 'refused') AND "
                       "    app_creator_id LIKE %s AND "
                       "    ((out_time <= %s AND in_time > %s) OR "
                       "    (out_time > %s AND out_time < %s)) ",
                       (cur_ID, leaving_time, leaving_time, leaving_time, return_time)
                       )
        results = cursor.fetchall()

        # 算出离开周的起始和末尾
        leaving_date = leaving_time[:10]
        str_s = leaving_date + ' 00:00:00'
        str_f = leaving_date + ' 23:59:59'
        datetime_s = datetime.datetime.strptime(str_s,'%Y-%m-%d %H:%M:%S')
        datetime_f = datetime.datetime.strptime(str_f, '%Y-%m-%d %H:%M:%S')

        x = leaving_datetime.weekday() # 离开的星期数-1
        week_begin = datetime_s - datetime.timedelta(days=x)
        week_end = datetime_f + datetime.timedelta(days=6 - x)
        week_begin_str = week_begin.strftime('%Y-%m-%d %H:%M:%S') # 该周起始
        week_end_str = week_end.strftime('%Y-%m-%d %H:%M:%S') # 该周结束

        # 检查一周离校次数
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Application "
                       "WHERE "
                       "    (state = 'pending' OR state = 'passed' OR state = 'refused') AND "
                       "    app_creator_id LIKE %s AND "
                       "    out_time >= %s AND "
                       "    out_time < %s ",
                       (cur_ID, week_begin_str, week_end_str)
                       )
        result1 = cursor.fetchall()

        if len(results) == 0 and flag and result1[0][0] < 3:
            QMessageBox.information(self, 'Information', 'You have applied!')
            print('Application id = ', self.tab3.app_ID)
            cursor.execute("INSERT INTO Application values(%s, %s, %s, %s,%s)",
                           (self.tab3.app_ID, 'pending', cur_ID, leaving_time, return_time))
            cursor.close()
            conn.commit()
            self.tab3.out_line.clear()
            self.tab3.in_line.clear()
        elif flag == 0:
            QMessageBox.critical(self, 'Wrong', 'Check your time interval shorter than 48h!')
        elif flag == 1 and len(results) != 0:
            QMessageBox.critical(self, 'Wrong', 'Time overlap!')
        elif flag ==1 and len(results) == 0 and result1[0][0] >= 3:
            QMessageBox.critical(self, 'Wrong', 'This week you have been out three times!')

    def tab4_init(self):
        app_label = QLabel('Application ID:', self.tab4)
        app_line = QLineEdit(self.tab4)
        state_label = QLabel('State:', self.tab4)
        items = ['Please choose the status of the application', 'passed', 'refused']
        state_combo = QComboBox(self.tab4)
        state_combo.addItems(items)
        submit_button_4 = QPushButton('Submit', self.tab4)
        comment_label = QLabel('Comment:', self.tab4)
        comment_line = QLineEdit(self.tab4)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        submit_button_4.clicked.connect(self.submit_info_4)

        g_layout = QGridLayout()
        g_layout.addWidget(app_label, 0, 0, 1, 1)
        g_layout.addWidget(app_line, 0, 1, 1, 1)
        g_layout.addWidget(state_label, 1, 0, 1, 1)
        g_layout.addWidget(state_combo, 1, 1, 1, 1)
        g_layout.addWidget(comment_label, 2, 0, 1, 1)
        g_layout.addWidget(comment_line, 2, 1, 1, 1)
        g_layout.addWidget(submit_button_4, 4, 0, 1, 1)
        g_layout.addItem(spacerItem, 3, 0, 1, 1)

        self.tab4.setLayout(g_layout)

        app_line.textChanged.connect(self.check_input_func_4)
        comment_line.textChanged.connect(self.check_input_func_4)

        self.tab4.app_line = app_line
        self.tab4.state_combo = state_combo
        self.tab4.comment_line = comment_line
        self.tab4.submit_button_4 = submit_button_4

    def check_input_func_4(self):
        if self.tab4.app_line.text() and self.tab4.state_combo.currentText():
            self.tab4.submit_button_4.setEnabled(True)
        else:
            self.tab4.submit_button_4.setEnabled(False)

    def submit_info_4(self):
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(app_id) FROM Application WHERE app_id LIKE %s",
                       (self.tab4.app_line.text(),))
        results = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("SELECT app_creator_id FROM Application WHERE app_id LIKE %s",
                       (self.tab4.app_line.text(), ))
        stu = cursor.fetchall()
        stu_id = stu[0][0]

        cursor = conn.cursor()
        cursor.execute("SELECT user_dep_id FROM my_User WHERE user_id LIKE %s",
                       (stu_id,))
        stu = cursor.fetchall()
        stu_dep = stu[0][0]

        cursor = conn.cursor()
        cursor.execute("SELECT user_dep_id FROM my_User WHERE user_id LIKE %s",
                       (self.tab1.id_lab.text(),))
        adm = cursor.fetchall()
        adm_dep = adm[0][0]

        adm_id = self.tab1.id_lab.text()

        com = self.tab4.comment_line.text()

        if len(results) != 0 and adm_dep == stu_dep and adm_id[0] == '0':
            cursor = conn.cursor()
            cursor.execute("UPDATE Application SET state = %s WHERE app_id LIKE %s",
                           (self.tab4.state_combo.currentText(),
                            self.tab4.app_line.text()))
            cursor.close()
            conn.commit()
            cursor = conn.cursor()
            cursor.execute("UPDATE Application SET app_commenter_id = %s WHERE app_id LIKE %s",
                           (adm_id,
                            self.tab4.app_line.text()))
            cursor.close()
            conn.commit()
            if com:
                cursor = conn.cursor()
                cursor.execute("UPDATE Application SET comment = %s WHERE app_id LIKE %s",
                               (self.tab4.comment_line.text(),
                                self.tab4.app_line.text()))
                cursor.close()
                conn.commit()
            QMessageBox.information(self, 'Information', 'You have updated the state')
            self.tab4.app_line.clear()
            self.tab4.comment_line.clear()
        else:
            self.tab4.app_line.clear()
            self.tab4.comment_line.clear()
            QMessageBox.critical(self, 'Wrong', 'You are not allowed to update the state!')


    def tab5_init(self):
        # table = QTableWidget(1, 11)
        table = QTableView()
        table.setSortingEnabled(True)

        app_label = QLabel('Application ID:', self.tab5)
        app_line = QLineEdit(self.tab5)
        status_label = QLabel('State:', self.tab5)
        items_status = ['', 'passed', 'pending', 'refused', 'cancelled']
        status_combo = QComboBox(self.tab5)
        status_combo.addItems(items_status)
        sort_label = QLabel('Sort:', self.tab5)
        items_status = ['', 'DESC', 'ASC']
        sort_combo = QComboBox(self.tab5)
        sort_combo.addItems(items_status)
        submit_button_5 = QPushButton('Search', self.tab5)

        submit_button_5.clicked.connect(self.search_func_5)

        g_layout = QGridLayout()
        g_layout.addWidget(app_label, 0, 0, 1, 1)
        g_layout.addWidget(app_line, 0, 1, 1, 1)
        g_layout.addWidget(status_label, 1, 0, 1, 1)
        g_layout.addWidget(status_combo, 1, 1, 1, 1)
        g_layout.addWidget(sort_label, 2, 0, 1, 1)
        g_layout.addWidget(sort_combo, 2, 1, 1, 1)
        g_layout.addWidget(submit_button_5, 3, 0, 1, 2)
        g_layout.addWidget(table, 4, 0, 1, 2)

        self.tab5.setLayout(g_layout)

        self.tab5.table = table
        self.tab5.app_line = app_line
        self.tab5.status_combo = status_combo
        self.tab5.sort_combo = sort_combo
        self.tab5.submit_button_5 = submit_button_5

    def search_func_5(self):
        appID = self.tab5.app_line.text()
        cur_ID = self.tab1.id_lab.text()
        status = self.tab5.status_combo.currentText()
        sort = self.tab5.sort_combo.currentText()

        cursor = conn.cursor()
        cursor.execute("SELECT user_dep_id FROM my_User WHERE user_id LIKE %s",
                       (cur_ID,))
        adm = cursor.fetchall()
        adm_dep = adm[0][0]
        print(adm_dep)

        if cur_ID[0] == '1':
            query = f"SELECT * FROM Application WHERE app_creator_id='{cur_ID}' "
            if appID:
                query += f" AND app_id='{appID}'"

            if status:
                query += f" AND state='{status}'"

            if sort:
                print(sort)
                if sort == 'DESC':
                    query += " ORDER BY out_time DESC"
                if sort == 'ASC':
                    query += " ORDER BY out_time ASC"
        else:
            query = f"SELECT * FROM Application JOIN my_User ON app_creator_id = user_id WHERE user_dep_id ='{adm_dep}'"
            if appID:
                query += f" AND app_id='{appID}'"

            if status:
                query += f" AND state='{status}'"

            if sort:
                if sort == 'DESC':
                    query += " ORDER BY out_time DESC, in_time DESC"
                if sort == 'ASC':
                    query += " ORDER BY out_time ASC, in_time DESC"

        print(query + '\n')

        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
        cursor.close()
        conn.commit()

        model = QStandardItemModel(len(results), 7)
        self.tab5.table.setModel(model)
        for row in range(len(results)):
            for column in range(7):
                model.setItem(row, column, QStandardItem('%s' % (results[row][column], )))
        self.tab5.table.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Mainwindow()
    mainwindow.show()
    sys.exit(app.exec_())
