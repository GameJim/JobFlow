import logging
import uuid
import osJob
from job import paramFactory, Callback,Job,Param, jobFactory
from jobFlow import JobFlow

from PyQt5.QtCore import Qt, QRect, QPoint, QPointF
from PyQt5.QtGui import QPen, QPainter, QBrush, QLinearGradient, QConicalGradient, QRadialGradient, QImage, QColor, \
    QPolygon, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget, QTabWidget


class DrawableFactory:
    # 所有的工场管理器
    drawableFactory = None

    # 注册参数类型
    def register(self, p_type, create):
        self.drawableTemplate[p_type] = create

    def create(self, p_type, jobDrawable=False):
        if p_type not in self.drawableTemplate:#使用默认得
            if jobDrawable:
                return self.drawableTemplate['defaultJob']()
            else:
                return self.drawableTemplate['default']()
        else:
            return self.drawableTemplate[p_type]()

    def __new__(cls, *args, **kwargs):
        if cls.drawableFactory is None:
            cls.drawableFactory = object.__new__(cls)
        return cls.drawableFactory

    def __init__(self):
        self.drawableTemplate = {}


drawableFactory = DrawableFactory()


class Drawable:
    @staticmethod
    def create():
        return Drawable()

    p_type = 'default'
    # 注册对象
    drawableFactory.register(p_type, create.__get__(object))

    def __init__(self, obj):
        self.uid = uuid.uuid1()
        # 当前对象
        self.obj = obj
        # 渲染几何对象锚点
        self.rect = QRect(200, 100, 100, 50)

    def boundbox(self) -> QRect:
        return self.rect

    # 将图形进行移动
    def move(self, pos):
        self.rect.moveCenter(self.rect.center() + pos)

    def drawDrawable(self, painter):
        # 绘制对象圆
        painter.drawEllipse(self.rect)
        return True

    def pick(self, pos):
        return False

