# Documentación del Proyecto:

## Descripción General

Este proyecto tiene como objetivo desarrollar una herramienta de extracción de características para documentos médicos e invoices. Utiliza procesamiento de lenguaje natural (NLP) para analizar textos de PDFs y extraer datos estructurados.

---

## Instrucciones de Uso

1. **Recrear el entorno con Conda:**
   - Crea un nuevo entorno con Conda para asegurar que todas las dependencias necesarias estén instaladas:
     ```bash
     conda create --name structured-extraction python=3.x
     ```
     (Reemplaza `3.x` por la versión de Python que prefieras).

   - Activa el entorno:ˆ`
     ```bash
     conda activate structured-extraction
     ```

2. **Instalar las dependencias:**
   - Instala las dependencias necesarias usando `pip` (dentro del entorno conda):
     ```bash
     pip install -r requirements.txt
     ```

3. **Configurar las API Keys:**
   - Asegúrate de tener las API keys necesarias configuradas. Este proyecto requiere claves para usar los modelos de OpenAI.
   - Crea un archivo `.env` en la raíz del proyecto y agrega las claves de la siguiente manera:
     ```bash
     OPENAI_API_KEY=tu_clave_de_api_aqui
     ```

4. **Ejecutar el script:**
   - Una vez configurado el entorno y las claves, ejecuta el script para procesar los PDFs:
     ```bash
     python extractors/medical_features_extractor.py /data/medical-studies
     ```

---

## Estructura del Proyecto

```plaintext
entregable-2/
│
├── extractors/              # Código fuente de los extractores
│   ├── medical_features_extractor.py
│   ├── invoice_extractor.py
├── data/              # Datos de ejemplo
│
├── notebooks/
│   ├── extractor.ipynb ## Notebook Entregable
```

---

## Módulos Principales

- **medical_features_extractor.py**
  - Extrae datos estructurados de investigaciones médicas.
  - Utiliza GPT-4o para analizar y extraer detalles como tipo de intervención, objetivos y eventos adversos.

- **invoice_extractor.py**
  - Extrae detalles de invoices, incluyendo ID, fecha y artículos.
  - Utiliza GPT-4o para obtener los datos estructurados.

---

## Funciones Clave

- **extract_text(file_path)**
  - Extrae texto de un archivo PDF.
  
- **extract_values_from_file(raw_file_data)**
  - Extrae información estructurada usando GPT-4o.

- **process_pdf_files(file_list)**
  - Procesa una lista de archivos PDF y genera un archivo JSON con los datos extraídos.

---

## Modelos de Datos (Pydantic)

- **StudyData** (medical_features_extractor.py)
  - Modela los datos de un estudio clínico: tipo de intervención, participantes, objetivos.

- **Invoice** (invoice_extractor.py)
  - Modela los datos de una invoice: ID, fecha y artículos.

---

## Salida

El script genera archivos JSON con los datos extraídos de los PDFs. Este formato es adecuado para análisis posterior o integración con otros sistemas.

---

## Mejoras Futuras

Se pueden agregar mejoras como el soporte para otros tipos de documentos y una mejor gestión de errores en documentos inconsistentes.

---

## Referencias

1. [Introduction to Structured Data Extraction](https://docs.llamaindex.ai/en/stable/understanding/extraction/)
2. [Extracting Structured JSON from Credit Card Statements with Langchain and Pydantic](https://github.com/Zipstack/structured-extraction/tree/main?tab=readme-ov-file)