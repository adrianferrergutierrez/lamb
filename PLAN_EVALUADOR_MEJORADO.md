# Plan de Mejora del Evaluador - Evaluación con Claude Code y AAC

**Proyecto:** Implementar un sistema de evaluación automática de trabajos estudiantiles usando rúbricas.  
**Enfoque:** Iterar con Claude Code → Validar → Migrar a AAC  
**Fecha:** April 2026

---

## 📋 TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Análisis de Estado Actual](#análisis-de-estado-actual)
3. [Visión del Nuevo Sistema](#visión-del-nuevo-sistema)
4. [Arquitectura Propuesta](#arquitectura-propuesta)
5. [Plan de Fases](#plan-de-fases)
6. [Especificaciones Detalladas](#especificaciones-detalladas)
7. [Criterios de Éxito](#criterios-de-éxito)
8. [Roadmap y Timeline](#roadmap-y-timeline)

---

## 1. Resumen Ejecutivo

### Objetivo Principal
Extender LAMB con un **sistema de evaluación automática de trabajos estudiantiles** que use rúbricas predefinidas para generar puntuaciones y retroalimentación mediante LLM. El desarrollo será **iterativo con Claude Code como agente de prueba**, validando el proceso completo antes de migración a AAC.

### Propuesta

1. ✅ **Usar Claude Code como agente** — Yo ejecuto el proceso completo del evaluador
2. ✅ **Crear `evaluator-cli`** — Herramienta CLI para automatizar la evaluación
3. ✅ **Aplicar mismos juegos de prueba** — Validar con datos reales que ya tienen
4. ✅ **Crear prompts y skills** — Definir cómo evaluar, qué mejorar
5. ✅ **Proponer mejoras** — Yo mismo valido y sugiero optimizaciones
6. ✅ **Portarlo a AAC** — Una vez validado, tu sistema AAC lo ejecuta

### Beneficios
- **Validación sin riesgo** — Pruebas exhaustivas antes de producción
- **Automatización de evaluación** — Reducir carga manual de docentes
- **Consistencia** — Rúbricas aplicadas uniformemente
- **Escalabilidad** — Evaluar muchos trabajos en paralelo
- **Trazabilidad** — Registro completo de decisiones de evaluación

---

## 2. Análisis de Estado Actual

### 2.1 ¿Qué ya existe?

✅ **Evaluaitor (Gestor de Rúbricas)**
- Ubicación: `/backend/lamb/evaluaitor/`
- Estado: Phase 1 (MVP) completo
- Características:
  - Crear/leer/actualizar/eliminar rúbricas
  - Exportar a JSON y Markdown
  - Interfaz web para editar rúbricas
  - Asistente de IA para generar rúbricas
  - Rúbricas privadas/públicas por organización

✅ **Estructura de Rúbrica**
```json
{
  "rubricId": "uuid",
  "title": "Nombre de la rúbrica",
  "criteria": [
    {
      "id": "criterion-1",
      "name": "Criterio 1",
      "weight": 30,
      "levels": [
        {
          "id": "level-1-1",
          "score": 4,
          "label": "Exemplar",
          "description": "..."
        }
      ]
    }
  ],
  "scoringType": "points",
  "maxScore": 10
}
```

### 2.2 ¿Qué NO existe?

❌ **Sistema de Evaluación de Trabajos**
- No hay proceso para evaluar trabajos estudiantiles
- No hay formato estándar para "trabajos" (submissions)
- No hay pipeline de evaluación LLM → puntuación
- No hay `evaluator-cli`
- No hay juegos de prueba integrados

❌ **Integración con AAC**
- AAC no puede ejecutar evaluaciones aún
- No hay API entre LAMB y AAC para este proceso
- No hay shared prompts/skills

### 2.3 Dependencias Existentes

- **Backend FastAPI**: `/backend` (puerto 9099) ✅
- **LLM providers**: OpenAI, Anthropic, Ollama (ya configurados) ✅
- **Base de datos LAMB**: SQLite WAL (`lamb_v4.db`) ✅
- **Frontend Svelte**: `/frontend/svelte-app` ✅

---

## 3. Visión del Nuevo Sistema

### 3.1 Flujo Completo Propuesto

```
┌─────────────────────────────────────────────────────────────────┐
│                   Proceso de Evaluación                         │
└─────────────────────────────────────────────────────────────────┘

1. ENTRADA
   ├─ Rúbrica (JSON)
   ├─ Trabajo Estudiantil (texto/documento)
   ├─ Criterios de Evaluación
   └─ Contexto (curso, estudiante, etc.)

2. PREPARACIÓN
   ├─ Validar rúbrica
   ├─ Validar formato de trabajo
   ├─ Generar contexto de evaluación
   └─ Seleccionar LLM

3. EVALUACIÓN (LLM)
   ├─ Enviar prompt estructurado al LLM
   ├─ LLM analiza trabajo contra cada criterio
   ├─ LLM selecciona nivel de rendimiento
   ├─ LLM justifica decisión
   └─ LLM calcula puntuación final

4. POST-PROCESAMIENTO
   ├─ Parsear respuesta LLM
   ├─ Validar puntuaciones
   ├─ Calcular estadísticas
   ├─ Generar retroalimentación
   └─ Guardar resultado en BD

5. SALIDA
   ├─ Puntuaciones por criterio
   ├─ Justificaciones detalladas
   ├─ Puntuación total
   ├─ Retroalimentación constructiva
   └─ Metadatos (modelo usado, timestamp, etc.)
```

### 3.2 Casos de Uso

**UC-1: Evaluación Manual (Docente)**
- El docente selecciona un trabajo estudiantil
- Click en "Evaluar con IA"
- Sistema genera evaluación en 10-30 seg
- Docente revisa y aprueba/rechaza
- Evaluación se guarda

**UC-2: Evaluación Batch (Administrador)**
- Admin sube 100+ trabajos en ZIP
- Selecciona rúbrica
- Sistema evalúa todos en paralelo
- Genera reporte CSV/JSON
- Admin revisa estadísticas

**UC-3: Evaluación Automática (AAC)**
- Estudiante entrega trabajo en el LMS
- AAC recibe webhook
- AAC ejecuta `evaluator-cli` con rúbrica
- AAC obtiene resultado
- AAC devuelve calificación al LMS

---

## 4. Arquitectura Propuesta

### 4.1 Componentes Nuevos

```
lamb/
├── backend/
│   ├── lamb/
│   │   ├── evaluaitor/          [EXISTENTE - Gestor de rúbricas]
│   │   │   ├── rubric_service.py
│   │   │   ├── rubric_database.py
│   │   │   ├── ai_generator.py
│   │   │   └── prompts/
│   │   │
│   │   └── evaluator/           [NUEVO - Evaluador de trabajos]
│   │       ├── __init__.py
│   │       ├── submission_service.py    # Procesa trabajos
│   │       ├── evaluation_engine.py     # Orquesta evaluación
│   │       ├── evaluation_prompts.py    # Prompts para evaluar
│   │       ├── result_formatter.py      # Formatea resultados
│   │       └── evaluation_database.py   # Guarda resultados
│   │
│   └── creator_interface/
│       └── routers/
│           └── evaluations.py    [NUEVO - Endpoints REST]
│
├── lamb-cli/
│   └── src/lamb_cli/
│       └── commands/
│           └── evaluator.py      [NUEVO - CLI commands]
│
└── testing/
    └── evaluator/               [NUEVO - Test cases]
        ├── sample_rubrics/
        ├── sample_submissions/
        ├── test_suite.py
        └── expected_outputs/
```

### 4.2 Flujo de Datos

```
Estudiante → LMS → AAC (webhook)
                    ↓
                [evaluator-cli]
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
  Rúbrica      Trabajo       Config LLM
    ↓               ↓               ↓
    └───────────────┼───────────────┘
                    ↓
            [Evaluation Engine]
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
  Validation   LLM Call        Parsing
    ↓               ↓               ↓
    └───────────────┼───────────────┘
                    ↓
            [Result Formatter]
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
  Scores     Feedback           JSON
    ↓               ↓               ↓
    └───────────────┼───────────────┘
                    ↓
            [BD + Webhook]
                    ↓
                LMS Grade
```

### 4.3 Entidades de BD

**Tabla: `submissions` (nuevas columnas o tabla separada)**
```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    rubric_id TEXT NOT NULL,
    student_id TEXT,
    work_text TEXT,
    work_url TEXT,  -- para archivos externos
    created_at TIMESTAMP,
    submitted_at TIMESTAMP,
    organization_id INTEGER,
    FOREIGN KEY (rubric_id) REFERENCES rubrics(rubric_id)
);

CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY,
    submission_id INTEGER,
    rubric_id TEXT,
    model_used TEXT,  -- "claude-3-opus", "gpt-4", etc.
    total_score FLOAT,
    max_score FLOAT,
    percentage_score FLOAT,
    criterion_scores JSON,  -- { "criterion-1": 4, ... }
    justifications JSON,    -- { "criterion-1": "..." }
    feedback TEXT,
    metadata JSON,          -- { "tokens_used": 1234, "latency_ms": 2300 }
    created_at TIMESTAMP,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);
```

---

## 5. Plan de Fases

### FASE 1: Implementación Base (Semanas 1-2)

**Objetivo:** Crear estructura mínima funcional con Claude Code como agente.

#### Sprint 1.1: Backend Core (Semana 1)
- [ ] Crear módulo `evaluator/` en backend
- [ ] Implementar `submission_service.py` — parseo y validación de trabajos
- [ ] Implementar `evaluation_engine.py` — lógica principal
- [ ] Implementar `evaluation_prompts.py` — generar prompts para LLM
- [ ] Implementar `result_formatter.py` — parsear respuesta LLM
- [ ] Crear tabla de BD para almacenar evaluaciones

**Deliverables:**
- ✅ Módulo evaluator completamente funcional
- ✅ Pruebas unitarias (90%+ cobertura)
- ✅ Documentación de API interna

#### Sprint 1.2: CLI (Semana 1-2)
- [ ] Crear `lamb-cli/commands/evaluator.py`
- [ ] Implementar comando: `lamb evaluator evaluate --rubric <id> --submission <file>`
- [ ] Implementar salida: JSON, CSV, YAML
- [ ] Agregar flags: `--model`, `--verbose`, `--save-to-db`
- [ ] Validar con juegos de prueba iniciales

**Deliverables:**
- ✅ CLI completamente funcional
- ✅ Manual de uso (`lamb evaluator --help`)
- ✅ Ejemplos de salida

### FASE 2: Validación con Claude Code (Semanas 2-3)

**Objetivo:** Yo ejecuto evaluaciones con tus juegos de prueba; propongo mejoras.

#### Sprint 2.1: Juegos de Prueba
- [ ] **Recopilar juegos de prueba** del profesor:
  - [ ] Rúbricas de ejemplo (al menos 3-5)
  - [ ] Trabajos estudiantiles (10-15 ejemplos)
  - [ ] Evaluaciones "esperadas" (puntuaciones de referencia)
  - [ ] Contexto (materia, nivel, etc.)

- [ ] **Crear suite de tests**:
  ```
  testing/evaluator/
  ├── rubrics/
  │   ├── rubric_essay.json
  │   ├── rubric_code.json
  │   └── rubric_presentation.json
  ├── submissions/
  │   ├── essay_student_1.txt
  │   ├── code_student_2.py
  │   └── ...
  ├── expected_outputs/
  │   ├── essay_student_1_expected.json
  │   └── ...
  └── test_evaluations.py
  ```

**Deliverables:**
- ✅ Test suite completo
- ✅ Baseline de puntuaciones conocidas

#### Sprint 2.2: Ejecuciones y Análisis (Claude Code)
- [ ] Ejecutar evaluaciones para TODOS los juegos de prueba
- [ ] Comparar resultados vs. esperados
- [ ] Identificar discrepancias:
  - ¿El LLM subestima/sobrestima?
  - ¿Falta contexto en el prompt?
  - ¿Justificaciones confusas?
  - ¿Outliers en puntuaciones?

**Mi análisis incluirá:**
- Matriz de confusión (predicho vs. real)
- Precisión por criterio
- Análisis de errores
- Recomendaciones de mejora

**Deliverables:**
- ✅ Reporte de validación (Markdown)
- ✅ Logs de todas las ejecuciones
- ✅ Análisis estadístico

#### Sprint 2.3: Iteración de Mejoras (Claude Code + Tú)
- [ ] Basado en análisis, mejorar:
  - [ ] Prompts de evaluación (más contexto, ejemplos)
  - [ ] Parsing de resultados (mejor robustez)
  - [ ] Validación de puntuaciones
  - [ ] Generación de feedback

- [ ] Re-ejecutar suite de tests
- [ ] Medir mejora: +% precisión

**Criterio de éxito:** ≥ 85% de evaluaciones dentro del rango esperado

**Deliverables:**
- ✅ Prompts mejorados
- ✅ Segundo reporte de validación
- ✅ Código refactorizado

### FASE 3: Integración con API REST (Semana 3)

**Objetivo:** API HTTP para que frontend/AAC ejecute evaluaciones.

- [ ] Crear endpoints en `creator_interface/routers/evaluations.py`:
  - `POST /creator/evaluations/evaluate` — evaluar un trabajo
  - `GET /creator/evaluations/{id}` — obtener resultado
  - `GET /creator/evaluations/submission/{submission_id}` — historial

- [ ] Middleware de autenticación/autorización
- [ ] Rate limiting
- [ ] Validación de entrada
- [ ] Error handling robusto

**Deliverables:**
- ✅ Endpoints fully tested
- ✅ OpenAPI spec auto-generada
- ✅ Postman collection de ejemplos

### FASE 4: Frontend (Semana 3-4)

**Objetivo:** UI para docentes.

- [ ] Componente: Upload de trabajo
- [ ] Componente: Seleccionar rúbrica
- [ ] Componente: Mostrar evaluación (tabla con puntuaciones + feedback)
- [ ] Componente: Historial de evaluaciones
- [ ] Integrar con store de Svelte

**Deliverables:**
- ✅ UI completamente funcional
- ✅ E2E tests (Playwright)

### FASE 5: AAC Integration (Semana 4-5)

**Objetivo:** AAC puede ejecutar evaluaciones.

- [ ] Documentar API para AAC
- [ ] Crear shared lib con prompts/skills
- [ ] Pruebas de integración E2E
- [ ] Documentación de webhook

**Deliverables:**
- ✅ AAC puede llamar API
- ✅ Webhook funcionando
- ✅ Documentación

### FASE 6: Producción (Semana 5-6)

- [ ] Performance testing
- [ ] Security audit
- [ ] Deployment a staging/prod
- [ ] Capacitación de docentes
- [ ] Soporte post-lanzamiento

---

## 6. Especificaciones Detalladas

### 6.1 Formato de Entrada (Submission)

**Opción A: JSON**
```json
{
  "submission_id": "sub_12345",
  "student_id": "student_67890",
  "rubric_id": "rubric_essay_01",
  "work": {
    "type": "text",  // "text", "url", "pdf", "code"
    "content": "El texto del trabajo estudiantil...",
    "metadata": {
      "title": "Ensayo sobre Cambio Climático",
      "language": "es",
      "word_count": 1200
    }
  },
  "context": {
    "course": "Historia Contemporánea",
    "grade_level": "10",
    "assignment": "Análisis crítico de movimientos sociales",
    "deadline": "2026-04-22"
  }
}
```

**Opción B: CLI**
```bash
lamb evaluator evaluate \
  --rubric rubric_essay_01 \
  --submission submission_12345.json \
  --model claude-3-opus \
  --output-format json \
  --save-to-db
```

### 6.2 Prompt de Evaluación (Ejemplar)

```markdown
# Evaluación de Trabajo Estudiantil

Eres un experto educativo evaluando un trabajo de estudiante usando una rúbrica específica.

## Rúbrica
[RUBRIC_JSON]

## Trabajo del Estudiante
Título: [TITLE]
Contenido:
---
[WORK_CONTENT]
---

## Tarea
Para CADA criterio en la rúbrica:
1. Lee la descripción del criterio
2. Lee las descripciones de cada nivel
3. Analiza el trabajo contra el criterio
4. Selecciona el nivel que mejor describe el trabajo
5. Justifica tu decisión (2-3 oraciones)

## Formato de Salida
Responde con JSON válido ÚNICAMENTE (sin markdown):

```json
{
  "criterion_evaluations": [
    {
      "criterion_id": "criterion-1",
      "criterion_name": "Contenido",
      "selected_level_id": "level-1-1",
      "selected_level_label": "Ejemplar",
      "score": 4,
      "justification": "El contenido demuestra..."
    }
  ],
  "score_calculation": {
    "criterion_contributions": [
      {
        "criterion_name": "Contenido",
        "criterion_score": 4,
        "criterion_weight": 40,
        "contribution": 1.6
      }
    ],
    "total_weighted": 8.5,
    "scaling_factor": 1.0,
    "total_score": 8.5
  },
  "total_score": 8.5,
  "max_score": 10,
  "percentage": 85,
  "overall_feedback": "El trabajo demuestra..."
}
```

## Requisitos Importantes
- Sé justo y objetivo
- Basa decisiones en el contenido, no en factores externos
- Justificaciones deben ser constructivas
- Si una sección es ambigua, elige el nivel más bajo de evidencia
```

### 6.3 Formato de Salida (Resultado)

```json
{
  "evaluation_id": "eval_987654",
  "submission_id": "sub_12345",
  "rubric_id": "rubric_essay_01",
  "evaluation_status": "completed",
  "timestamp": "2026-04-22T14:30:00Z",
  
  "criterion_evaluations": [
    {
      "criterion_id": "criterion-1",
      "criterion_name": "Contenido",
      "selected_level": {
        "id": "level-1-1",
        "label": "Ejemplar",
        "score": 4
      },
      "justification": "El trabajo demuestra conocimiento profundo...",
      "confidence": 0.92
    },
    {
      "criterion_id": "criterion-2",
      "criterion_name": "Organización",
      "selected_level": {
        "id": "level-2-2",
        "label": "Proficient",
        "score": 3
      },
      "justification": "La estructura es clara pero con algunas transiciones débiles...",
      "confidence": 0.85
    }
  ],
  
  "score_calculation": {
    "components": [
      {
        "criterion": "Contenido",
        "score": 4,
        "weight": 40,
        "contribution": 1.6
      },
      {
        "criterion": "Organización",
        "score": 3,
        "weight": 30,
        "contribution": 0.9
      },
      {
        "criterion": "Ortografía",
        "score": 4,
        "weight": 30,
        "contribution": 1.2
      }
    ],
    "total_weighted_sum": 3.7,
    "max_weighted_sum": 4.3,
    "scaling_factor": 2.33,
    "final_score": 8.6
  },
  
  "total_score": 8.6,
  "max_score": 10,
  "percentage_score": 86,
  "letter_grade": "A",  // Opcional
  
  "overall_feedback": "Excelente ensayo que demuestra comprensión profunda del tema...",
  
  "model_used": "claude-3-opus",
  "tokens_used": {
    "input": 2450,
    "output": 890
  },
  "evaluation_time_ms": 3200,
  
  "metadata": {
    "rubric_version": "1.0",
    "submission_word_count": 1200,
    "language_detected": "es"
  }
}
```

---

## 7. Criterios de Éxito

### Métrica 1: Exactitud
- ✅ ≥ 85% de evaluaciones dentro del ±1 punto del rango esperado
- ✅ ≥ 90% de criterios clasificados correctamente

### Métrica 2: Confiabilidad
- ✅ Reproducibilidad: misma entrada → mismo resultado (mismo modelo)
- ✅ Consistencia: puntuaciones uniformes entre trabajos similares
- ✅ Disponibilidad: 99% uptime en API

### Métrica 3: Usabilidad
- ✅ Evaluación completa en < 30 segundos (promedio)
- ✅ UI comprensible sin capacitación
- ✅ ≥ 95% de resultados sin error

### Métrica 4: Validación
- ✅ Suite de tests: 100% pasando
- ✅ Coverage de código: ≥ 85%
- ✅ Juegos de prueba: todos pasos

---

## 8. Roadmap y Timeline

### Timeline Estimado: 5-6 Semanas

```
Semana 1 (Apr 22-26):
  ├─ Mar: Recopilar juegos de prueba
  ├─ Mié: Backend core (evaluator module)
  ├─ Jue: Primeras pruebas unitarias
  ├─ Vie: Integración inicial
  └─ Sáb: Primera iteración completa

Semana 2 (Apr 29-May 3):
  ├─ Lun-Mar: CLI completamente funcional
  ├─ Mié: Suite de tests establecida
  ├─ Jue: Claude Code ejecuta validación
  └─ Vie: Primer reporte de análisis

Semana 3 (May 6-10):
  ├─ Lun-Mar: Mejoras basadas en validación
  ├─ Mié: API REST endpoints
  ├─ Jue-Vie: Frontend básico
  └─ Fin: Segundo reporte validación (≥85%)

Semana 4 (May 13-17):
  ├─ Lun-Mié: Frontend refinado + E2E tests
  ├─ Jue-Vie: Integración AAC
  └─ Fin: Pruebas de integración

Semana 5 (May 20-24):
  ├─ Lun-Mar: Performance testing
  ├─ Mié: Seguridad + audit
  └─ Jue-Vie: Deployment staging

Semana 6 (May 27-31):
  ├─ Lun-Mar: Pruebas en staging
  ├─ Mié: Documentación final
  ├─ Jue: Capacitación docentes
  └─ Vie: Go-live a producción
```

---

## 9. Recursos Necesarios

### Equipo
- **Tú**: Definir requerimientos, validar resultados
- **Claude Code (Yo)**: Desarrollo, validación iterativa, análisis
- **Profesor**: Proporcionar feedback, juegos de prueba, contexto educativo
- **AAC**: Futuro consumidor de API

### Herramientas
- ✅ FastAPI backend (ya existe)
- ✅ SQLite BD (ya existe)
- ✅ LLM providers (OpenAI, Anthropic, Ollama - ya configurados)
- ✅ Svelte frontend (ya existe)
- ✅ pytest para tests (ya existe)
- ✅ GitHub Actions para CI/CD (ya existe)

### Datos
- ❓ Juegos de prueba (necesita proporcionar profesor)
- ❓ Rúbricas de ejemplo (al menos 3-5)
- ❓ Trabajos estudiantiles de prueba (10-15)
- ❓ Puntuaciones esperadas de referencia

---

## 10. Preguntas Abiertas para Aclarar

1. **¿Qué tipos de trabajos evaluar?**
   - Solo texto (ensayos)?
   - También código, presentaciones, multimedia?
   - ¿Cómo manejar archivos adjuntos grandes?

2. **¿Qué LLM usar por defecto?**
   - Claude 3 Opus (buena calidad, más costoso)
   - GPT-4 (OpenAI)
   - Modelo local (Ollama)

3. **¿Evaluación en tiempo real o batch?**
   - Ambos: API HTTP para tiempo real + CLI para batch?

4. **¿Integración con Moodle/LMS?**
   - Solo webhook básico?
   - LTI completo?
   - Ambos?

5. **¿Almacenar todas las evaluaciones?**
   - Sí (para análisis histórico)
   - Solo las "finales"?

6. **¿Permitir revisión docente?**
   - Docente revisa antes de guardar?
   - Docente puede modificar puntuaciones?

---

## 11. Próximos Pasos

### Inmediatos (Hoy-Mañana)
1. ✅ Revisar y validar este plan contigo
2. ✅ Recopilar juegos de prueba ya existentes
3. ✅ Responder preguntas abiertas (sección 10)
4. ✅ Crear backlog detallado de tareas

### Semana 1
1. Comenzar Sprint 1.1 (Backend core)
2. Crear estructura de módulos
3. Primeras pruebas unitarias

### Semana 2
1. CLI completamente funcional
2. Suite de tests con juegos de prueba
3. Yo ejecuto validación como Claude Code

---

**Documento creado:** 22 de abril de 2026  
**Versión:** 1.0  
**Estado:** 🟡 BORRADOR - Pendiente tu revisión y feedback
