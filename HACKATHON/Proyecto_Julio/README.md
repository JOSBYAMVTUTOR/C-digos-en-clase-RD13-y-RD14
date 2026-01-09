# Proyecto de Deteccion de Fraude con Machine Learning

Proyecto para deteccion de fraude usando multiples enfoques:
- Modelo supervisado con LightGBM
- Modelo no supervisado con Autoencoder
- Soporte opcional para texto con BERT
- Explicabilidad del modelo con SHAP

---

## Dataset

### Credit Card Fraud Detection

- Archivo: `creditcard.csv`
- Columna objetivo: `Class`
  - 0 = transaccion normal
  - 1 = fraude
---

## Modelos usados

- LightGBM (clasificacion supervisada)
- Autoencoder (deteccion de anomalias)
- BERT (opcional, solo si hay columna de texto)

---

## Librerias

- pandas
- numpy
- scikit-learn
- lightgbm
- torch
- tf-keras
- transformers
- shap

Instalacion:

```bash
pip install pandas numpy scikit-learn lightgbm torch transformers tf-keras shap
