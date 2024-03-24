import math

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPainterPath, QPen, QColor
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsPathItem, QGraphicsRectItem, \
    QGraphicsItem


class DrawingArea(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()
        self.radius = 0
        self.spanAngle = 0
        self.startAngle = 0
        self.angle = 0

        self.setSceneRect(0, 0, 1000, 700)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.drawings = []
        self.action = 'cursor'
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.temp_line = self.temp_path_item = self.temp_rect_item = None

        self.border = QGraphicsRectItem(0, 0, 1000, 700)
        self.border.setPen(QPen(Qt.PenStyle.DashLine))
        self.scene.addItem(self.border)

    def printDrawings(self):
        print("Generating G-Code")
        g_code = ""
        for item in self.drawings:
            if isinstance(item, QGraphicsLineItem):
                line = item.line()
                print(f"G01 X{int(line.x1())*10} Y-{int(line.y1())*10} Z-1; Move to ({line.x1()}, {line.y1()})")
                print(f"G01 X{int(line.x2())*10} Y-{int(line.y2())} Z1; Line from ({line.x1()}, {line.y1()}) to ({line.x2()}, {line.y2()})")
                print(f"G00 Z-1; Move Z up")
                # set the head to the start of the line
                g_code += f"G01 X{int(line.x1())*10} Y-{int(line.y1())*10} Z-1; Move to ({line.x1()}, {line.y1()})\n"
                # draw the line
                g_code += f"G01 X{int(line.x2())*10} Y-{int(line.y2())*10} Z1; Line from ({line.x1()}, {line.y1()}) to ({line.x2()}, {line.y2()})\n"
                # move the head up
                g_code += f"G00 Z-1; Move Z up\n"

            elif isinstance(item, QGraphicsPathItem):
                path = item.path()
                element = path.elementAt(0)
                startX = element.x
                startY = element.y

                # Assuming the path is a circular arc
                rect = path.boundingRect()
                centerX = rect.center().x()
                centerY = rect.center().y()
                I = centerX - startX
                J = centerY - startY

                endX = path.elementAt(1).x
                endY = path.elementAt(1).y

                # Determine direction (G02 for CW, G03 for CCW)
                direction = "G02" if self.isClockwise(item) else "G03"
                print(f"G01 X{startX*10} Y{startY*10} Z-1; Move to ({startX}, {startY})")
                print(f"{direction} X{startX*10} Y{startY*10} Z1 I{I*10} J{J*10}  ; Arc with center ({centerX}, {centerY}), and I{I} J{J}")
                print(f"G00 Z-1; Move Z up")
                # set the head to the start of the arc
                g_code += f"G01 X{startX*10} Y{startY*10} Z-1; Move to ({startX}, {startY})\n"
                # draw the arc
                g_code += f"{direction} X{endX*10} Y{endY*10} Z1 I{I*10} J{J*10}  ; Arc with center ({centerX}, {centerY}), and I{I} J{J}\n"
                # move the head up
                g_code += f"G00 Z-1; Move Z up\n"
        print("Done generating G-Code")
        return g_code

    def isClockwise(self, arcItem):
        if isinstance(arcItem, QGraphicsPathItem):
            path = arcItem.path()
            element = path.elementAt(0)
            startAngle = math.degrees(math.atan2(element.y, element.x))

            secondElement = path.elementAt(1)
            endAngle = math.degrees(math.atan2(secondElement.y, secondElement.x))

            return endAngle < startAngle

        return False

    def undoLastDraw(self):
        if self.drawings:
            self.scene.removeItem(self.drawings.pop())
        else:
            print("Nothing to undo.")

    def draw_line(self):
        if None not in [self.x1, self.y1, self.x2, self.y2]:
            line = self.scene.addLine(self.x1, self.y1, self.x2, self.y2)
            line.setFlags(
                QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.drawings.append(line)

    def draw_arc(self, clockwise=False):
        size = self.radius * 2
        x = self.x1 - self.radius
        y = self.y1 - self.radius

        rect = QRectF(x, y, size, size)

        path = QPainterPath()

        start_x = rect.center().x() + self.radius * math.cos(math.radians(self.angle))
        start_y = rect.center().y() - self.radius * math.sin(math.radians(self.angle))

        path.moveTo(start_x, start_y)
        path.arcTo(rect, self.angle, -self.spanAngle if clockwise else self.spanAngle)

        arcItem = QGraphicsPathItem(path)
        arcItem.setPen(QPen(QColor("black")))
        arcItem.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        self.scene.addItem(arcItem)
        self.drawings.append(arcItem)

    def update_temp_arc(self, clockwise=False):
        size = self.radius * 2
        x = self.x1 - self.radius
        y = self.y1 - self.radius
        rect = QRectF(x, y, size, size)

        path = QPainterPath()

        start_x = rect.center().x() + self.radius * math.cos(math.radians(self.angle))
        start_y = rect.center().y() - self.radius * math.sin(math.radians(self.angle))

        path.moveTo(start_x, start_y)
        path.arcTo(rect, self.angle, -self.spanAngle if clockwise else self.spanAngle)
        if not self.temp_rect_item:
            self.temp_rect_item = QGraphicsRectItem()
            self.temp_rect_item.setPen(QPen(Qt.PenStyle.DashLine))
            self.scene.addItem(self.temp_rect_item)

        self.temp_rect_item.setRect(QRectF(self.x1 - self.radius, self.y1 - self.radius, size, size))

        self.temp_path_item.setPath(path)

    def setAction(self, action):
        self.action = action

    def setAngle(self, angle):
        self.startAngle = angle

    def setRadius(self, radius):
        self.radius = radius

    def setSpanAngle(self, spanAngle):
        self.spanAngle = spanAngle



    def mousePressEvent(self, e):
        pos = self.mapToScene(e.position().toPoint())
        self.x1 = pos.x()
        self.y1 = pos.y()

        #x1 and y1 out of bounds
        if self.x1 < 0:
            self.x1 = 0
        elif self.x1 > 1000:
            self.x1 = 1000
        if self.y1 < 0:
            self.y1 = 0
        elif self.y1 > 700:
            self.y1 = 700

        if self.action == "line":
            self.temp_line = self.scene.addLine(self.x1, self.y1, self.x1, self.y1)
        elif self.action in ["arc_cw", "arc_ccw"]:
            self.temp_path_item = QGraphicsPathItem()
            self.scene.addItem(self.temp_path_item)
            self.temp_path_item.setPen(QPen(QColor("black")))

    def mouseMoveEvent(self, e):
        pos = self.mapToScene(e.position().toPoint())
        self.x2 = pos.x()
        self.y2 = pos.y()

        if self.x2 < 0:
            self.x2 = 0
        elif self.x2 > 1000:
            self.x2 = 1000
        if self.y2 < 0:
            self.y2 = 0
        elif self.y2 > 700:
            self.y2 = 700

        if self.action == "line":
            self.temp_line.setLine(self.x1, self.y1, self.x2, self.y2)
        elif self.action in ["arc_cw", "arc_ccw"]:
            self.update_temp_arc(clockwise=self.action == "arc_ccw")

    def mouseReleaseEvent(self, e):
        pos = self.mapToScene(e.position().toPoint())
        self.x2 = pos.x()
        self.y2 = pos.y()

        if self.x2 < 0:
            self.x2 = 0
        elif self.x2 > 1000:
            self.x2 = 1000
        if self.y2 < 0:
            self.y2 = 0
        elif self.y2 > 700:
            self.y2 = 700

        if self.action == "line":
            self.draw_line()
        elif self.action in ["arc_cw", "arc_ccw"]:
            self.draw_arc(clockwise=self.action == "arc_ccw")
        self.remove_artifacts()

    def remove_artifacts(self):
        if self.temp_rect_item:
            self.scene.removeItem(self.temp_rect_item)
            self.temp_rect_item = None
        if self.temp_path_item:
            self.scene.removeItem(self.temp_path_item)
            self.temp_path_item = None
        if self.temp_line:
            self.scene.removeItem(self.temp_line)
            self.temp_line = None
