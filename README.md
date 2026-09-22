# Predicción de retrasos de vuelos — NYC 2013

Proyecto final del curso de Machine Learning. Predice si un vuelo que sale de
Nueva York llegará con **15+ minutos de retraso**, usando solo información
disponible **antes del despegue**.

Ver [`proposal.md`](proposal.md) para el planteamiento completo del problema
(pregunta predictiva, variable objetivo, riesgos de leakage, métricas, plan
de validación, baseline y plan de trabajo).

## Dataset

[`nycflights13`](https://pypi.org/project/nycflights13/): 336,776 vuelos que
salieron de JFK, LGA y EWR en 2013, con clima horario, aeronaves, aerolíneas
y aeropuertos de destino. Se instala como paquete de Python — **no requiere
descargas manuales, cuentas ni credenciales**.

## Estructura del repositorio

```
proyecto-final/
├── README.md                          <- este archivo
├── proposal.md                        <- entrega previa (13 secciones)
├── requirements.txt
├── notebooks/
│   └── 01_exploracion_inicial.ipynb   <- carga, EDA, leakage, baseline (ejecutado)
├── src/
│   └── data.py                        <- carga y unión reproducible de las 5 tablas
├── reports/
│   └── figures/                       <- las 7 figuras generadas en el EDA (PNG)
└── outputs/
    └── metrics.json                   <- métricas del baseline (val + test)
```

## Cómo reproducir la exploración

```bash
# 1. Crear entorno y dependencias
python -m venv venv
source venv/bin/activate            # en Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Levantar Jupyter y correr el notebook de exploración
jupyter notebook notebooks/01_exploracion_inicial.ipynb
# Kernel > Restart & Run All
```

O, para regenerar solo los datos unidos desde la línea de comandos:

```bash
python src/data.py
# Imprime shape final y balance del target
```

No se necesita ninguna variable de entorno, API key, ni descarga manual: al
correr `import nycflights13`, el propio paquete de pip trae los datos.

## Semilla aleatoria

Todos los modelos usan `random_state=42` para reproducibilidad.

## Notas de reproducibilidad

- Python 3.12.
- El split de entrenamiento/validación/test es **temporal** (no aleatorio):
  enero–octubre / noviembre / diciembre de 2013 — ver sección 10 de
  `proposal.md` para la justificación.
