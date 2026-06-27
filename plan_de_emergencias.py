import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
TOKEN = os.getenv("TOKEN")

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
        "/biologico — PON Riesgo biológico / Pandemia\n"
        "/hurto — PON Hurto / Amenaza de seguridad\n\n"
        "🩺 *Primeros auxilios:*\n"
        "/primeros\\_auxilios — Heridas, golpes, quemaduras\n"
        "/convulsion — Si un niño convulsiona\n\n"
        "🟣 *Evacuación:*\n"
        "/rutas — Rutas de evacuación\n"
        "/punto\\_encuentro — Punto de encuentro (PMU)\n"
        "/extintor — Técnica JALE para extintor"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

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
        "/incendio | /sismo | /tormenta | /biologico | /hurto\n\n"
        "6️⃣ *EVACÚA SI SE ORDENA*\n"
        "Sigue las /rutas hacia el /punto\\_encuentro.\n"
        "Cuenta niños antes de salir y al llegar.\n\n"
        "7️⃣ *ESPERA AUTORIZACIÓN PARA REINGRESAR*\n"
        "Nadie regresa sin orden del Comité de Emergencias.\n\n"
        "8️⃣ *POST-EMERGENCIA*\n"
        "Reporta a la ARL en menos de 24 horas.\n"
        "Elabora informe del evento. Repone elementos en menos de 48 horas.\n\n"
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
        "🏨 Hospital / Centro de Salud: *3105591538*\n"
        "📋 ARL (reportar accidentes): *018000511414*\n\n"
        "📌 _Guarda estos números en tu celular personal._\n"
        "_El reporte a la ARL debe hacerse en máximo 24 horas tras el evento._"
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
        "⚠️ En ausencia de un rol, el superior inmediato asume sus funciones.\n"
        "Simulacros mínimo 1 vez al año (decreto 1072 de 2015)."
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
        "1. Quien detecta la emergencia avisa de inmediato al *Director del Plan* "
        "y al *Jefe de Brigada*.\n"
        "2. Ellos activan la cadena de llamadas al resto del Comité.\n"
        "3. El Comité se reúne en el *Punto de Encuentro* (PMU).\n"
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
        "Evalúa daños. Notifica ARL en máx 24 h.\n"
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
        "AGÁCHATE — CÚBRETE — SUJÉTATE\n"
        "Protege cabeza y cuello bajo escritorios o junto a columnas.\n"
        "Aléjate de ventanas, estantes y zonas de vidrio.\n"
        "❌ No intentes evacuar durante el sismo.\n\n"
        "✅ *Después (Docentes / Coordinadores):*\n"
        "Calma al grupo. Verifica heridos.\n"
        "No muevas lesionados graves.\n"
        "Evalúa daños estructurales visibles.\n"
        "Activa evacuación solo si el Coordinador lo indica.\n\n"
        "🚶 *Evacuación (si hay daño estructural):*\n"
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
        "3. Llama al hospital: *3105591538* o NUSE: *123*\n"
        "4. Si no respira y no hay pulso: inicia RCP.\n"
        "5. Mantenla abrigada y tranquila.\n\n"
        "📋 *Post-evento (Coordinador):*\n"
        "Inspecciona instalaciones eléctricas antes de reconectar.\n"
        "Reporta daños a mantenimiento. Elabora informe.\n\n"
        "📞 Hospital / Centro de Salud: *3105591538* | NUSE: *123*"
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
        "📞 Hospital / Centro de Salud: *3105591538*\n"
        "🆘 NUSE: *123*"
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
        "🩺 *PRIMEROS AUXILIOS BÁSICOS*\n\n"
        "🩸 *Herida con sangrado:*\n"
        "• Presiona con paño limpio de forma sostenida.\n"
        "• No retires el paño; agrega otro encima si se empapa.\n"
        "• Eleva la zona. Si no para en 5 min → 3105591538.\n\n"
        "🔥 *Quemadura leve:*\n"
        "• Agua fría (no helada) durante 10-15 minutos.\n"
        "• No apliques pasta dental ni cremas caseras.\n"
        "• Si es grande o profunda → 3105591538 de inmediato.\n\n"
        "🤕 *Golpe en la cabeza:*\n"
        "• Sienta al niño y obsérvalo.\n"
        "• Vómito, pérdida de conciencia o llanto excesivo → 3105591538.\n"
        "• Hielo envuelto en tela, nunca directo.\n"
        "• Avisa siempre a los acudientes.\n\n"
        "😮 *Niño que se atraganta:*\n"
        "• Si puede toser → anímalo a seguir tosiendo.\n"
        "• Si no puede respirar → maniobra de Heimlich + llama al 123.\n\n"
        "😵 *Inconsciente:*\n"
        "• Llámalo por su nombre. Si no responde → 123.\n"
        "• No lo muevas si sospechas golpe en cabeza o cuello.\n\n"
        "⚡ *Descarga eléctrica* → /tormenta\n"
        "⚠️ *Convulsión* → /convulsion\n\n"
        "📞 Hospital / Centro de Salud: *3105591538* | NUSE: *123*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  /convulsion