#
#     # def _draw(self,canvas):
#     #     qp = QPainter()
#     #     qp.begin(canvas)
#     #     #应用style
#     #     self.applyStyle(qp)
#     #     #绘制几何图形
#     #     self.drawable(qp)
#     #     qp.end(canvas)
#
#     ##############
#     # qp = QPainter()
#     # pen = QPen()
#     # qp.begin(canvas)
#     #
#     # #  todo 画网格代码可不要开始（方便理解）-----------------------------------------------
#     # x, y, w, h, number = 0, 0, 900, 0, 6  # x:起点横坐标，y:起点纵坐标，w:长度，h:高
#     # qp.setPen(QPen(Qt.black, 2, Qt.DashLine))  # 设置画笔颜色，画笔粗细，画笔的画线类型（虚线）
#     # qp.drawLine(150, 0, 150, 600)  # 画第一条竖直虚线
#     # qp.drawLine(300, 0, 300, 600)  # 画第二条竖直虚线
#     # qp.drawLine(450, 0, 450, 600)  # 画第三条竖直虚线
#     # qp.drawLine(600, 0, 600, 600)  # 画第四条竖直虚线
#     # qp.drawLine(900, 0, 900, 600)  # 画第五条竖直虚线，竖直边界
#     # while number > 1:
#     #     # 画横虚线
#     #     qp.drawLine(x, y, w, h)
#     #     w = 600
#     #     y += 150
#     #     h += 150
#     #     number -= 1
#     #     if number == 2:  # 画最后一条横线时，需要加长到900
#     #         w += 300
#     #
#     # # todo 画网格代码不要结束-------------------------------------------------------------------
#     #
#     # pen.setWidth(4)  # 设置画笔粗细
#     # pen.setColor(Qt.blue)  # 设置画笔颜色：蓝
#     # qp.setPen(pen)  # 设置的画笔
#     # # 绘制弧
#     # rect = QRect(30, 25, 100, 100)  # (x:起始横坐标，y:起始纵坐标，w:长，h:高)
#     # #  alen: 1个 alen 等于1/16度，例如90°则需要 90 * 16
#     # qp.drawArc(rect, 90 * 16, 90 * 16)  # 90 * 16 旋转角度， 90 * 16 弧度
#     #
#     # # 绘制圆
#     # pen.setColor(Qt.red)  # 设置画笔颜色：红
#     # qp.setPen(pen)  # 设置的画笔
#     # qp.drawArc(180, 25, 100, 100, 0 * 16, 360 * 16)
#     #
#     # # 绘制椭圆
#     # pen.setColor(Qt.yellow)  # 设置画笔颜色：黄
#     # qp.setPen(pen)  # 设置的画笔
#     # qp.drawArc(10, 200, 130, 50, 0 * 16, 360 * 16)
#     #
#     # # 绘制带弦的弧
#     # pen.setColor(Qt.green)  # 设置画笔颜色：绿
#     # qp.setPen(pen)  # 设置的画笔
#     # qp.drawChord(180, 200, 100, 50, 0 * 16, 180 * 16)  # 横起，纵起，弦长，弧高，旋转角度，结束弧度
#     #
#     # # 绘制扇形
#     # pen.setColor(Qt.gray)  # 设置画笔颜色：灰
#     # qp.setPen(pen)  # 设置的画笔
#     # qp.drawPie(0, 350, 150, 150, 45 * 16, 90 * 16)  # 横起，纵起，弦长，弧高，旋转角度，
#     #
#     # # 多边形
#     # pen.setColor(Qt.magenta)  # 设置画笔颜色：洋红色
#     # qp.setPen(pen)  # 设置的画笔
#     # """
#     # 坐标需要精确计算，以point1为初始点
#     # point2坐标连接point1，point3坐标连接point2
#     # 以此类推，最后point6连接point1
#     # """
#     # point1 = QPoint(200, 325)  # 坐标点一
#     # point2 = QPoint(260, 325)  # 坐标点二
#     # point3 = QPoint(285, 375)  # 坐标点三
#     # point4 = QPoint(260, 425)  # 坐标点四
#     # point5 = QPoint(200, 425)  # 坐标点五
#     # point6 = QPoint(175, 375)  # 坐标点六
#     # polygon = QPolygon([point1, point2, point3, point4, point5, point6])  # 六个点坐标
#     # qp.drawPolygon(polygon)  # 画多边形
#     #
#     # # 绘制多个虚线圆
#     # pen = QColor(0, 0, 0)  # 设置画笔初始颜色
#     # pen.setNamedColor('#7300FF')  # 设置色号
#     # qp.setPen(QPen(pen, 3, Qt.DashLine))  # 设置画笔颜色， 粗细， 画线方式
#     # qp.drawArc(20, 480, 100, 100, 0, 360 * 16)  # 坐标
#     # while True:
#     #     for Arc_x in range(2, 5):
#     #         qp.drawArc(Arc_x * 17, Arc_x * 10 + 480, Arc_x * 10, Arc_x * 10, 0, 360 * 16)  # 坐标
#     #     break
#     #
#     # # 绘制点线正方形
#     # pen = QColor(0, 0, 0)  # 设置画笔初始颜色
#     # pen.setNamedColor('#ff8b02')  # 设置色号
#     # qp.setPen(QPen(pen, 3, Qt.DashDotLine))  # 设置画笔颜色， 粗细， 画线方式
#     # point1 = QPoint(170, 490)  # 点坐标一
#     # point2 = QPoint(280, 490)  # 点坐标二
#     # point3 = QPoint(280, 560)  # 点坐标三
#     # point4 = QPoint(170, 560)  # 点坐标四
#     # polygon = QPolygon([point1, point2, point3, point4])  # 四个点坐标
#     # qp.drawPolygon(polygon)  # 画多边形的方式画矩形
#     #
#     # # 绘制渐变色线段
#     # pen = QLinearGradient(QPointF(300, 10), QPointF(300, 100))  # 设置颜色起始，结束位置
#     # pen.setColorAt(0, Qt.magenta)  # 设置渐变颜色一
#     # pen.setColorAt(1, Qt.green)  # 设置渐变颜色二
#     # qp.setPen(QPen(pen, 5, Qt.SolidLine))  # 画实线段
#     # qp.drawLine(335, 20, 335, 130)  # 实线段坐标
#     # qp.setPen(QPen(pen, 5, Qt.DashLine))  # 画虚线段
#     # qp.drawLine(355, 20, 355, 140)  # 虚线段坐标
#     # qp.setPen(QPen(pen, 5, Qt.DashDotLine))  # 画点划线段
#     # qp.drawLine(375, 20, 375, 140)  # 点划线段坐标
#     # qp.setPen(QPen(pen, 5, Qt.DotLine))  # 画密集虚线段
#     # qp.drawLine(395, 20, 395, 140)  # 密集虚线段坐标
#     # qp.setPen(QPen(pen, 5, Qt.DashDotDotLine))  # 点点划线段
#     # qp.drawLine(415, 20, 415, 140)  # 点点划线段坐标
#     #
#     # # 渐变色字体（色彩区域暂时未能调试成功）
#     # pen = QLinearGradient(QPointF(350, 10), QPointF(350, 100))  # 设置颜色起始，结束位置
#     # pen.setColorAt(0, Qt.red)  # 设置渐变颜色一
#     # pen.setColorAt(1, Qt.blue)  # 设置渐变颜色二
#     # qp.setFont(QFont('SimSun', 20))  # 设置字体，字号
#     # qp.setBrush(pen)  # 画刷
#     # qp.drawText(480, 70, "测试字体")  # 文本位置，文本内容
#     #
#     # # 绘制图像
#     # # image = QImage(r'C:\Users\点雨洛\Desktop\小人.png')  # 图片路径
#     # # rect = QRect(600, 0, image.width() / 3.2, image.height() / 3.95)  # 图片放置坐标，长，高缩放的倍数
#     # # qp.drawImage(rect, image)  # 画出图片
#     #
#     # qp.end()  # 结束整个画图
#     #
#     # return False
#
#     def draw(self, canvas):
#         qp = QPainter()
#         qp.begin(canvas)
#
#         # 绘制本体部分
#         # 应用style
#         self.applyStyle(qp)
#         # 绘制几何图形
#         self.drawDrawable(qp)
#         qp.end(canvas)
#
#


