"""
Práctica III: Implementación del Algoritmo K-Caminos en Grafos
Algoritmos y Estructuras de Datos
Ingeniería de Sistemas
"""

import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsEllipseItem,
                             QGraphicsLineItem, QGraphicsTextItem,
                             QGraphicsItem, QTabWidget, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget,
                             QLabel, QSpinBox, QHBoxLayout, QPushButton,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
import numpy as np


class Nodo(QGraphicsEllipseItem):
    """Nodo visual en el grafo"""

    def __init__(self, x, y, radius, id, app):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.setBrush(QBrush(QColor(100, 200, 255)))
        self.setPen(QPen(QColor(50, 50, 50), 2))
        self.id = id
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)

        self.text_item = QGraphicsTextItem(f"{chr(65 + self.id)}", self)
        self.text_item.setDefaultTextColor(QColor(0, 0, 0))
        font = QFont("Arial", 12, QFont.Bold)
        self.text_item.setFont(font)
        self.text_item.setPos(-7, -12)

        self.app = app
        self.aristas = []

    def agregar_arista(self, arista):
        self.aristas.append(arista)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for arista in self.aristas:
                arista.actualizar_posiciones()
        return super().itemChange(change, value)


class Arista(QGraphicsLineItem):
    """Arista visual en el grafo"""

    def __init__(self, nodo1, nodo2, peso, scene):
        super().__init__()
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso = peso
        self.scene = scene

        self.text_item = QGraphicsTextItem(str(self.peso))
        self.text_item.setDefaultTextColor(QColor(255, 255, 255))
        font = QFont("Arial", 10, QFont.Bold)
        self.text_item.setFont(font)
        self.scene.addItem(self.text_item)

        self.actualizar_posiciones()
        self.setPen(QPen(QColor(200, 200, 200), 2))

    def actualizar_posiciones(self):
        x1, y1 = self.nodo1.scenePos().x(), self.nodo1.scenePos().y()
        x2, y2 = self.nodo2.scenePos().x(), self.nodo2.scenePos().y()

        self.setLine(x1, y1, x2, y2)
        self.text_item.setPos((x1 + x2) / 2 - 10, (y1 + y2) / 2 - 15)


class AlgoritmoKCaminos:
    """Implementa el algoritmo de k-trayectorias usando potencias de matriz"""

    def __init__(self, matriz_pesos, num_vertices):
        self.matriz_pesos = matriz_pesos
        self.n = num_vertices

        # Matriz de adyacencia binaria
        self.matriz_adyacencia = []
        for i in range(num_vertices):
            fila = []
            for j in range(num_vertices):
                if i != j and matriz_pesos[i][j] > 0:
                    fila.append(1)
                else:
                    fila.append(0)
            self.matriz_adyacencia.append(fila)

        print("\n=== Matriz de Adyacencia Binaria ===")
        print("     A   B   C   D")
        for i in range(num_vertices):
            print(f"{chr(65 + i):3}  {self.matriz_adyacencia[i]}")

    def calcular_matrices_binarias_k_trayectorias(self, max_k=3):
        """Calcula matrices binarias de k-trayectorias usando A^k"""
        A = np.array(self.matriz_adyacencia, dtype=int)

        print("\n=== Matriz A (numpy) ===")
        print(A)

        matrices = [A.copy()]

        A_k = A.copy()
        for k in range(2, max_k + 1):
            A_k = np.matmul(A_k, A)

            print(f"\n=== A^{k} (multiplicación matricial) ===")
            print(A_k)

            matriz_binaria = np.where(A_k > 0, 1, 0)

            print(f"\n=== A^{k} binaria (0 o 1) ===")
            print(matriz_binaria)

            matrices.append(matriz_binaria)

        return [matriz.tolist() for matriz in matrices]


