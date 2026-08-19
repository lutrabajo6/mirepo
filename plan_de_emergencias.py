import asyncio
import os
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# SEGURIDAD: nunca escribas el token directamente en este archivo.
# Revoca en BotFather el token que aparecía en la versión anterior y genera uno nuevo.
# Instala la dependencia: pip install "python-telegram-bot>=20,<23"
# Antes de ejecutar:
# Windows PowerShell:  $env:TELEGRAM_BOT_TOKEN="TOKEN_NUEVO"
# Linux/macOS:         export TELEGRAM_BOT_TOKEN="TOKEN_NUEVO"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Este número debe ser confirmado formalmente por la institución antes de usarlo.
CENTRO_SALUD = os.getenv("CENTRO_SALUD_TELEFONO", "").strip()

TECLADO = ReplyKeyboardMarkup(
    [
        ["🔥 Incendio", "🌍 Sismo"],
        ["⛈️ Tormenta", "🌧️ Inundación"],
        ["🦠 Riesgo biológico", "🔒 Intrusión"],
        ["🗺️ Rutas", "📍 Punto de encuentro"],
        ["📞 Contactos", "👥 Brigada"],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# ─────────────────────────────────────────────
#  LISTA DE AUTORIZADAS — SG-SST-PL-04 5.3
#  Reemplaza cada 0000000000 con el ID real
#  usando obtener_ids.py antes de activar el bot
# ─────────────────────────────────────────────
DOCENTES_AUTORIZADAS = {
    6548130564: "Docente autorizada",      # ya tenías este ID
    6809336072: "Docente autorizada",      # ya tenías este ID
    # ── Agrega aquí los IDs del listado de brigadistas ──
    # 0000000001: "Miguel Ángel Bayona Ojeda — Rector / Director del Plan",
    # 0000000002: "Jessica Ximena Arévalo — Brigadista integral",
    # 0000000003: "Deisy Mariana Bernal Caro — Brigadista integral",
    # 0000000004: "Yessica Alexandra Sissa Aguilar — Coordinadora de Emergencias",
    # 0000000005: "María Alejandra Barón Cachope — Brigadista integral",
    # 0000000006: "Andrea Julieth Becerra López — Jefe de Brigada",
    # 0000000007: "Laura Carolina Olmos Pulido — Brigadista integral",
    # 0000000008: "Yolima Riaño Suárez — Encargada de Comunicaciones",
    # 0000000009: "Nidia Paola Fonseca Vargas — Brigadista integral",
    # 0000000010: "Angelica Cardozo Camargo — Coordinadora de Evacuación",
}

def autorizada(user_id):
    return user_id in DOCENTES_AUTORIZADAS

def contacto_salud():
    """Muestra el número local solo cuando fue validado y configurado."""
    if CENTRO_SALUD:
        return f"🏥 Centro de Salud validado: *{CENTRO_SALUD}*\n"
    return "🏥 Centro de Salud: *pendiente de validación institucional*\n"

async def acceso_denegado(update):
    await update.message.reply_text("⛔ No tienes acceso. Comunícate con coordinación.")

# ─────────────────────────────────────────────────────────────────────────────
#  /start
# ─────────────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    nombre = update.effective_user.first_name
    mensaje = (
        f"🌟 Hola, {nombre}. Bienvenida al bot de emergencias del\n"
        "*Centro Educativo Mi Mundo Mágico de Tibasosa*\n"
        "_SG-SST-PL-04 — Plan de Emergencias v01_\n\n"
        "📋 *Comandos disponibles:*\n\n"
        "🟢 *Información general:*\n"
        "/emergencias — Pasos generales ante cualquier emergencia\n"
        "/mantener\\_calma — Cómo calmarte y calmar a los niños\n"
        "/contactos — Directorio de emergencias oficial\n"
        "/brigada — Roles y brigadistas del jardín\n"
        "/cadena — Cadena de llamadas y activación\n\n"
        "🔴 *Protocolos PON:*\n"
        "/incendio — PON Incendio\n"
        "/sismo — PON Sismo\n"
        "/tormenta — PON Tormenta eléctrica / Descarga\n"
        "/inundacion — PON Inundación\n"
        "/biologico — PON Riesgo biológico / Pandemia\n"
        "/hurto — PON Hurto / Amenaza de seguridad\n\n"
        "🩺 *Primeros auxilios:*\n"
        "/primeros\\_auxilios — Heridas, golpes, quemaduras\n"
        "/convulsion — Si un niño convulsiona\n\n"
        "🟣 *Evacuación:*\n"
        "/rutas — Rutas de evacuación\n"
        "/punto\\_encuentro — Punto de encuentro (PMU)\n"
        "/extintor — Técnica JALE para extintor\n\n"
        "⚠️ *En una emergencia real:* activa la alarma, llama al *123* "
        "y sigue las instrucciones del Director del Plan o la Coordinadora de Emergencias. "
        "El bot es una guía y no reemplaza a los organismos de socorro."
    )
    await update.message.reply_text(
        mensaje,
        parse_mode="Markdown",
        reply_markup=TECLADO,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  /emergencias
# ─────────────────────────────────────────────────────────────────────────────
async def emergencias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🚨 *PASOS GENERALES ANTE CUALQUIER EMERGENCIA*\n"
        "_Centro Educativo Mi Mundo Mágico de Tibasosa — SG-SST-PL-04_\n\n"
        "1️⃣ *MANTÉN LA CALMA* → /mantener\\_calma\n\n"
        "2️⃣ *DETECTA Y EVALÚA*\n"
        "¿Hay peligro inmediato? ¿Alguien está herido?\n"
        "Identifica el tipo de emergencia.\n\n"
        "3️⃣ *ACTIVA LA ALERTA*\n"
        "Avisa a la Coordinadora de Emergencias y al Jefe de Brigada.\n"
        "Activa la cadena de llamadas → /cadena\n\n"
        "4️⃣ *PROTEGE A LOS NIÑOS PRIMERO*\n"
        "Agrúpalos. Nunca los dejes solos.\n\n"
        "5️⃣ *APLICA EL PON CORRESPONDIENTE*\n"
        "/incendio | /sismo | /tormenta | /inundacion | /biologico | /hurto\n\n"
        "6️⃣ *EVACÚA SI SE ORDENA*\n"
        "Sigue las /rutas hacia el /punto\\_encuentro.\n"
        "Cuenta niños antes de salir y al llegar.\n\n"
        "7️⃣ *ESPERA AUTORIZACIÓN PARA REINGRESAR*\n"
        "Nadie regresa sin autorización del Director del Plan.\n\n"
        "8️⃣ *POST-EMERGENCIA*\n"
        "Elabora el informe institucional. El responsable del SG-SST determinará "
        "si corresponde reportar el evento a la ARL.\n"
        "Repone los elementos de emergencia utilizados antes de 48 horas.\n\n"
        "📞 Emergencias general: *123*\n"
        "🚒 Bomberos Tibasosa: *3053123903*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /mantener_calma
# ─────────────────────────────────────────────────────────────────────────────
async def mantener_calma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🧘 *CÓMO MANTENER LA CALMA EN EMERGENCIAS*\n\n"
        "━━━━ PARA TI ━━━━\n\n"
        "🫁 *Respiración de emergencia:*\n"
        "Inhala 4 seg → Sostén 4 seg → Exhala 6 seg.\n"
        "Repite 3 veces.\n\n"
        "🎯 *Técnica 5-4-3-2-1:*\n"
        "• 5 cosas que puedes VER\n"
        "• 4 cosas que puedes TOCAR\n"
        "• 3 cosas que puedes OÍR\n"
        "• 2 cosas que puedes OLER\n"
        "• 1 cosa que puedes SABOREAR\n\n"
        "💬 *Frase de anclaje:*\n"
        "_'Estoy aquí, los niños me necesitan, puedo con esto.'_\n\n"
        "━━━━ PARA LOS NIÑOS ━━━━\n\n"
        "🗣️ Habla con voz firme y calmada.\n"
        "Di: _'Tranquilos, estamos bien, vamos juntos.'_\n\n"
        "🐢 *Respiración de la tortuga:*\n"
        "Sopla suave como si apagaras una velita lejos.\n\n"
        "🤝 Toma de la mano al niño más asustado.\n"
        "El contacto físico tranquiliza.\n\n"
        "🚫 Nunca solo digas 'cálmate'.\n"
        "Muéstrales CON tu cuerpo cómo respirar."
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /contactos — Directorio oficial SG-SST-PL-04 5.1
# ─────────────────────────────────────────────────────────────────────────────
async def contactos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "📞 *DIRECTORIO DE EMERGENCIAS OFICIAL*\n"
        "_SG-SST-PL-04 5.1 — Centro Educativo Mi Mundo Mágico de Tibasosa_\n\n"
        "🆘 Emergencias General (NUSE): *123* — 24 horas\n"
        "🚒 Bomberos Tibasosa: *3053123903*\n"
        "👮 Policía Nacional: *112*\n"
        "🏥 Cruz Roja Colombiana: *3133007105*\n"
        "🛡️ Defensa Civil: *3112620844*\n"
        f"{contacto_salud()}"
        "📋 ARL (reportar accidentes): *018000511414*\n\n"
        "📌 _Guarda estos números en tu celular personal._\n"
        "_El responsable del SG-SST define si corresponde realizar el reporte a la ARL._"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /brigada — Roles y brigadistas SG-SST-PL-04 5.3
# ─────────────────────────────────────────────────────────────────────────────
async def brigada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "👥 *BRIGADA DE EMERGENCIAS*\n"
        "_SG-SST-PL-04 4.5 y 5.3 — Listado de brigadistas_\n\n"
        "🔴 *Director del Plan:*\n"
        "Miguel Ángel Bayona Ojeda — Rector\n\n"
        "🟠 *Jefe de Brigada:*\n"
        "Andrea Julieth Becerra López\n\n"
        "🟡 *Coordinadora de Emergencias:*\n"
        "Yessica Alexandra Sissa Aguilar\n\n"
        "🟢 *Coordinadora de Evacuación:*\n"
        "Angelica Cardozo Camargo\n\n"
        "📡 *Encargada de Comunicaciones:*\n"
        "Yolima Riaño Suárez\n\n"
        "🔵 *Brigadistas integrales:*\n"
        "• Jessica Ximena Arévalo\n"
        "• Deisy Mariana Bernal Caro\n"
        "• María Alejandra Barón Cachope\n"
        "• Laura Carolina Olmos Pulido\n"
        "• Nidia Paola Fonseca Vargas\n\n"
        "📅 Última capacitación: 30 de mayo de 2026\n\n"
        "⚠️ En ausencia de un responsable, comunícate con el Director del Plan "
        "o la Coordinadora de Emergencias y sigue la cadena institucional.\n"
        "Simulacros: mínimo una vez al año, según el plan institucional."
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /cadena — Cadena de llamadas y fases de activación SG-SST-PL-04 4.2
# ─────────────────────────────────────────────────────────────────────────────
async def cadena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "📣 *CADENA DE LLAMADAS Y ACTIVACIÓN*\n"
        "_SG-SST-PL-04 4.2 — Reporte, evaluación y activación_\n\n"
        "━━━━ FASE 1: ALERTA ━━━━\n\n"
        "1. Quien detecta la emergencia avisa de inmediato a la "
        "*Coordinadora de Emergencias* o al *Director del Plan*.\n"
        "2. Se activa la cadena de llamadas al Comité y a la brigada.\n"
        "3. El Comité se reúne en el PMU definido en un lugar seguro.\n"
        "4. Se verifica: veracidad, naturaleza, magnitud y vulnerabilidad.\n\n"
        "━━━━ DECISIONES DEL COMITÉ ━━━━\n\n"
        "• Volver a la normalidad y hacer seguimiento.\n"
        "• Permanecer reunidos y en alerta.\n"
        "• Pasar a Fase 2 (acción).\n"
        "• Avisar a organismos externos (bomberos, policía, ARL).\n\n"
        "━━━━ FASE 2: ACCIÓN ━━━━\n\n"
        "Se inicia con el impacto. Dos acciones simultáneas:\n\n"
        "1️⃣ *Evacuación* — coordinada por Coordinadora de Evacuación.\n"
        "2️⃣ *Brigada activa* — primeros auxilios, rescate, control.\n\n"
        "📞 Bomberos Tibasosa: *3053123903*\n"
        "🆘 Emergencias general: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /incendio — PON Incendio SG-SST-PL-04 4.1.1
# ─────────────────────────────────────────────────────────────────────────────
async def incendio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🔥 *PON — INCENDIO*\n"
        "_SG-SST-PL-04 4.1.1_\n\n"
        "🔍 *Detección (Todo el personal):*\n"
        "Al detectar humo o fuego: no intentes apagar si el fuego es grande.\n"
        "Activa alarma (pito / voz). Avisa al Coordinador de Emergencias y brigada.\n\n"
        "📢 *Activación (Coordinadora de Emergencias):*\n"
        "Llama a Bomberos Tibasosa: *3053123903*\n"
        "Notifica al Comité. Evalúa magnitud.\n\n"
        "🧯 *Respuesta (Brigada contraincendios):*\n"
        "Conato: usa extintor tipo ABC — técnica JALE → /extintor\n"
        "Corta el suministro eléctrico del área.\n"
        "No abras puertas si hay humo al otro lado.\n\n"
        "🚶 *Evacuación (Coordinadora de Evacuación):*\n"
        "Activa evacuación total por /rutas establecidas.\n"
        "Guía a estudiantes al /punto\\_encuentro\n"
        "Verifica lista de asistencia. Asiste a personas con movilidad reducida.\n\n"
        "🚒 *Control (Bomberos / Brigada):*\n"
        "Bomberos asumen el control. La brigada apoya.\n"
        "Nadie retorna hasta autorización oficial.\n\n"
        "📋 *Post-emergencia (Comité):*\n"
        "Evalúa daños. El responsable del SG-SST determina si corresponde notificar a la ARL.\n"
        "Elabora informe. Recarga extintores en máx 48 h.\n\n"
        "📞 Bomberos Tibasosa: *3053123903* | NUSE: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /sismo — PON Sismo SG-SST-PL-04 4.1.2
# ─────────────────────────────────────────────────────────────────────────────
async def sismo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🌍 *PON — SISMO*\n"
        "_SG-SST-PL-04 4.1.2_\n\n"
        "⚡ *Durante el movimiento (Todo el personal):*\n"
        "AGÁCHATE — CÚBRETE — AGÁRRATE\n"
        "Protege cabeza y cuello bajo escritorios o junto a columnas.\n"
        "Aléjate de ventanas, estantes y zonas de vidrio.\n"
        "❌ No intentes evacuar durante el sismo.\n\n"
        "✅ *Después (Docentes / Coordinadores):*\n"
        "Calma al grupo. Verifica heridos.\n"
        "No muevas lesionados graves.\n"
        "Evalúa daños estructurales visibles.\n"
        "Evacúa después de finalizar el movimiento y solo cuando el Coordinador lo indique.\n\n"
        "🚶 *Evacuación (por orden del Coordinador):*\n"
        "Evacúa ante daños, obstáculos u otras condiciones que hagan insegura la permanencia.\n"
        "Usa rutas alternas si la principal está bloqueada → /rutas\n"
        "Desconecta gas y electricidad si es seguro hacerlo.\n\n"
        "📍 *En el punto de encuentro (PMU):*\n"
        "Verifica listas. Atiende heridos → /primeros\\_auxilios\n"
        "Espera inspección estructural antes de reingresar.\n\n"
        "⚠️ Pueden venir réplicas. No ingreses hasta autorización.\n\n"
        "📞 Bomberos Tibasosa: *3053123903*\n"
        "🛡️ Defensa Civil: *3112620844* | NUSE: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /tormenta — PON Tormenta eléctrica SG-SST-PL-04 4.1.3
# ─────────────────────────────────────────────────────────────────────────────
async def tormenta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "⛈️ *PON — TORMENTA ELÉCTRICA / DESCARGA*\n"
        "_SG-SST-PL-04 4.1.3_\n\n"
        "⚠️ *Alerta previa (Coordinador / Docentes):*\n"
        "Al ver nubes oscuras o escuchar truenos lejanos:\n"
        "• Suspende actividades al aire libre de inmediato.\n"
        "• Ingresa todo el personal y estudiantes a las aulas.\n"
        "• Cierra ventanas y puertas.\n\n"
        "🏠 *Durante (Todo el personal):*\n"
        "• Mantente alejada de ventanas, enchufes y equipos eléctricos.\n"
        "• No toques tuberías metálicas.\n"
        "• Desconecta equipos electrónicos.\n"
        "• No salgas al exterior hasta que pase.\n\n"
        "⚡ *Si hay víctima por descarga eléctrica (Brigada Primeros Auxilios):*\n"
        "1. NO la toques sin cortar primero la electricidad.\n"
        "2. Corta el suministro eléctrico del área.\n"
        "3. Llama al NUSE: *123*.\n"
        "4. Si no respira, una persona capacitada debe iniciar RCP y seguir "
        "las instrucciones del servicio de emergencias.\n"
        "5. Mantenla abrigada y tranquila.\n\n"
        "📋 *Post-evento (Coordinador):*\n"
        "Inspecciona instalaciones eléctricas antes de reconectar.\n"
        "Reporta daños a mantenimiento. Elabora informe.\n\n"
        "📞 NUSE: *123*\n"
        f"{contacto_salud()}"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /inundacion — Amenaza identificada en SG-SST-DC-01
# ─────────────────────────────────────────────────────────────────────────────
async def inundacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🌧️ *PROTOCOLO — INUNDACIÓN*\n"
        "_SG-SST-DC-01 y SG-SST-PL-04_\n\n"
        "⚠️ *Prevención y alerta:*\n"
        "• Vigila la acumulación de agua y el estado de drenajes y canaletas.\n"
        "• Mantén despejadas las salidas y los recorridos de evacuación.\n"
        "• Informa de inmediato a la Coordinadora de Emergencias.\n"
        "• Mantén a los niños alejados de zonas inundadas y conexiones eléctricas.\n\n"
        "🚶 *Si se ordena evacuar:*\n"
        "• Evacúa primero las aulas o zonas bajas.\n"
        "• Sigue la ruta que indique la Coordinadora de Evacuación.\n"
        "• No uses la cancha si está inundada o comprometida.\n"
        "• Dirígete al punto alterno indicado y verifica la lista de asistencia.\n\n"
        "❌ No atravieses corrientes ni acumulaciones de agua.\n"
        "❌ No regreses hasta que el Director del Plan lo autorice.\n\n"
        "🆘 Emergencias: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /biologico — PON Riesgo biológico SG-SST-PL-04 4.1.4
# ─────────────────────────────────────────────────────────────────────────────
async def biologico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🦠 *PON — RIESGO BIOLÓGICO / PANDEMIA*\n"
        "_SG-SST-PL-04 4.1.4_\n\n"
        "🛡️ *Prevención (Coordinadora SG-SST):*\n"
        "• Garantizar disponibilidad de jabón, alcohol gel y tapabocas.\n"
        "• Mantener ventilación adecuada en aulas.\n"
        "• Coordinar protocolo de bioseguridad con centro de salud.\n\n"
        "🤒 *Caso sospechoso (Docente / Coordinador):*\n"
        "1. Aisla al estudiante o empleado sintomático en área designada.\n"
        "2. Notifica al acudiente de inmediato.\n"
        "3. Orienta hacia el centro de salud.\n"
        "4. Registra el caso por escrito.\n"
        "5. Informa a autoridades de salud si aplica.\n\n"
        "🚨 *Contingencia (Directivos):*\n"
        "• Activa protocolo de bioseguridad reforzado.\n"
        "• Evalúa suspensión de actividades presenciales.\n"
        "• Desinfecta instalaciones.\n"
        "• Coordina con la Secretaría de Salud Municipal.\n\n"
        "🆘 NUSE: *123*\n"
        f"{contacto_salud()}"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /hurto — PON Hurto / Amenaza de seguridad SG-SST-PL-04 4.1.5
# ─────────────────────────────────────────────────────────────────────────────
async def hurto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🔒 *PON — HURTO POR INTRUSIÓN / AMENAZA DE SEGURIDAD*\n"
        "_SG-SST-PL-04 4.1.5_\n\n"
        "👁️ *Detección (Todo el personal):*\n"
        "Al detectar persona sospechosa o intrusión:\n"
        "• ❌ NO confrontes al intruso.\n"
        "• Activa silenciosamente la alerta al Coordinador.\n"
        "• Mantén a los estudiantes en las aulas con puertas cerradas.\n\n"
        "📢 *Activación (Coordinador / Director):*\n"
        "• Llama al 123 (Policía Nacional) de inmediato.\n"
        "• Describe la situación con calma.\n"
        "• No permitas ingreso ni salida de personas.\n"
        "• Asegura los accesos.\n\n"
        "✅ *Control (Policía / Coordinador):*\n"
        "• La Policía asume el control — coopera plenamente.\n"
        "• Preserva la escena si hubo delito (no toques nada).\n"
        "• Elabora denuncia y reporte institucional.\n\n"
        "📞 Policía Nacional: *112* | NUSE: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /primeros_auxilios
# ─────────────────────────────────────────────────────────────────────────────
async def primeros_auxilios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🩺 *PRIMEROS AUXILIOS — ORIENTACIÓN INICIAL*\n\n"
        "⚠️ Esta guía no reemplaza la atención médica. La intervención debe ser "
        "realizada por una persona capacitada y con elementos de bioseguridad.\n\n"
        "1. Verifica que el lugar sea seguro antes de acercarte.\n"
        "2. Activa la brigada de primeros auxilios.\n"
        "3. Si la persona no responde, no respira normalmente, presenta sangrado "
        "abundante, dificultad respiratoria, quemadura grave o lesión importante, llama al *123*.\n"
        "4. No muevas a una persona con posible lesión de cabeza, cuello o columna, "
        "salvo que permanezca expuesta a un peligro mayor.\n"
        "5. No suministres medicamentos, alimentos ni bebidas.\n"
        "6. Acompaña a la persona y sigue las instrucciones del servicio de emergencias.\n"
        "7. Informa a coordinación y al acudiente cuando corresponda.\n\n"
        "⚡ Descarga eléctrica → /tormenta\n"
        "🧠 Convulsión → /convulsion\n\n"
        "🆘 NUSE: *123*\n"
        f"{contacto_salud()}"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /convulsion
# ─────────────────────────────────────────────────────────────────────────────
async def convulsion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🧠 *QUÉ HACER ANTE UNA CONVULSIÓN*\n\n"
        "⏱️ Registra la hora de inicio y protege al niño de lesiones.\n\n"
        "✅ *Acciones iniciales:*\n"
        "• Retira objetos cercanos y protege la cabeza con algo blando.\n"
        "• Afloja la ropa ajustada alrededor del cuello.\n"
        "• Cuando sea posible y sin forzarlo, colócalo de lado.\n"
        "• Permanece a su lado, activa la brigada y avisa a coordinación.\n"
        "• Llama al *123* si dura cinco minutos o más, se repite, es la primera "
        "convulsión conocida, existe lesión, dificultad para respirar o no recupera la conciencia.\n\n"
        "🚫 *No debes:*\n"
        "• Sujetar o intentar detener los movimientos.\n"
        "• Introducir objetos, dedos, alimentos o líquidos en la boca.\n"
        "• Dejar al niño solo.\n\n"
        "Después, informa al acudiente y registra la duración y las características observadas.\n\n"
        "🆘 NUSE: *123*\n"
        f"{contacto_salud()}"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /rutas — Rutas de evacuación SG-SST-PL-04 4.6
# ─────────────────────────────────────────────────────────────────────────────
async def rutas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🗺️ *RUTAS DE EVACUACIÓN*\n"
        "_SG-SST-PL-04 4.6 — Ver también Anexo 7: Plano de evacuación_\n\n"
        "⚠️ La documentación registra señalización parcial. Sigue la orientación "
        "de la Coordinadora de Evacuación y el plano institucional vigente.\n\n"
        "🚪 *Recorrido principal:*\n"
        "Desplázate desde el aula por el recorrido señalado hacia la cancha, "
        "solo si la ruta fue verificada como segura.\n\n"
        "🚪 *Alternativas:*\n"
        "• Costado lateral derecho del patio.\n"
        "• Puerta principal de la institución.\n"
        "La Coordinadora define la alternativa según la zona afectada.\n\n"
        "🚶 *Durante la evacuación:*\n"
        "• Camina, no corras. Niños en fila.\n"
        "• Cuenta antes de salir y al llegar al punto.\n"
        "• Cierra puertas al salir (sin llave).\n"
        "• Asiste a niños con movilidad reducida.\n"
        "• Si una ruta está bloqueada, usa la alterna.\n\n"
        "⏱️ El objetivo institucional de evacuación total es de 3 minutos o menos.\n\n"
        "📍 Al salir → /punto\\_encuentro"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /punto_encuentro — PMU SG-SST-PL-04 4.6.1
# ─────────────────────────────────────────────────────────────────────────────
async def punto_encuentro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "📍 *PUNTOS DE ENCUENTRO*\n"
        "_SG-SST-PL-04 — Aspectos de la evacuación_\n\n"
        "🏁 *Punto principal:*\n"
        "Cancha ubicada al lado de la infraestructura de la institución.\n\n"
        "🏁 *Punto alterno 1:*\n"
        "Salida por el costado lateral derecho del patio.\n\n"
        "🏁 *Punto alterno 2:*\n"
        "Puerta principal de la institución.\n\n"
        "La Coordinadora de Emergencias define el punto seguro. El PMU puede "
        "ubicarse en el punto de encuentro únicamente cuando el lugar no esté comprometido.\n\n"
        "✅ *Al llegar:*\n"
        "1. Cuenta a TODOS los niños — verifica con lista de asistencia.\n"
        "2. Repórtate con el Director del Plan o Coordinadora de Emergencias.\n"
        "3. Mantén a los niños sentados y tranquilos.\n"
        "4. No permitas que ningún niño se aleje del grupo.\n"
        "5. Espera instrucciones del Comité de Emergencias.\n"
        "6. *No regreses al edificio* sin autorización del Director del Plan.\n\n"
        "⚠️ Si falta un niño, avisa de inmediato al Jefe de Brigada.\n"
        "El Director del Plan autoriza el reingreso después de verificar condiciones seguras.\n\n"
        "📞 Bomberos Tibasosa: *3053123903* | NUSE: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /extintor — Técnica JALE (el plan usa JALE, no PASS)
# ─────────────────────────────────────────────────────────────────────────────
async def extintor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🧯 *CÓMO USAR EL EXTINTOR — TÉCNICA JALE*\n"
        "_SG-SST-PL-04 4.1.1 — Solo para conato de incendio_\n\n"
        "⚠️ *Antes de actuar verifica:*\n"
        "• ¿Los niños están fuera o con otra docente?\n"
        "• ¿Tienes una salida a tus espaldas?\n"
        "• ¿El fuego es pequeño y controlable?\n"
        "Si alguna respuesta es NO → *evacúa primero.*\n\n"
        "🔴 *J — Jala el seguro (pasador)*\n"
        "🎯 *A — Apunta a la BASE de las llamas*\n"
        "💪 *L — Lanza / aprieta la palanca*\n"
        "↔️ *E — En abanico, mueve de lado a lado*\n\n"
        "⚠️ El extintor dura solo 8 a 30 segundos.\n"
        "Si el fuego no cede → retírate y evacúa de inmediato.\n\n"
        "📍 *Inventario documentado:* un extintor tipo ABC ubicado en Rectoría.\n"
        "⚠️ El plan registra cinco unidades requeridas; confirma en campo la cantidad, "
        "ubicación, señalización y vigencia antes de intervenir.\n\n"
        "📞 Bomberos Tibasosa: *3053123903*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  Consultas en lenguaje natural y botones
# ─────────────────────────────────────────────────────────────────────────────
async def consulta_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return

    texto = (update.message.text or "").lower().strip()
    intenciones = [
        (("fuego", "humo", "incendio", "🔥"), incendio),
        (("temblor", "temblando", "sismo", "tiembla", "🌍"), sismo),
        (("tormenta", "trueno", "rayo", "descarga", "⛈"), tormenta),
        (("inund", "mucha agua", "lluvia intensa", "🌧"), inundacion),
        (("biológico", "biologico", "pandemia", "síntomas", "sintomas", "🦠"), biologico),
        (("intruso", "intrusión", "intrusion", "hurto", "persona extraña", "🔒"), hurto),
        (("ruta", "salida", "evacuar", "🗺"), rutas),
        (("punto de encuentro", "cancha", "reunión", "reunion", "📍"), punto_encuentro),
        (("contacto", "teléfono", "telefono", "llamar", "📞"), contactos),
        (("brigada", "brigadista", "responsable", "👥"), brigada),
        (("extintor", "jale", "🧯"), extintor),
        (("primeros auxilios", "herido", "lesionado"), primeros_auxilios),
        (("convuls",), convulsion),
    ]

    for palabras, funcion in intenciones:
        if any(palabra in texto for palabra in palabras):
            await funcion(update, context)
            return

    await update.message.reply_text(
        "No pude identificar la consulta. Selecciona una opción del menú o escribe, "
        "por ejemplo: *hay humo*, *está temblando*, *hay una inundación* o "
        "*cuál es el punto de encuentro*.\n\n"
        "Si existe peligro inmediato, activa la alarma y llama al *123*.",
        parse_mode="Markdown",
        reply_markup=TECLADO,
    )

async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    await update.message.reply_text(
        "Ese comando no está registrado. Usa /start para consultar el menú.",
        reply_markup=TECLADO,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  Arranque del bot
# ─────────────────────────────────────────────────────────────────────────────
async def run():
    if not TOKEN:
        raise RuntimeError(
            "Falta TELEGRAM_BOT_TOKEN. Configura un token nuevo en una variable de entorno."
        )
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",             start))
    app.add_handler(CommandHandler("emergencias",       emergencias))
    app.add_handler(CommandHandler("mantener_calma",    mantener_calma))
    app.add_handler(CommandHandler("contactos",         contactos))
    app.add_handler(CommandHandler("brigada",           brigada))
    app.add_handler(CommandHandler("cadena",            cadena))
    # PON
    app.add_handler(CommandHandler("incendio",          incendio))
    app.add_handler(CommandHandler("sismo",             sismo))
    app.add_handler(CommandHandler("tormenta",          tormenta))
    app.add_handler(CommandHandler("inundacion",        inundacion))
    app.add_handler(CommandHandler("biologico",         biologico))
    app.add_handler(CommandHandler("hurto",             hurto))
    # Primeros auxilios
    app.add_handler(CommandHandler("primeros_auxilios", primeros_auxilios))
    app.add_handler(CommandHandler("convulsion",        convulsion))
    # Evacuación
    app.add_handler(CommandHandler("rutas",             rutas))
    app.add_handler(CommandHandler("punto_encuentro",   punto_encuentro))
    app.add_handler(CommandHandler("extintor",          extintor))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, consulta_texto))
    app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))

    print("Bot Plan de Emergencias — Mi Mundo Mágico funcionando... (Ctrl+C para detener)")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(run())