class JobDrawable(Drawable):
    # 参数圆大小

    @staticmethod
    def create():
        return JobDrawable()

    p_type = 'defaultJob'
    # 注册对象
    drawableFactory.register(p_type, create.__get__(object))
    r = 20

    def boundbox(self):
        return QRect(self.rect.left(), self.rect.top(), self.rect.width(), self.rect.height() + Drawable * 1.5)

    def drawDrawable(self, painter):
        # 绘制对象矩形
        pen = QPen()
        pen.setColor(QColor(0, 0, 0))
        pen.setWidth(2)
        pen.setBrush(QColor(255, 2552, 55))
        # pen.setStyle(Qt.DashLine)
        # pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(QColor(0, 255, 0))

        painter.drawRect(self.rect)

        # 输入
        nInput = len(self.obj.inputParamType)
        nstep = (self.rect.width() - JobDrawable.r * nInput) / (nInput + 1)
        # 绘制输入矩形
        index = 1.0

        topLeft = self.rect.topLeft()
        for key, paratm in self.obj.inputParamType.items():
            # 输入参数对应的矩形
            rect = QRect(0, 0, JobDrawable.r, JobDrawable.r)

            pos = QPoint(int(nstep * index + JobDrawable.r * (index - 0.5)), int(JobDrawable.r * -0.5))
            pos = topLeft + pos
            rect.moveCenter(rect.center() + pos)

            # 绘制对应参数
            pen.setColor(QColor(127, 127, 127))
            pen.setWidth(1)
            pen.setBrush(QColor(255, 2552, 55))
            # pen.setStyle(Qt.DashDotLine)
            # pen.setStyle(Qt.NoPen)
            painter.setPen(pen)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 255))

            painter.drawEllipse(rect)

            index = index + 1.0

        # 输出
        nInput = len(self.obj.outputParams)
        nstep = (self.rect.width() - JobDrawable.r * nInput) / (nInput + 1)
        # 绘制输入矩形
        index = 1.0

        topLeft = self.rect.bottomLeft()
        for key, paratm in self.obj.outputParams.items():
            # 输入参数对应的矩形
            rect = QRect(0, 0, JobDrawable.r, JobDrawable.r)

            pos = QPoint(int(nstep * index + JobDrawable.r * (index - 0.5)), int(JobDrawable.r * -0.5))
            pos = topLeft + pos
            rect.moveCenter(rect.center() + pos)

            # 绘制对应参数
            pen.setColor(QColor(127, 127, 127))
            pen.setWidth(1)
            pen.setBrush(QColor(255, 2552, 55))
            # pen.setStyle(Qt.DashDotLine)
            # pen.setStyle(Qt.NoPen)
            painter.setPen(pen)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 0, 0))

            painter.drawEllipse(rect)

            index = index + 1.0

        return True

    def pick(self, pos):
        # 检测是否在输入函数里
        nInput = len(self.obj.inputParamType)
        nstep = (self.rect.width() - JobDrawable.r * nInput) / (nInput + 1)
        # 绘制输入矩形
        index = 1.0

        topLeft = self.rect.topLeft()
        for key, paratm in self.obj.inputParamType.items():
            # 输入参数对应的矩形
            rect = QRect(0, 0, JobDrawable.r, JobDrawable.r)

            pos = QPoint(int(nstep * index + JobDrawable.r * (index - 0.5)), int(JobDrawable.r * -0.5))
            pos = topLeft + pos
            rect.moveCenter(rect.center() + pos)

            if rect.contains(pos):
                return ['job_input', key, rect.center()]

        nInput = len(self.obj.outputParams)
        nstep = (self.rect.width() - JobDrawable.r * nInput) / (nInput + 1)
        # 绘制输入矩形
        index = 1.0

        topLeft = self.rect.bottomLeft()
        for key, paratm in self.obj.outputParams.items():
            # 输入参数对应的矩形
            rect = QRect(0, 0, JobDrawable.r, JobDrawable.r)

            pos = QPoint(int(nstep * index + JobDrawable.r * (index - 0.5)), int(JobDrawable.r * -0.5))
            pos = topLeft + pos
            rect.moveCenter(rect.center() + pos)

            if rect.contains(pos):
                return ['job_output', key, rect.center()]

        # 检测是否为主题锁包含
        if self.rect.left() == pos.x():
            return ['boundbox', 'l']
        elif self.rect.right() == pos.x():
            return ['boundbox', 'r']
        elif self.rect.top() == pos.y():
            return ['boundbox', 't']
        elif self.rect.bottom() == pos.y():
            return ['boundbox', 'b']

        if self.rect.contains(pos):
            return ['obj']

        return None