class GrafoApp(QtWidgets.QMainWindow):
    """Aplicación principal con interfaz gráfica"""

    def __init__(self):
        super(GrafoApp, self).__init__()
        self.setWindowTitle("Algoritmo K-Caminos en Grafos - Práctica III")
        self.setGeometry(100, 100, 1300, 900)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 13px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5f62;
            }
            QTableWidget {
                background-color: #3c3c3c;
                color: white;
                gridline-color: #555555;
                border: 1px solid #555555;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0d7377;
            }
            QHeaderView::section {
                background-color: #0d7377;
                color: white;
                padding: 5px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QGraphicsView {
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: white;
                padding: 10px 20px;
                border: 1px solid #555555;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
            }
            QSpinBox {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
                font-size: 14px;
            }
            QMessageBox {
                background-color: #2b2b2b;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
                min-width: 300px;
            }
            QMessageBox QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 8px 20px;
                font-size: 12px;
                border-radius: 4px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #14a085;
            }
        """)

        self.setup_ui()
        self.nodos = []
        self.aristas = []

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        titulo = QLabel("🔗 Práctica III: Algoritmo de K-Trayectorias en Grafos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #14a085; padding: 15px;")
        main_layout.addWidget(titulo)

        controles_layout = QHBoxLayout()

        controles_layout.addWidget(QLabel("Número de Nodos:"))
        self.spinbox_nodos = QSpinBox()
        self.spinbox_nodos.setMinimum(3)
        self.spinbox_nodos.setMaximum(10)
        self.spinbox_nodos.setValue(4)  # Por defecto 4 para el ejemplo
        self.spinbox_nodos.valueChanged.connect(self.cambiar_tamano_matriz)
        controles_layout.addWidget(self.spinbox_nodos)

        self.btn_generar = QPushButton("🎲 Generar Grafo Aleatorio")
        self.btn_generar.clicked.connect(self.generar_grafo_aleatorio)
        controles_layout.addWidget(self.btn_generar)

        self.btn_aplicar = QPushButton("✏️ Aplicar Matriz Manual")
        self.btn_aplicar.clicked.connect(self.aplicar_matriz_manual)
        controles_layout.addWidget(self.btn_aplicar)

        self.btn_limpiar = QPushButton("🗑️ Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar_todo)
        controles_layout.addWidget(self.btn_limpiar)

        self.btn_calcular = QPushButton("🧮 Calcular K-Trayectorias")
        self.btn_calcular.clicked.connect(self.calcular_k_caminos)
        controles_layout.addWidget(self.btn_calcular)

        controles_layout.addStretch()
        main_layout.addLayout(controles_layout)

        contenido_layout = QHBoxLayout()

        panel_matriz = QVBoxLayout()
        matriz_label = QLabel("📝 Matriz de Pesos (Editable):")
        matriz_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 10px;")
        panel_matriz.addWidget(matriz_label)

        info_label = QLabel("💡 Ingresa los pesos y presiona 'Aplicar Matriz Manual'")
        info_label.setStyleSheet("font-size: 12px; color: #14a085; font-style: italic;")
        panel_matriz.addWidget(info_label)

        self.tabla_pesos = self.crear_tabla_editable()
        panel_matriz.addWidget(self.tabla_pesos)

        contenido_layout.addLayout(panel_matriz, 1)

        panel_grafo = QVBoxLayout()
        grafo_label = QLabel("🌐 Visualización del Grafo:")
        grafo_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 10px;")
        panel_grafo.addWidget(grafo_label)

        self.graphicsView = QtWidgets.QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMinimumHeight(350)
        panel_grafo.addWidget(self.graphicsView)

        contenido_layout.addLayout(panel_grafo, 2)

        main_layout.addLayout(contenido_layout)

        resultados_label = QLabel("📈 Matrices de K-Trayectorias (valores binarios 0/1):")
        resultados_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(resultados_label)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.tabla_adyacencia = self.crear_tabla()
        self.tab_widget.addTab(self.tabla_adyacencia, "Matriz de Adyacencia (A)")

        self.tabla_k2 = self.crear_tabla()
        self.tab_widget.addTab(self.tabla_k2, "K=2 (A²)")

        self.tabla_k3 = self.crear_tabla()
        self.tab_widget.addTab(self.tabla_k3, "K=3 (A³)")

        self.cambiar_tamano_matriz()

    def crear_tabla(self):
        tabla = QTableWidget()
        tabla.setMinimumHeight(180)
        tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        return tabla

    def crear_tabla_editable(self):
        tabla = QTableWidget()
        tabla.setMinimumHeight(250)
        tabla.setMaximumHeight(300)
        return tabla

    def cambiar_tamano_matriz(self):
        n = self.spinbox_nodos.value()
        self.configurar_tabla(self.tabla_pesos, n, editable=True)

        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                if i == j:
                    item.setBackground(QColor(60, 60, 60))
                    item.setFlags(Qt.ItemIsEnabled)
                else:
                    item.setBackground(QColor(80, 80, 80))
                self.tabla_pesos.setItem(i, j, item)

    def aplicar_matriz_manual(self):
        n = self.tabla_pesos.rowCount()
        matriz = self.obtener_matriz(self.tabla_pesos)

        for i in range(n):
            for j in range(n):
                if i != j and matriz[i][j] < 0:
                    QMessageBox.warning(self, "Error",
                                        f"El peso en ({chr(65 + i)}, {chr(65 + j)}) no puede ser negativo")
                    return

        self.dibujar_grafo(matriz)
        QMessageBox.information(self, "Éxito", "Grafo dibujado correctamente")

    def generar_grafo_aleatorio(self):
        num_nodos = self.spinbox_nodos.value()

        matriz = [[0 for _ in range(num_nodos)] for _ in range(num_nodos)]
        probabilidad_arista = 0.4 + random.random() * 0.2

        for i in range(num_nodos):
            for j in range(i + 1, num_nodos):
                if random.random() < probabilidad_arista:
                    peso = random.randint(1, 15)
                    matriz[i][j] = peso
                    matriz[j][i] = peso

        self.asegurar_conectividad(matriz, num_nodos)
        self.llenar_tabla(self.tabla_pesos, matriz)
        self.dibujar_grafo(matriz)

    def asegurar_conectividad(self, matriz, n):
        visitados = [False] * n

        def dfs(v):
            visitados[v] = True
            for u in range(n):
                if matriz[v][u] > 0 and not visitados[u]:
                    dfs(u)

        dfs(0)

        for i in range(n):
            if not visitados[i]:
                nodo_conectar = random.randint(0, i - 1) if i > 0 else 0
                peso = random.randint(1, 15)
                matriz[i][nodo_conectar] = peso
                matriz[nodo_conectar][i] = peso
                dfs(i)

    def configurar_tabla(self, tabla, n, editable=False):
        tabla.setRowCount(n)
        tabla.setColumnCount(n)

        headers = [chr(65 + i) for i in range(n)]
        tabla.setHorizontalHeaderLabels(headers)
        tabla.setVerticalHeaderLabels(headers)

        if not editable:
            tabla.setEditTriggers(QTableWidget.NoEditTriggers)

    def llenar_tabla(self, tabla, matriz):
        """Llena una tabla con una matriz"""
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                valor = matriz[i][j]

                # Para tabla de pesos
                if tabla == self.tabla_pesos:
                    if i == j:
                        texto = "0"
                    elif valor == 0:
                        texto = "-"
                    else:
                        texto = str(int(valor))
                # Para tablas de resultados (matrices binarias)
                else:
                    # Convertir explícitamente a string el valor de la matriz
                    texto = str(int(valor))

                item = QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignCenter)

                if i == j and tabla == self.tabla_pesos:
                    item.setBackground(QColor(60, 60, 60))
                    item.setFlags(Qt.ItemIsEnabled)
                elif tabla == self.tabla_pesos:
                    item.setBackground(QColor(80, 80, 80))

                tabla.setItem(i, j, item)

    def dibujar_grafo(self, matriz):
        self.scene.clear()
        self.nodos.clear()
        self.aristas.clear()

        n = len(matriz)
        radius = 25

        width = self.graphicsView.width() - 100
        height = self.graphicsView.height() - 100
        center_x = width / 2
        center_y = height / 2
        radio_circulo = min(width, height) / 2 - 50

        import math
        for i in range(n):
            angulo = 2 * math.pi * i / n - math.pi / 2
            x = center_x + radio_circulo * math.cos(angulo)
            y = center_y + radio_circulo * math.sin(angulo)

            nodo = Nodo(x, y, radius, i, self)
            nodo.setPos(x, y)
            self.scene.addItem(nodo)
            self.nodos.append(nodo)

        aristas_dibujadas = set()

        for i in range(n):
            for j in range(n):
                if i != j and matriz[i][j] > 0:
                    if matriz[i][j] == matriz[j][i] and (j, i) in aristas_dibujadas:
                        continue

                    arista = Arista(self.nodos[i], self.nodos[j],
                                    int(matriz[i][j]), self.scene)
                    self.aristas.append(arista)
                    self.scene.addItem(arista)
                    self.nodos[i].agregar_arista(arista)
                    self.nodos[j].agregar_arista(arista)
                    aristas_dibujadas.add((i, j))

    def calcular_k_caminos(self):
        n = self.tabla_pesos.rowCount()
        if n == 0:
            QMessageBox.warning(self, "Advertencia", "Primero genera o edita un grafo")
            return

        matriz = self.obtener_matriz(self.tabla_pesos)

        print("\n=== Matriz de Pesos Leída ===")
        print(f"Tamaño: {n}x{n}")
        for i in range(n):
            print(f"{chr(65 + i)}: {matriz[i]}")

        tiene_aristas = any(matriz[i][j] > 0 for i in range(n) for j in range(n) if i != j)
        if not tiene_aristas:
            QMessageBox.warning(self, "Advertencia",
                                "El grafo no tiene aristas. Agrega pesos en la matriz.")
            return

        algoritmo = AlgoritmoKCaminos(matriz, n)
        matrices_k = algoritmo.calcular_matrices_binarias_k_trayectorias(max_k=3)

        self.configurar_tabla(self.tabla_adyacencia, n)
        self.configurar_tabla(self.tabla_k2, n)
        self.configurar_tabla(self.tabla_k3, n)

        self.llenar_tabla(self.tabla_adyacencia, matrices_k[0])
        self.llenar_tabla(self.tabla_k2, matrices_k[1])
        self.llenar_tabla(self.tabla_k3, matrices_k[2])

        QMessageBox.information(self, "Éxito",
                                "Matrices binarias de k-trayectorias calculadas correctamente\n\n"
                                "• 1 = Existe al menos una k-trayectoria\n"
                                "• 0 = No existe k-trayectoria")

    def limpiar_todo(self):
        self.scene.clear()
        self.nodos.clear()
        self.aristas.clear()
        self.cambiar_tamano_matriz()

        for tabla in [self.tabla_adyacencia, self.tabla_k2, self.tabla_k3]:
            tabla.clear()
            tabla.setRowCount(0)
            tabla.setColumnCount(0)

    def obtener_matriz(self, tabla):
        """Lee la matriz desde la tabla"""
        n = tabla.rowCount()
        matriz = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                item = tabla.item(i, j)
                if item:
                    texto = item.text().strip()
                    if texto and texto not in ["-", "∞", ""]:
                        try:
                            valor = int(texto)
                            matriz[i][j] = max(0, valor)
                        except ValueError:
                            matriz[i][j] = 0

        return matriz


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GrafoApp()
    window.show()
    sys.exit(app.exec_())

