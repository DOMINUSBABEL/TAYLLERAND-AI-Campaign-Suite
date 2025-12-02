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
- **Simulador de Mensajes**: Predicción de impacto de mensajes.

### 4. Plataforma de Simulación (War Room)
- **Gemelo Digital**: Simulación de escenarios electorales.
- **Constructor de Coaliciones**: Análisis de impacto de alianzas.
- **Gamificación GOTV**: Estrategias para maximizar la participación.

## 🏗️ Arquitectura Técnica (DevSecOps)

El sistema ha sido refactorizado siguiendo principios de **DevSecOps** y **Arquitectura Modular**:

### Estructura Modular
```
TAYLLERAND/
├── app.py                 # Punto de entrada principal
├── src/
│   ├── components/        # Componentes UI (Vistas)
│   │   ├── layout.py      # Configuración y CSS global
│   │   ├── map.py         # Lógica de mapas Folium
│   │   └── ...
│   └── services/          # Lógica de Negocio (Controladores)
│       ├── e26_processor.py
│       ├── social_sentinel.py
│       └── ...
├── tests/                 # Pruebas Automatizadas
├── .github/workflows/     # Pipeline CI/CD
├── Dockerfile             # Contenedorización
└── docker-compose.yml     # Orquestación Local
```

### Pipeline CI/CD
El proyecto incluye un pipeline de GitHub Actions que ejecuta automáticamente:
1.  **Linting**: Verificación de estilo de código (flake8).
2.  **Seguridad**: Análisis estático de vulnerabilidades (bandit).
3.  **Pruebas**: Ejecución de pruebas unitarias (pytest).

## 🛠️ Instalación y Ejecución

### Opción A: Docker (Recomendado)
1.  **Construir y Correr**:
    ```bash
    docker-compose up --build
    ```
2.  **Acceso**: `http://localhost:8501`

### Opción B: Manual
1.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Ejecutar**:
    ```bash
    streamlit run app.py
    ```

## 🔐 Seguridad
Este sistema está clasificado para **SOLO OJOS AUTORIZADOS**. El acceso a los módulos de inteligencia y datos de votantes debe ser restringido.

---
*Tayllerand OS - "La política es el arte de lo posible."*
