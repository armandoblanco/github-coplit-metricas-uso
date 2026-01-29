#!/usr/bin/env python3
"""
GitHub Copilot Usage Metrics Report Generator

Este script obtiene métricas de uso de GitHub Copilot para una organización
utilizando la API REST de GitHub.

Autor: armblaorg
Documentación API: https://docs.github.com/en/enterprise-cloud@latest/rest/copilot/copilot-usage-metrics
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
GITHUB_API_BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"


class CopilotMetricsClient:
    """Cliente para obtener métricas de GitHub Copilot."""

    def __init__(self, token: str, org: str, enterprise: str = None):
        """
        Inicializa el cliente de métricas de Copilot.

        Args:
            token: Token de acceso personal de GitHub
            org: Nombre de la organización
            enterprise: Nombre de la empresa (opcional)
        """
        self.token = token
        self.org = org
        self.enterprise = enterprise
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
        }

    def _make_request(self, url: str, params: dict = None) -> dict:
        """
        Realiza una petición GET a la API de GitHub.

        Args:
            url: URL del endpoint
            params: Parámetros de la petición

        Returns:
            Respuesta JSON de la API
        """
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"❌ Error 403: No tienes permisos para acceder a este recurso.")
                print("   Verifica que tu token tenga los scopes necesarios:")
                print("   - Para organización: 'read:org'")
                print("   - Para empresa: 'manage_billing:copilot' o 'read:enterprise'")
            elif e.response.status_code == 404:
                print(f"❌ Error 404: Recurso no encontrado.")
                print(f"   Verifica que la organización '{self.org}' existe y tiene Copilot habilitado.")
            else:
                print(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            sys.exit(1)

    def _download_report_files(self, download_links: list) -> list:
        """
        Descarga los archivos de reporte desde los enlaces proporcionados.
        Soporta JSON y JSON Lines (NDJSON) formato.

        Args:
            download_links: Lista de URLs de descarga

        Returns:
            Lista con el contenido de todos los reportes
        """
        all_data = []
        for link in download_links:
            try:
                response = requests.get(link)
                response.raise_for_status()
                content = response.text
                
                # Intentar parsear como JSON normal primero
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)
                except json.JSONDecodeError:
                    # Si falla, intentar como JSON Lines (un JSON por línea)
                    for line in content.strip().split('\n'):
                        if line.strip():
                            try:
                                data = json.loads(line)
                                all_data.append(data)
                            except json.JSONDecodeError as e:
                                print(f"⚠️  Error parseando línea: {e}")
            except Exception as e:
                print(f"⚠️  Error descargando reporte: {e}")
        return all_data

    def get_org_metrics_28_day(self) -> dict:
        """
        Obtiene métricas de uso de Copilot de los últimos 28 días para la organización.

        Returns:
            Métricas de uso de Copilot
        """
        url = f"{GITHUB_API_BASE_URL}/orgs/{self.org}/copilot/metrics/reports/organization-28-day/latest"
        print(f"📊 Obteniendo métricas de 28 días para la organización '{self.org}'...")
        
        response = self._make_request(url)
        
        if "download_links" in response:
            print(f"📥 Descargando {len(response['download_links'])} archivo(s) de reporte...")
            report_data = self._download_report_files(response["download_links"])
            response["data"] = report_data
        
        return response

    def get_org_metrics_by_day(self, day: str) -> dict:
        """
        Obtiene métricas de uso de Copilot para un día específico.

        Args:
            day: Fecha en formato YYYY-MM-DD

        Returns:
            Métricas de uso de Copilot para el día especificado
        """
        url = f"{GITHUB_API_BASE_URL}/orgs/{self.org}/copilot/metrics/reports/organization-1-day"
        params = {"day": day}
        print(f"📊 Obteniendo métricas para el día {day}...")
        
        response = self._make_request(url, params)
        
        if "download_links" in response:
            print(f"📥 Descargando {len(response['download_links'])} archivo(s) de reporte...")
            report_data = self._download_report_files(response["download_links"])
            response["data"] = report_data
        
        return response

    def get_org_users_metrics_28_day(self) -> dict:
        """
        Obtiene métricas de uso por usuario de los últimos 28 días.

        Returns:
            Métricas de uso por usuario
        """
        url = f"{GITHUB_API_BASE_URL}/orgs/{self.org}/copilot/metrics/reports/users-28-day/latest"
        print(f"👥 Obteniendo métricas de usuarios para la organización '{self.org}'...")
        
        response = self._make_request(url)
        
        if "download_links" in response:
            print(f"📥 Descargando {len(response['download_links'])} archivo(s) de reporte...")
            report_data = self._download_report_files(response["download_links"])
            response["data"] = report_data
        
        return response

    def get_org_users_metrics_by_day(self, day: str) -> dict:
        """
        Obtiene métricas de uso por usuario para un día específico.

        Args:
            day: Fecha en formato YYYY-MM-DD

        Returns:
            Métricas de uso por usuario para el día especificado
        """
        url = f"{GITHUB_API_BASE_URL}/orgs/{self.org}/copilot/metrics/reports/users-1-day"
        params = {"day": day}
        print(f"👥 Obteniendo métricas de usuarios para el día {day}...")
        
        response = self._make_request(url, params)
        
        if "download_links" in response:
            print(f"📥 Descargando {len(response['download_links'])} archivo(s) de reporte...")
            report_data = self._download_report_files(response["download_links"])
            response["data"] = report_data
        
        return response

    def get_copilot_billing_seats(self) -> dict:
        """
        Obtiene la lista de usuarios con seats de Copilot asignados.
        Endpoint: GET /orgs/{org}/copilot/billing/seats

        Returns:
            Lista de usuarios con seats asignados
        """
        url = f"{GITHUB_API_BASE_URL}/orgs/{self.org}/copilot/billing/seats"
        print(f"👥 Obteniendo lista de usuarios con Copilot para '{self.org}'...")
        
        all_seats = []
        page = 1
        per_page = 50
        total_seats = 0
        
        while True:
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    params={"page": page, "per_page": per_page}
                )
                response.raise_for_status()
                data = response.json()
                
                if page == 1:
                    total_seats = data.get("total_seats", 0)
                
                seats = data.get("seats", [])
                all_seats.extend(seats)
                
                if len(seats) < per_page:
                    break
                page += 1
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"❌ Error 403: No tienes permisos. Verifica el scope 'GitHub Copilot Business'.")
                elif e.response.status_code == 404:
                    print(f"❌ Error 404: Copilot no está habilitado en '{self.org}'.")
                else:
                    print(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
                return None
        
        return {
            "total_seats": total_seats,
            "seats": all_seats
        }

    def get_copilot_usage_summary(self) -> dict:
        """
        Obtiene el resumen de uso de Copilot (billing summary).
        Endpoint: GET /orgs/{org}/copilot/billing

        Returns:
            Resumen de facturación de Copilot
        """
        url = f"{GITHUB_API_BASE_URL}/orgs/{self.org}/copilot/billing"
        print(f"💰 Obteniendo resumen de billing para '{self.org}'...")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"⚠️  No se pudo obtener billing summary: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"⚠️  Error obteniendo billing: {e}")
            return None

    def get_enterprise_metrics_28_day(self) -> dict:
        """
        Obtiene métricas de uso de Copilot de los últimos 28 días para la empresa.

        Returns:
            Métricas de uso de Copilot a nivel de empresa
        """
        if not self.enterprise:
            print("⚠️  No se especificó una empresa. Usa la variable GITHUB_ENTERPRISE.")
            return {}

        url = f"{GITHUB_API_BASE_URL}/enterprises/{self.enterprise}/copilot/metrics/reports/enterprise-28-day/latest"
        print(f"🏢 Obteniendo métricas de empresa '{self.enterprise}'...")
        
        response = self._make_request(url)
        
        if "download_links" in response:
            print(f"📥 Descargando {len(response['download_links'])} archivo(s) de reporte...")
            report_data = self._download_report_files(response["download_links"])
            response["data"] = report_data
        
        return response


class ReportGenerator:
    """Generador de reportes de métricas de Copilot."""

    def __init__(self, output_dir: str, output_format: str = "json"):
        """
        Inicializa el generador de reportes.

        Args:
            output_dir: Directorio de salida para los reportes
            output_format: Formato de salida (json, csv, excel)
        """
        self.output_dir = Path(output_dir)
        self.output_format = output_format.lower()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_filename(self, report_type: str) -> str:
        """
        Genera un nombre de archivo para el reporte.

        Args:
            report_type: Tipo de reporte

        Returns:
            Nombre del archivo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = self.output_format if self.output_format != "excel" else "xlsx"
        return f"copilot_{report_type}_{timestamp}.{extension}"

    def save_json(self, data: dict, filepath: Path):
        """Guarda los datos en formato JSON."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def save_csv(self, data: dict, filepath: Path):
        """Guarda los datos en formato CSV."""
        import csv

        # Extraer datos del reporte
        report_data = data.get("data", [data])
        
        if not report_data:
            print("⚠️  No hay datos para guardar en CSV")
            return

        # Si es una lista de diccionarios, usarla directamente
        if isinstance(report_data, list) and len(report_data) > 0:
            if isinstance(report_data[0], dict):
                fieldnames = list(report_data[0].keys())
                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(report_data)
            else:
                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(report_data)

    def save_excel(self, data: dict, filepath: Path):
        """Guarda los datos en formato Excel."""
        try:
            import pandas as pd
            
            report_data = data.get("data", [data])
            
            if isinstance(report_data, list):
                df = pd.DataFrame(report_data)
            else:
                df = pd.DataFrame([report_data])
            
            df.to_excel(filepath, index=False, engine="openpyxl")
        except ImportError:
            print("⚠️  Para exportar a Excel, instala: pip install pandas openpyxl")
            # Fallback a JSON
            self.save_json(data, filepath.with_suffix(".json"))

    def save_report(self, data: dict, report_type: str) -> Path:
        """
        Guarda el reporte en el formato especificado.

        Args:
            data: Datos del reporte
            report_type: Tipo de reporte

        Returns:
            Ruta del archivo guardado
        """
        filename = self.generate_filename(report_type)
        filepath = self.output_dir / filename

        if self.output_format == "json":
            self.save_json(data, filepath)
        elif self.output_format == "csv":
            self.save_csv(data, filepath)
        elif self.output_format == "excel":
            self.save_excel(data, filepath)
        else:
            print(f"⚠️  Formato no soportado: {self.output_format}. Usando JSON.")
            self.save_json(data, filepath.with_suffix(".json"))

        print(f"✅ Reporte guardado en: {filepath}")
        return filepath


def print_usage_breakdown(seats_data: dict, users_metrics: dict = None, billing_data: dict = None):
    """
    Imprime una tabla de usuarios con su uso de Copilot, similar al UI de GitHub.

    Args:
        seats_data: Datos de seats de Copilot
        users_metrics: Datos de métricas por usuario (opcional)
        billing_data: Datos de billing (opcional)
    """
    if not seats_data or "seats" not in seats_data:
        print("⚠️  No hay datos de usuarios para mostrar")
        return

    seats = seats_data.get("seats", [])
    total_seats = seats_data.get("total_seats", len(seats))
    
    # Obtener el límite de requests incluidos (1000 para Copilot Business/Enterprise)
    included_limit = 1000
    price_per_premium = 0.04
    
    # Agregar métricas por usuario si están disponibles
    user_stats = {}
    if users_metrics and "data" in users_metrics:
        for record in users_metrics.get("data", []):
            user_login = record.get("user_login", "")
            if user_login not in user_stats:
                user_stats[user_login] = {
                    "interactions": 0,
                    "code_gen": 0,
                    "code_accept": 0,
                    "loc_added": 0,
                    "loc_suggested": 0
                }
            user_stats[user_login]["interactions"] += record.get("user_initiated_interaction_count", 0)
            user_stats[user_login]["code_gen"] += record.get("code_generation_activity_count", 0)
            user_stats[user_login]["code_accept"] += record.get("code_acceptance_activity_count", 0)
    
    # Obtener período del reporte
    period_start = users_metrics.get("report_start_day", "N/A") if users_metrics else "N/A"
    period_end = users_metrics.get("report_end_day", "N/A") if users_metrics else "N/A"
    
    print("\n" + "=" * 110)
    print("📊 USAGE BREAKDOWN")
    print(f"   Período: {period_start} a {period_end} | Precio por premium request: ${price_per_premium}")
    print("=" * 110)
    
    # Header de la tabla
    print(f"\n{'User':<22} {'Interactions':<15} {'Code Gen':<12} {'Included req':<18} {'Editor':<25}")
    print("-" * 110)
    
    total_interactions = 0
    total_code_gen = 0
    
    for seat in seats:
        assignee = seat.get("assignee", {})
        login = assignee.get("login", "N/A")
        
        # Obtener métricas del usuario
        stats = user_stats.get(login, {})
        interactions = stats.get("interactions", 0)
        code_gen = stats.get("code_gen", 0)
        
        total_interactions += interactions
        total_code_gen += code_gen
        
        # Calcular uso de requests incluidos
        total_user_requests = interactions + code_gen
        included_str = f"{total_user_requests:,}/1,000"
        
        # Calcular porcentaje de uso
        usage_pct = min(100, (total_user_requests / included_limit) * 100)
        bar_width = int(usage_pct / 5)  # 20 chars = 100%
        progress_bar = "█" * bar_width + "░" * (20 - bar_width)
        
        # Último editor usado
        last_editor = seat.get("last_activity_editor", "N/A")
        if last_editor and "/" in last_editor:
            last_editor = last_editor.split("/")[1][:20]
        
        # Estado del usuario
        last_activity = seat.get("last_activity_at")
        status = "🟢" if last_activity else "⚪"
        
        # Mostrar fila
        print(f"{status} {login:<20} {interactions:<15} {code_gen:<12} {included_str:<18} {last_editor:<25}")
        
        # Mostrar barra de progreso
        if total_user_requests > 0:
            print(f"   {progress_bar} {usage_pct:.1f}%")
        
        # Mostrar si hay cancelación pendiente
        pending_cancellation = seat.get("pending_cancellation_date")
        if pending_cancellation:
            print(f"   ⚠️  Cancelación pendiente: {pending_cancellation[:10]}")
    
    print("-" * 110)
    
    # Totales
    print(f"\n📊 RESUMEN")
    print(f"   👥 Total de usuarios con Copilot: {total_seats}")
    
    active_users = sum(1 for s in seats if s.get("last_activity_at"))
    inactive_users = total_seats - active_users
    
    print(f"   🟢 Usuarios activos: {active_users}")
    print(f"   ⚪ Usuarios sin actividad reciente: {inactive_users}")
    print(f"\n   💬 Total interacciones: {total_interactions:,}")
    print(f"   💻 Total generación de código: {total_code_gen:,}")
    print("=" * 110 + "\n")


def print_seats_detail(seats_data: dict):
    """
    Imprime detalle de seats de Copilot.

    Args:
        seats_data: Datos de seats
    """
    if not seats_data or "seats" not in seats_data:
        print("⚠️  No hay datos de seats")
        return
    
    seats = seats_data.get("seats", [])
    
    print("\n" + "=" * 90)
    print("👥 DETALLE DE USUARIOS CON COPILOT")
    print("=" * 90)
    print(f"\n{'Usuario':<25} {'Asignado':<15} {'Última actividad':<20} {'Estado'}")
    print("-" * 90)
    
    for seat in seats:
        assignee = seat.get("assignee", {})
        login = assignee.get("login", "N/A")
        created = seat.get("created_at", "")[:10] if seat.get("created_at") else "N/A"
        last_activity = seat.get("last_activity_at")
        last_activity_str = last_activity[:10] if last_activity else "Sin actividad"
        
        pending = seat.get("pending_cancellation_date")
        if pending:
            status = f"⚠️ Cancela: {pending[:10]}"
        elif last_activity:
            status = "🟢 Activo"
        else:
            status = "⚪ Inactivo"
        
        print(f"{login:<25} {created:<15} {last_activity_str:<20} {status}")
    
    print("-" * 90)
    print(f"Total: {len(seats)} usuarios")
    print("=" * 90 + "\n")


def print_summary(data: dict, report_type: str):
    """
    Imprime un resumen de los datos obtenidos.

    Args:
        data: Datos del reporte
        report_type: Tipo de reporte
    """
    print("\n" + "=" * 60)
    print(f"📈 RESUMEN DEL REPORTE: {report_type.upper()}")
    print("=" * 60)

    if "report_start_day" in data and "report_end_day" in data:
        print(f"📅 Período: {data['report_start_day']} a {data['report_end_day']}")
    elif "report_day" in data:
        print(f"📅 Día: {data['report_day']}")

    if "download_links" in data:
        print(f"📁 Archivos de reporte: {len(data['download_links'])}")

    if "data" in data and isinstance(data["data"], list):
        print(f"📊 Registros obtenidos: {len(data['data'])}")
        
        # Si hay datos, mostrar algunas métricas
        if len(data["data"]) > 0:
            sample = data["data"][0]
            print(f"\n📋 Campos disponibles en el reporte:")
            for key in list(sample.keys())[:10]:
                print(f"   - {key}")
            if len(sample.keys()) > 10:
                print(f"   ... y {len(sample.keys()) - 10} campos más")

    print("=" * 60 + "\n")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Generador de reportes de métricas de GitHub Copilot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python copilot_metrics.py                     # Reporte de 28 días
  python copilot_metrics.py --day 2026-01-15    # Reporte de un día específico
  python copilot_metrics.py --users             # Incluir métricas por usuario
  python copilot_metrics.py --format csv        # Exportar a CSV
  python copilot_metrics.py --format excel      # Exportar a Excel
        """
    )
    
    parser.add_argument(
        "--day",
        type=str,
        help="Día específico para el reporte (formato: YYYY-MM-DD)"
    )
    parser.add_argument(
        "--users",
        action="store_true",
        help="Incluir métricas detalladas por usuario"
    )
    parser.add_argument(
        "--seats",
        action="store_true",
        help="Mostrar lista de usuarios con seats de Copilot asignados"
    )
    parser.add_argument(
        "--breakdown",
        action="store_true",
        help="Mostrar usage breakdown por usuario (similar a GitHub UI)"
    )
    parser.add_argument(
        "--enterprise",
        action="store_true",
        help="Obtener métricas a nivel de empresa"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "csv", "excel"],
        default=os.getenv("OUTPUT_FORMAT", "json"),
        help="Formato de salida (default: json)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.getenv("OUTPUT_DIR", "./reports"),
        help="Directorio de salida (default: ./reports)"
    )
    parser.add_argument(
        "--org",
        type=str,
        default=os.getenv("GITHUB_ORG"),
        help="Nombre de la organización de GitHub"
    )
    parser.add_argument(
        "--token",
        type=str,
        default=os.getenv("GITHUB_TOKEN"),
        help="Token de acceso personal de GitHub"
    )

    args = parser.parse_args()

    # Validar parámetros requeridos
    if not args.token:
        print("❌ Error: Se requiere un token de GitHub.")
        print("   Configura la variable GITHUB_TOKEN en el archivo .env")
        print("   o usa el parámetro --token")
        sys.exit(1)

    if not args.org:
        print("❌ Error: Se requiere el nombre de la organización.")
        print("   Configura la variable GITHUB_ORG en el archivo .env")
        print("   o usa el parámetro --org")
        sys.exit(1)

    # Banner
    print("\n" + "=" * 60)
    print("🚀 GitHub Copilot Usage Metrics Report Generator")
    print("=" * 60)
    print(f"📁 Organización: {args.org}")
    print(f"📂 Directorio de salida: {args.output}")
    print(f"📄 Formato: {args.format}")
    print("=" * 60 + "\n")

    # Inicializar cliente y generador
    enterprise = os.getenv("GITHUB_ENTERPRISE") if args.enterprise else None
    client = CopilotMetricsClient(args.token, args.org, enterprise)
    generator = ReportGenerator(args.output, args.format)

    reports_generated = []

    try:
        # Obtener métricas de organización
        if args.day:
            # Métricas para un día específico
            org_metrics = client.get_org_metrics_by_day(args.day)
            report_type = f"org_day_{args.day}"
        else:
            # Métricas de 28 días
            org_metrics = client.get_org_metrics_28_day()
            report_type = "org_28_day"

        if org_metrics:
            print_summary(org_metrics, report_type)
            filepath = generator.save_report(org_metrics, report_type)
            reports_generated.append(filepath)

        # Obtener métricas por usuario si se solicita
        if args.users:
            if args.day:
                users_metrics = client.get_org_users_metrics_by_day(args.day)
                users_report_type = f"users_day_{args.day}"
            else:
                users_metrics = client.get_org_users_metrics_28_day()
                users_report_type = "users_28_day"

            if users_metrics:
                print_summary(users_metrics, users_report_type)
                filepath = generator.save_report(users_metrics, users_report_type)
                reports_generated.append(filepath)

        # Obtener métricas de empresa si se solicita
        if args.enterprise:
            enterprise_metrics = client.get_enterprise_metrics_28_day()
            if enterprise_metrics:
                print_summary(enterprise_metrics, "enterprise_28_day")
                filepath = generator.save_report(enterprise_metrics, "enterprise_28_day")
                reports_generated.append(filepath)

        # Obtener lista de seats (usuarios con Copilot)
        if args.seats or args.breakdown:
            seats_data = client.get_copilot_billing_seats()
            
            if seats_data:
                if args.breakdown:
                    # Obtener métricas por usuario para el breakdown
                    print("📊 Obteniendo métricas detalladas por usuario...")
                    if args.day:
                        users_metrics_breakdown = client.get_org_users_metrics_by_day(args.day)
                    else:
                        users_metrics_breakdown = client.get_org_users_metrics_28_day()
                    
                    # Mostrar tabla estilo GitHub UI con métricas reales
                    print_usage_breakdown(seats_data, users_metrics_breakdown)
                    
                    # Guardar también las métricas de usuarios
                    if users_metrics_breakdown:
                        filepath = generator.save_report(users_metrics_breakdown, "users_breakdown")
                        reports_generated.append(filepath)
                else:
                    # Mostrar detalle de seats
                    print_seats_detail(seats_data)
                
                # Guardar reporte de seats
                filepath = generator.save_report(seats_data, "seats")
                reports_generated.append(filepath)

        # Resumen final
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print(f"📊 Reportes generados: {len(reports_generated)}")
        for report in reports_generated:
            print(f"   📄 {report}")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\n⚠️  Proceso cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