class JobFlowUI(QWidget):
    class AddCallback(Callback):
        def __init__(self, ui):
            super().__init__()
            self.ui = ui

        def call(self, obj):
            if isinstance(obj, Job):
                drawable = drawableFactory.create(obj.jobName(), True)
                drawable.move(QPoint(500, 500))
                self.ui.drawables[obj.uid] = drawable
            else:
                drawable = drawableFactory.create(obj.paramType())
                drawable.move(QPoint(500, 500))
                self.ui.drawables.append(drawable)
                self.ui.drawables[obj.uid] = drawable
            self.ui.update()

    class RemoveCallback(Callback):
        def __init__(self, ui):
            super().__init__()
            self.ui = ui

        def call(self, obj):
            self.ui.drawables.remove(obj.uid)
            #销毁掉
            obj.destory()
            self.ui.update()

    def __init__(self, jobflow=None):
        super(JobFlowUI, self).__init__()
        self.uid = uuid.uuid1()

        if jobflow is None:
            self.jobflow = JobFlow()
        else:
            self.jobflow = jobflow

        # 添加AddCallback
        self.jobflow.addCallback(JobFlowUI.AddCallback(self), 'addJob')
        self.jobflow.addCallback(JobFlowUI.AddCallback(self), 'addParam')
        #添加removecallback
        self.jobflow.addCallback(JobFlowUI.RemoveCallback(self), 'removeJob')
        self.jobflow.addCallback(JobFlowUI.RemoveCallback(self), 'removeParam')
        # 渲染数据
        self.drawables = {}

        job = jobFactory.create('pathMerge')
        base = paramFactory.create('aPath')
        paramDrawable = Drawable(base)
        self.drawables[paramDrawable.uid] = paramDrawable

        jobDrawable = JobDrawable(job)
        self.drawables[jobDrawable.uid] = jobDrawable


        # 绑定
        # self.jobflow.addCallback(self.callbacks['addJobCallback'], 'job')
        #
        # # 当前激活的对象
        # self.activeRenderable = None
        #
        # # 记录按下事件
        # self.mouseState = {}
        # # 依据选中数据设置对应状态
        #
        # # 选中状态
        # self.pickState = {}
        # 'pick': 'obj', 'obj_boundbox', 'job-ouput', 'job-input'
        # 'renderable',renderable

        # self.buttonPressEvent = None
        # self.mousePos = None

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for sid, drawable in self.drawables.items():
            drawable.drawDrawable(painter)

        painter.end()

    # def mouseDoubleClickEvent(self, event):
    #     # copy_job = jobFactory.createJob('file_c')
    #     copy_job = jobFactory.createJob('path_m')
    #     self.jobflow.addJob(copy_job)
    #     # 先检测查询到的对象
    #     # 如果是Job 则判断是否点击到输入框，如果是则进行输入按钮弹窗
    #
    #     # 如果是Job自己本身。则弹出所有
    #
    #     # 如果是Param 则弹出对应的参数框
    #
    # def mouseMoveEvent(self, event):
    #     if self.activeRenderable:
    #         if self.buttonPressEvent:
    #             print(event.pos())
    #             print(event.pos())
    #             print(self.mousePos)
    #             pos = event.pos() - self.mousePos
    #             # print(pos)
    #             self.activeRenderable.move(pos)
    #
    #     self.mousePos = event.pos()
    #     self.update()
    #
    # def mousePressEvent(self, event):
    #     # 记录鼠标状态
    #     self.mouseState['Press_Pos'] = event.pos()
    #     # print(event)
    #     if event.buttons() == Qt.LeftButton:
    #         self.mouseState['LButton_Press'] = True
    #         # 选中参数划线
    #     elif event.buttons == Qt.MidButton:
    #         self.mouseState['MButton_Press'] = True
    #         for renderable in self.renderbales:
    #             self.mouseState['pick'] = renderable.pick(self.mouseState['Press_Pos'])
    #             if self.mouseState['pick']:
    #                 self.activeRenderable = renderable
    #                 break
    #
    #         # 选中对象进行平移
    #     elif event.buttons == Qt.RightButton:
    #         self.mouseState['RButton_Press'] = True
    #
    #     return
    #
    # def mouseReleaseEvent(self, event):
    #     # 记录鼠标状态
    #     self.mouseState['Press_Pos'] = None
    #     if event.buttons() == Qt.LeftButton:
    #         self.mouseState['LButton_Press'] = False
    #
    #     elif event.buttons == Qt.MidButton:
    #         self.mouseState['MButton_Press'] = False
    #
    #
    #
    #     elif event.buttons == Qt.RightButton:
    #         self.mouseState['RButton_Press'] = False
    #     return
    # 创建任务对应的几何形态
    # def createJobGeometry(self, job):
    #     return None
    #
    # def createParamGeometry(self, param):
    #     return None
    #
    #     # 绘制任务
    #
    # def drawJob(self, job):
    #     return False
    #
    #     # 绘制任务
    #
    # def drawParam(self, Param):
    #     return False
    #
    #     # 绘制任务
    #
    # def drawParam(self, Param):
    #     return False
    #
    # def drawArrow(self, painter, start, end):
    #     if start == end:
    #         return