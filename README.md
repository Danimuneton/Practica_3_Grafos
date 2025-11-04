# Práctica III: Algoritmo de K-Trayectorias en Grafos

## 👥 Integrantes del Equipo

- **Mateo Gómez** 
- **Daniel Muñeton** 

**Curso:** Algoritmos y Estructuras de Datos   
**Fecha:** Noviembre 2025

---

## 📋 Descripción

Este proyecto implementa el **algoritmo de k-trayectorias más cortas** en grafos ponderados, calculando matrices binarias que indican la existencia de caminos de longitud k (k=1, 2, 3) entre todos los pares de vértices. Utiliza el método algebraico basado en potencias de la matriz de adyacencia (A, A², A³) y proporciona una interfaz gráfica interactiva desarrollada en PyQt5 para la visualización y análisis de grafos, permitiendo tanto la entrada manual de matrices como la generación aleatoria de grafos no completamente conectados.

---

---

## 🛠️ Requisitos del Sistema

### Dependencias

- **Python 3.8 o superior**
- **PyQt5 5.15 o superior**
- **NumPy 1.20 o superior**

---

## Cómo Compilar y Ejecutar

### 1. Clonar o Descargar el Repositorio
### 2. Ejecutar la Aplicación

La interfaz gráfica se abrirá automáticamente.

---

## 📖 Guía de Uso

### Opción 1: Generar Grafo Aleatorio

1. Selecciona el **número de nodos** deseado (3-10)
2. Haz clic en **"🎲 Generar Grafo Aleatorio"**
3. El grafo se visualizará automáticamente
4. Haz clic en **"🧮 Calcular K-Trayectorias"** para obtener las matrices

### Opción 2: Entrada Manual

1. Selecciona el **número de nodos**
2. Edita los valores en la **Matriz de Pesos** (0 = sin arista, >0 = peso de la arista)
3. Haz clic en **"✏️ Aplicar Matriz Manual"**
4. El grafo se dibujará según tu matriz
5. Haz clic en **"🧮 Calcular K-Trayectorias"**

### Interpretación de Resultados

Las pestañas muestran:
- **Matriz de Adyacencia (A)**: Conexiones directas (1-trayectorias)
- **K=2 (A²)**: 2-trayectorias (caminos de 2 aristas)
- **K=3 (A³)**: 3-trayectorias (caminos de 3 aristas)

**Valores:**
- `1` = Existe al menos una k-trayectoria entre esos vértices
- `0` = No existe k-trayectoria

---


