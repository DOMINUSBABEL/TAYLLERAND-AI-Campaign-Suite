# 🦅 TAYLLERAND OS v3.5
### Sistema Operativo de Campaña Neo-Clásico | Est. 2025

![Tayllerand OS Logo](app/static/logo.png)

## 📜 Descripción General
**TAYLLERAND OS** es una plataforma de inteligencia electoral de vanguardia, diseñada bajo una estética "Neo-Clásica Digital" que evoca prestigio, autoridad y control total. Inspirada en las terminales financieras de alta frecuencia y los centros de mando militares, esta herramienta permite a los estrategas políticos monitorear, simular y ejecutar operaciones de campaña con precisión quirúrgica.

La versión **v3.5** introduce una arquitectura de interfaz de 3 columnas, navegación personalizada y un motor de simulación electoral avanzado.

## 🚀 Características Principales

### 1. Dashboard de Comando (3-Column View)
- **Roster de Candidatos**: Selección rápida de objetivos y análisis comparativo.
- **Perfil de Candidato**: Visualización centralizada de capital político, estatus y plataforma.
- **Métricas en Tiempo Real**: Proyección de votos, volumen social y zonas de crecimiento con indicadores de tendencia.

### 2. Inteligencia Geoespacial (Field Ops)
- **Mapas de Calor Dinámicos**: Visualización de densidad de votos, potencial de crecimiento y crisis.
- **Matriz Estratégica**: Clasificación automática de puestos de votación (Bastión, Campo de Batalla, Oportunidad).
- **Rutas Logísticas (TSP)**: Optimización de recorridos para equipos en terreno.

### 3. Inteligencia Social Avanzada (Social Sentinel)
- **Libro de Órdenes de Sentimiento**: Visualización tipo "Trading" de opiniones positivas (Bids) y negativas (Asks).
- **Perfilador de Votantes (KYC)**: Análisis profundo de usuarios individuales para reclutamiento o neutralización.
- **Simulador de Mensajes**: Predicción de impacto y resonancia de mensajes antes de su difusión.

### 4. Plataforma de Simulación (War Room)
- **Gemelo Digital**: Simulación de escenarios electorales basada en datos históricos y tendencias actuales.
- **Constructor de Coaliciones**: Análisis de impacto de alianzas estratégicas.
- **Gamificación GOTV**: Estrategias para maximizar la participación el día D.

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Python 3.8+
- Pip

### Pasos
1.  **Clonar el Repositorio**:
    ```bash
    git clone https://github.com/usuario/tayllerand-os.git
    cd tayllerand-os
    ```

2.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar el Sistema**:
    ```bash
    python -m streamlit run app.py
    ```

4.  **Acceso**:
    El sistema estará disponible en `http://localhost:8501`.

## 📂 Estructura del Proyecto
```
TAYLLERAND/
├── app.py                 # Núcleo del Sistema (Interfaz y Lógica)
├── src/
│   ├── e26_processor.py   # Procesamiento de Datos Electorales
│   ├── social_sentinel.py # Motor de Inteligencia Social
│   ├── targeting_brain.py # Cerebro de Simulación y Estrategia
│   └── survey_handler.py  # Gestión de CRM y Encuestas
├── data/                  # Almacenamiento de Datos (CSV/Parquet)
└── README.md              # Documentación Clasificada
```

## 🔐 Seguridad y Privacidad
Este sistema está clasificado para **SOLO OJOS AUTORIZADOS**. El acceso a los módulos de inteligencia y datos de votantes debe ser restringido según los protocolos de la campaña.

---
*Tayllerand OS - "La política es el arte de lo posible."*
