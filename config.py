from pathlib import Path

NOMBRE_NEGOCIO = "Liseth"
ESLOGAN = "Control de papas y pollerías · del cuaderno a la nube"

_RAIZ = Path(__file__).resolve().parent
LOGIN_BG = _RAIZ / "assets" / "login_papas.jpg"
APP_BG = _RAIZ / "assets" / "app_papas_fritas.jpg"

LISTA_POLLERIAS = [
    "Pollería Damnus",
    "Pollería Reynoso",
    "Pollería Taco tico",
    "Pollería Broster. Tac.",
    "Pollería Broster. Fos.",
    "Pollería Broster. Ent.",
    "Pollería Dorados",
    "Pollería Perez",
    "Pollería Patrón",
    "Pollería Surys",
    "Pollería Elimar",
    "Pollería Huaylacho",
    "Pollería Pollón. Pas.",
    "Pollería Pollón. Ind.",
    "Pollería Milano",
    "Pollería Qui wui",
    "Pollería León",
    "Pollería D'criss",
    "Pollería Vegas",
    "Pollería Estrella",
    "Pollería Lua",
    "Pollería Paisa",
    "Pollería Tacuchi",
    "Pollería Alitas",
    "Pollería Covida",
    "Pollería Jairo",
    "Pollería Orión",
    "Pollería Lopez",
    "Pollería Gisela",
    "Pollería Verónica",
    "Pollería Chike burger",
    "Pollería Totus",
]

ESTADOS_PAGO = ["Pagado en efectivo", "Transferencia", "Fiado / Debe"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
TABS_DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
SECCIONES = ["Cuaderno Semanal", "Resumen Semanal", "Cuentas por Cobrar"]
