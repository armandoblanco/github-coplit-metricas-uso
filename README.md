# 📊 GitHub Copilot Usage Metrics Report Generator

Generador de reportes de métricas de uso de GitHub Copilot para organizaciones y empresas.

## � Autor

Soy Armando Blanco un **Solution Engineer en Microsoft LATAM** para facilitar el acceso a métricas de Copilot en escenarios donde:

- 🔒 No tienes acceso a las métricas a nivel de **Enterprise**
- 🎯 Solo necesitas ver los datos de una **organización específica** dentro de tu Enterprise
- 📊 Quieres exportar las métricas a formatos como **Excel o CSV** para análisis personalizado
- 🔄 Necesitas automatizar la recolección de métricas de forma programática

## 📋 Descripción

Este proyecto te permite obtener métricas de uso de GitHub Copilot de tu organización utilizando la API REST de GitHub. Genera reportes en múltiples formatos (JSON, CSV, Excel) que puedes usar para análisis y seguimiento del uso de Copilot.

> ⚠️ **Nota**: En este README se usa `armblaorg` como nombre de organización de ejemplo. **Deberás reemplazarlo por el nombre real de tu organización** en todos los comandos y configuraciones.

### Características

- ✅ Métricas agregadas de organización (28 días o día específico)
- ✅ Métricas detalladas por usuario
- ✅ **Usage Breakdown** - Vista de uso por usuario estilo GitHub UI
- ✅ Lista de usuarios con seats de Copilot asignados
- ✅ Soporte para GitHub Enterprise Cloud
- ✅ Múltiples formatos de salida: JSON, CSV, Excel
- ✅ Variables de entorno para configuración segura
- ✅ Fácilmente replicable

## 🔧 Requisitos Previos

### 1. Python 3.8 o superior

```bash
python --version
```

### 2. GitHub Copilot habilitado en tu organización

Tu organización debe tener:
- Una suscripción activa a GitHub Copilot Business o Enterprise
- La política "Copilot usage metrics" habilitada en la configuración de la empresa/organización

### 3. Token de Acceso Personal (PAT) de GitHub

Crear un **Fine-grained personal access token** con los permisos necesarios:

#### Paso a paso:

1. Ve a [GitHub Settings > Developer settings > Fine-grained tokens](https://github.com/settings/personal-access-tokens/new)

2. **Token name**: `copilot-metrics-reader` (o el nombre que prefieras)

3. **Expiration**: Selecciona la duración deseada (ej: 366 days / 1 año)

4. **Resource owner**: Selecciona tu organización
   
   > 📝 **Ejemplo**: En este README usamos `armblaorg` como ejemplo. **Selecciona el nombre real de tu organización**.
   
   > ⚠️ **Si no ves tu organización**: Ve a Settings de la organización → Third-party access → Personal access tokens → Habilita "Allow access via fine-grained personal access tokens"

5. **Repository access**: Selecciona `Public repositories`
   
   > No se necesita acceso a repositorios privados para las métricas de Copilot

6. **Organization permissions** - Haz clic en **"Add permissions"** y agrega los siguientes permisos:

   ```
   ┌─────────────────────────────────────────────────────────────┐
   │ Organizations  2                          [Add permissions] │
   ├─────────────────────────────────────────────────────────────┤
   │                                                             │
   │ GitHub Copilot Business                                     │
   │ Manage Copilot Business seats and settings.                 │
   │                                      Access: Read-only  ✓   │
   │                                                             │
   │ Organization Copilot metrics                                │
   │ View organization Copilot metrics.                          │
   │                                      Access: Read-only  ✓   │
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
   ```

   | Permiso | Nivel | ¿Para qué se usa? |
   |---------|-------|-------------------|
   | **GitHub Copilot Business** | Read-only | Ver lista de usuarios con seats de Copilot asignados (`--seats`, `--breakdown`) |
   | **Organization Copilot metrics** | Read-only | Ver métricas de uso de Copilot (requests, interacciones, código generado) |

7. Scroll hacia abajo y haz clic en **"Generate token"**

8. **¡COPIA EL TOKEN INMEDIATAMENTE!** 
   
   > ⚠️ Solo lo verás una vez. Si lo pierdes, tendrás que generar uno nuevo.

   El token tendrá un formato como: `github_pat_xxxxxxxxxxxxxxxxx`

#### Alternativa: Token Clásico

Si prefieres usar un token clásico (menos recomendado):
1. Ve a [GitHub Settings > Developer settings > Tokens (classic)](https://github.com/settings/tokens/new)
2. Scope requerido: `read:org`

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/armblaorg/usage-metrics.git
cd usage-metrics
```

### 2. Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus valores
# Windows
notepad .env

# macOS/Linux
nano .env
```

Configurar las siguientes variables en `.env`:

```env
GITHUB_TOKEN=ghp_tu_token_aqui
GITHUB_ORG=armblaorg
OUTPUT_DIR=./reports
OUTPUT_FORMAT=json
```

## 📖 Uso

### Uso básico - Reporte de 28 días

```bash
python copilot_metrics.py
```

### Reporte de un día específico

```bash
python copilot_metrics.py --day 2026-01-15
```

### Incluir métricas por usuario

```bash
python copilot_metrics.py --users
```

### Ver lista de usuarios con Copilot (seats)

```bash
python copilot_metrics.py --seats
```

### 📊 Usage Breakdown (estilo GitHub UI)

Muestra una tabla con el uso de cada usuario, similar a la vista de GitHub:

```bash
python copilot_metrics.py --breakdown
```

Ejemplo de salida:
```
📊 USAGE BREAKDOWN
   Período: 2026-01-01 a 2026-01-28 | Precio por premium request: $0.04

User                   Interactions    Code Gen     Included req       Editor
----------------------------------------------------------------------------------
🟢 armbla_abdemo        77              354          431/1,000          GitHubCopilotChat
   ████████░░░░░░░░░░░░ 43.1%
🟢 admin_abdemo         0               0            0/1,000            github_spark

📊 RESUMEN
   👥 Total de usuarios con Copilot: 2
   💬 Total interacciones: 77
   💻 Total generación de código: 354
```

### Exportar a CSV

```bash
python copilot_metrics.py --format csv
```

### Exportar a Excel

```bash
python copilot_metrics.py --format excel
```

### Métricas de empresa (GitHub Enterprise Cloud)

```bash
# Primero configura GITHUB_ENTERPRISE en .env
python copilot_metrics.py --enterprise
```

### Combinando opciones

```bash
# Reporte de un día específico, con usuarios, en formato Excel
python copilot_metrics.py --day 2026-01-15 --users --format excel

# Especificar organización y token directamente
python copilot_metrics.py --org armblaorg --token ghp_xxx --format csv
```

### Ayuda

```bash
python copilot_metrics.py --help
```

## 📁 Estructura del Proyecto

```
usage-metrics/
├── copilot_metrics.py      # Script principal
├── requirements.txt        # Dependencias de Python
├── .env.example           # Plantilla de variables de entorno
├── .env                   # Variables de entorno (no incluido en git)
├── .gitignore             # Archivos a ignorar en git
├── README.md              # Este archivo
└── reports/               # Directorio de salida (creado automáticamente)
    ├── copilot_org_28_day_20260129_120000.json
    └── copilot_users_28_day_20260129_120000.json
```

## 📊 Datos del Reporte

### Métricas de Organización

El reporte de organización incluye métricas agregadas como:

- Estadísticas de uso de funciones de Copilot
- Datos de engagement de usuarios
- Métricas de adopción de funcionalidades
- Sugerencias aceptadas vs rechazadas
- Líneas de código sugeridas

### Métricas por Usuario

El reporte de usuarios incluye:

- Estadísticas individuales por usuario
- Patrones de uso de funcionalidades
- Métricas de adopción por usuario
- Tiempos de actividad

## 🔒 Seguridad

- **NUNCA** subas tu archivo `.env` al repositorio
- El archivo `.gitignore` ya está configurado para excluir `.env`
- Usa tokens con los mínimos permisos necesarios
- Rota tus tokens periódicamente

## 🐛 Solución de Problemas

### Error 403: Forbidden

```
❌ Error 403: No tienes permisos para acceder a este recurso.
```

**Solución**:
1. Verifica que tu token tenga el scope `read:org` (classic) o permiso `Copilot metrics` (fine-grained)
2. Verifica que seas owner o tengas permisos de admin en la organización
3. Verifica que la política "Copilot usage metrics" esté habilitada

### Error 404: Not Found

```
❌ Error 404: Recurso no encontrado.
```

**Solución**:
1. Verifica que el nombre de la organización sea correcto
2. Verifica que la organización tenga Copilot habilitado
3. Los reportes están disponibles desde octubre 2025

### Sin datos en el reporte

**Solución**:
1. Verifica que haya actividad de Copilot en tu organización
2. Los reportes se generan diariamente, puede haber un retraso de 24-48 horas

## 📚 Referencias

- [Documentación de la API de Copilot Usage Metrics](https://docs.github.com/en/enterprise-cloud@latest/rest/copilot/copilot-usage-metrics)
- [Cómo se atribuyen las métricas en organizaciones](https://docs.github.com/enterprise-cloud@latest/copilot/concepts/copilot-metrics#how-are-metrics-attributed-across-organizations)
- [Administrar políticas de Copilot en tu empresa](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-enterprise-policies)

## 📝 Licencia

MIT License - Siéntete libre de usar y modificar este proyecto.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request