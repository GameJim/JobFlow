from PyQt5.QtCore import Qt, QRect, QPoint, QPointF

from PyQt5.QtGui import QPen, QPainter, QBrush, QLinearGradient, QConicalGradient, QRadialGradient, QImage, QColor, \
    QPolygon, QFont, QMouseEvent, QPalette
from PyQt5.QtWidgets import QWidget, QTabWidget, QSplitter, QTabWidget, QHBoxLayout, QVBoxLayout, QMenuBar, \
    QListView, QPushButton, QDockWidget, QMainWindow
from jobFlowUI import JobFlowUI


class TemplateUI(QWidget):
    def __init__(self):
        super(TemplateUI, self).__init__()

        mainLayerout = QVBoxLayout()
        self.setLayout(mainLayerout)
        # 菜单
        mainLayerout.addWidget(self.createMenu())
        mainLayerout.addWidget(self.createTabWidget())
        
    def createMenu(self):
        menuBar = QMenuBar()

        cmdMenu = menuBar.addMenu('命令(&S)')
        # menuBar.addAction(fileMenu)

        searchMenu = menuBar.addMenu('查询(&S)')
        # menuBar.addAction(windownsAction)

        exMenu = menuBar.addMenu('拓展(&E)')
        # menuBar.addMenu(fileMenu)
        return menuBar

    def createTabWidget(self):
        tabWidget = QTabWidget()

        def createParamWidge():
            w = QWidget()
            mainLayerout = QVBoxLayout()
            w.setLayout(mainLayerout)
            mainLayerout.addWidget(QPushButton('参数'))
            return QWidget()

        def createJobWidge():
            w = QWidget()
            mainLayerout = QVBoxLayout()
            w.setLayout(mainLayerout)
            mainLayerout.addWidget(QPushButton('测试Search'))
            return QWidget()

        tabWidget.addTab(createParamWidge(), '参数')
        tabWidget.addTab(createJobWidge(), '任务')

        return tabWidget

class JobFlowListUI(QWidget):
    def __init__(self):
        super(JobFlowListUI, self).__init__()
        mainLayerout = QVBoxLayout()
        self.setLayout(mainLayerout)
        # 菜单
        mainLayerout.addWidget(self.createMenu())

    def createMenu(self):
        menuBar = QMenuBar()

        fileMenu = menuBar.addMenu('文件(&F)')
        fileMenu.addAction('导入(&I)')
        fileMenu.addAction('导出(&E)')
        fileMenu.addAction('保存(&S)')
        # menuBar.addAction(fileMenu)

        opMenu = menuBar.addMenu('批操作(&B)')
        opMenu.addAction('启动(&S)')
        opMenu.addAction('取消(&C)')
        # menuBar.addAction(windownsAction)

        toolMenu = menuBar.addMenu('工具(&T)')
        toolMenu.addAction('合并(&M)')
        # menuBar.addMenu(fileMenu)
        return menuBar


class MainFrm(QMainWindow):
    def __init__(self):
        super(MainFrm, self).__init__()

        self.dock = {'template': None, 'jobFlowList': None}
        self.setWindowTitle("自动化脚本")
        self.createMenu()
        self.createLayout()

    def createMenu(self):
        fileMenu = self.menuBar().addMenu('文件(&F)')
        # menuBar.addAction(fileMenu)

        windownsMenu = self.menuBar().addMenu('窗口(&W)')
        # menuBar.addAction(windownsAction)

        settingMenu = self.menuBar().addMenu('设置(&S)')
        # menuBar.addMenu(fileMenu)



    def createLayout(self):
        # mainLayerout = QVBoxLayout()
        # self.setLayout(mainLayerout)
        # splitter1 = QSplitter()
        # splitter1.setOrientation(Qt.Horizontal)
        # mainLayerout.addWidget(splitter1)
        #
        # # 第一个窗口Job Partam  Docker
        # self.dock['template'] = TemplateUI()
        # splitter1.addWidget(self.dock['template'])
        # # 画布窗口
        # splitter1.addWidget(JobFlowUI())
        #
        # # 以及JobFlowList Docker
        # self.dock['jobFlowList'] = JobFlowListUI()
        # splitter1.addWidget(self.dock['jobFlowList'])
        pal = QPalette()
        templateDock = QDockWidget("模板")  # 实例化dockwidget类
        templateDock.setWidget(TemplateUI())  # 带入的参数为一个QWidget窗体实例，将该窗体放入dock中
        templateDock.setObjectName("templateDock")
        templateDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        templateDock.setFeatures(templateDock.DockWidgetFloatable|templateDock.DockWidgetMovable)
        pal.setColor(QPalette.Background, Qt.green)
        templateDock.setAutoFillBackground(True)
        templateDock.setPalette(pal)
        self.addDockWidget(Qt.LeftDockWidgetArea, templateDock)

        self.setCentralWidget(JobFlowUI())

        jobFlowListDock = QDockWidget("任务流")  # 实例化dockwidget类
        jobFlowListDock.setWidget(JobFlowListUI())  # 带入的参数为一个QWidget窗体实例，将该窗体放入dock中
        jobFlowListDock.setObjectName("jobFlowListDock")
        jobFlowListDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        jobFlowListDock.setFeatures(jobFlowListDock.DockWidgetFloatable | jobFlowListDock.DockWidgetMovable)
        jobFlowListDock.setAutoFillBackground(True)
        pal.setColor(QPalette.Background, Qt.blue)
        jobFlowListDock.setAutoFillBackground(True)
        jobFlowListDock.setPalette(pal)
        self.addDockWidget(Qt.RightDockWidgetArea, jobFlowListDock)