# ─────────────────────────────────────────────────────────────────────────────
async def convulsion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizada(update.effective_user.id):
        await acceso_denegado(update); return
    mensaje = (
        "🧠 *QUÉ HACER SI UN NIÑO CONVULSIONA*\n\n"
        "⏱️ *Mira el reloj al inicio. El tiempo importa.*\n\n"
        "✅ *SÍ debes hacer:*\n\n"
        "1. Llama al 3105591538 si dura más de 5 minutos o es la primera vez.\n"
        "2. Baja al niño al suelo con cuidado.\n"
        "3. Ponlo de lado para que no se ahogue con saliva.\n"
        "4. Aleja objetos duros a su alrededor.\n"
        "5. Protege su cabeza con tu mano o una chaqueta doblada.\n"
        "6. Afloja ropa ajustada en el cuello.\n"
        "7. Quédate a su lado: _'Estoy aquí, ya pasa.'_\n"
        "8. Al terminar, ponlo de lado y espera que despierte.\n"
        "9. Anota: duración, movimientos, color de piel.\n\n"
        "🚫 *NO debes hacer:*\n\n"
        "• No sujetes ni intentes detener los movimientos\n"
        "• No metas nada en su boca\n"
        "• No le des agua ni comida\n"
        "• No lo dejes solo\n"
        "• No te asustes en voz alta frente a otros niños\n\n"
        "👦 *Después:* Puede estar confuso o dormido. Es normal.\n"
        "Avisa a coordinación y a los acudientes.\n\n"
        "📞 Hospital / Centro de Salud: *3105591538* | NUSE: *123*"
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
        "Sigue las señales y flechas verdes de evacuación en las paredes.\n\n"
        "🚪 *Salida principal:*\n"
        "[Completa con la ruta real del jardín]\n\n"
        "🚪 *Salida secundaria:*\n"
        "[Completa con la ruta real del jardín]\n\n"
        "🚪 *Salida de emergencia:*\n"
        "[Completa con la ruta real del jardín]\n\n"
        "🚶 *Durante la evacuación:*\n"
        "• Camina, no corras. Niños en fila.\n"
        "• Cuenta antes de salir y al llegar al punto.\n"
        "• Cierra puertas al salir (sin llave).\n"
        "• Asiste a niños con movilidad reducida.\n"
        "• Si una ruta está bloqueada, usa la alterna.\n\n"
        "⏱️ El tiempo máximo de preparación para salir es 40 segundos.\n\n"
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
        "📍 *PUNTO DE ENCUENTRO — PMU*\n"
        "_SG-SST-PL-04 4.6.1 — Puesto de Mando Unificado_\n\n"
        "🏁 *Punto principal:*\n"
        "[Completa con la ubicación exacta del jardín]\n\n"
        "🏁 *Punto alternativo:*\n"
        "[Completa con la ubicación alternativa]\n\n"
        "✅ *Al llegar:*\n"
        "1. Cuenta a TODOS los niños — verifica con lista de asistencia.\n"
        "2. Repórtate con el Director del Plan o Coordinadora de Emergencias.\n"
        "3. Mantén a los niños sentados y tranquilos.\n"
        "4. No permitas que ningún niño se aleje del grupo.\n"
        "5. Espera instrucciones del Comité de Emergencias.\n"
        "6. *No regreses al edificio* sin autorización oficial.\n\n"
        "⚠️ Si falta un niño, avisa de inmediato al Jefe de Brigada.\n"
        "El Comité autoriza el reingreso solo tras inspección estructural.\n\n"
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
        "📍 Extintores tipo ABC ubicados en:\n"
        "[Completa con la ubicación real en el jardín]\n\n"
        "📞 Bomberos Tibasosa: *3053123903*"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────────────────────────
#  Arranque del bot
# ─────────────────────────────────────────────────────────────────────────────
async def run():
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
    app.add_handler(CommandHandler("biologico",         biologico))
    app.add_handler(CommandHandler("hurto",             hurto))
    # Primeros auxilios
    app.add_handler(CommandHandler("primeros_auxilios", primeros_auxilios))
    app.add_handler(CommandHandler("convulsion",        convulsion))
    # Evacuación
    app.add_handler(CommandHandler("rutas",             rutas))
    app.add_handler(CommandHandler("punto_encuentro",   punto_encuentro))
    app.add_handler(CommandHandler("extintor",          extintor))

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
