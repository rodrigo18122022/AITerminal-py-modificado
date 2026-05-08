# AiTerminal

## 1. Repositorio del Proyecto

El código fuente del proyecto se encuentra disponible en el siguiente repositorio de GitHub:

```text
https://github.com/rodrigo18122022/AITerminal-py-modificado
```

El repositorio contiene tanto la versión basada en consola (`CLI.py`) como la versión con interfaz gráfica (`UI.py`) del sistema **AiTerminal**.

---

## 2. Descripción General

El presente proyecto corresponde a una terminal interactiva desarrollada en Python, diseñada para ofrecer funcionalidades de administración básica del sistema, ejecución de comandos personalizados e integración con herramientas de inteligencia artificial.

La aplicación fue desarrollada utilizando las siguientes tecnologías:

- Lenguaje de programación Python 3.11
- Interfaz gráfica Tkinter
- Librería g4f para integración de funcionalidades de inteligencia artificial
- Librería requests para peticiones HTTP
- Librería BeautifulSoup4 (bs4) para procesamiento de contenido HTML

El sistema dispone de dos modos de ejecución:

- Versión por consola (`CLI.py`)
- Versión con interfaz gráfica (`UI.py`)

La aplicación permite realizar operaciones como:

- Navegación entre directorios
- Gestión de archivos y carpetas
- Ejecución de código Python
- Búsqueda de archivos
- Operaciones matemáticas mediante calculadora integrada
- Interacción con inteligencia artificial mediante comandos personalizados
- Visualización estructurada de directorios
- Interfaz gráfica moderna estilo terminal

---

## 3. Requisitos del sistema

### 3.1. Requisitos Generales

Antes de ejecutar el proyecto, es necesario contar con los siguientes componentes instalados en el sistema:

- Python 3.11
- pip (gestor de paquetes de Python)
- PowerShell o terminal de comandos
- Git (opcional, únicamente si se desea clonar el repositorio)

### 3.2. Requisitos para Windows

Para entornos Windows, el proyecto fue probado utilizando:

- Windows 10 / Windows 11
- Python 3.11
- PowerShell

Verificación de Python:

```powershell
py -3.11 --version
```

El sistema debe mostrar una salida similar a:

```text
Python 3.11.x
```

---

## 4. Obtención del Código Fuente

Clonar el repositorio:

```powershell
git clone https://github.com/rodrigo18122022/AITerminal-py-modificado.git
```

Ingresar a la carpeta del proyecto:

```powershell
cd AITerminal-py-modificado
```

---

## 5. Configuración del Entorno Virtual

Con el objetivo de aislar las dependencias del proyecto y evitar conflictos con otras instalaciones de Python, se recomienda utilizar un entorno virtual.

### 5.1. Creación del entorno virtual

Ejecutar el siguiente comando:

```powershell
py -3.11 -m venv venv311
```

Este comando generará una carpeta denominada:

```text
venv311
```

La cual contendrá todas las dependencias necesarias para el proyecto.

### 5.2. Activación del entorno virtual

Una vez creado el entorno virtual, se debe activar mediante:

```powershell
.\venv311\Scripts\Activate.ps1
```

---

## 6. Instalación de Dependencias

Con el entorno virtual activado, se debe actualizar el gestor de paquetes pip:

```powershell
python -m pip install --upgrade pip
```

Posteriormente, instalar las dependencias necesarias para el funcionamiento del proyecto.

### 6.1. Instalación de Requests

```powershell
pip install requests
```

La librería `requests` permite realizar peticiones HTTP desde Python.

### 6.2. Instalación de g4f

```powershell
pip install g4f
```

La librería `g4f` permite integrar funcionalidades de inteligencia artificial dentro del sistema.

### 6.3. Instalación de BeautifulSoup4

```powershell
pip install bs4
```

La librería `BeautifulSoup4` es utilizada para el procesamiento y análisis de contenido HTML.

---

## 7. Ejecución del Sistema

El proyecto dispone de dos modos principales de ejecución.

### 7.1. Ejecución de la versión en consola

Para ejecutar la versión basada en terminal de comandos, utilizar:

```powershell
python CLI.py
```

Esta versión permite interactuar con el sistema mediante comandos escritos directamente en consola.

### 7.2. Ejecución de la versión con interfaz gráfica

Para ejecutar la versión con interfaz gráfica desarrollada en Tkinter:

```powershell
python UI.py
```

Esta versión incorpora mejoras visuales y funcionalidades adicionales, entre ellas:

- Interfaz gráfica moderna estilo terminal
- Barra de estado dinámica
- Historial de comandos
- Botón de ayuda interactivo
- Visualización estructurada de directorios
- Sistema de búsqueda de archivos
- Calculadora integrada
