# import
from fastapi.templating import Jinja2Templates
from enum import Enum
from zoneinfo import ZoneInfo
from datetime import datetime
from pathlib import Path

# local import
from app.backend.tooling.setting.env import env

# constants class
class Constants(Enum):

    # connection string
    CONNECTION_STRING = f"postgresql://{env.db_username}:{env.db_password}@{env.db_host}:{env.db_port}/{env.db_name}"

    # static dir
    STATIC_DIR, STATIC_PATH, STATIC_NAME = '/frontend', 'app/frontend', 'static'

    # jinja2 template
    TEMPLATES = Path(__file__).resolve().parent.parent.parent.parent
    TEMPLATES_DIR = f'{TEMPLATES}/frontend/templates'
    HTML_ = Jinja2Templates(directory=TEMPLATES_DIR)

    # general
    CR_TIME_ZONE = datetime.now(ZoneInfo('America/Costa_Rica')).strftime("%d-%m-%Y | %-I:%M %p")

    # email
    EMAIL_SANTALUCIA_SENDER = "notificacionesferreteriasantal@gmail.com"

    # email subject
    SUBJECT_EMAIL_NEW_PASSWORD_CONFIRM = "Ferretería Santa Lucía. Confirmación de cambio de contraseña."
    SUBJECT_EMAIL_TEMP_PASSWORD_CONFIRM = "Ferretería Santa Lucía. Generación de contraseña temporal."

    # email links
    EMAIL_TO_LOGIN_SESSION = "http://127.0.0.1:8000/sesion/usuario"

    # labels
    LABEL_ADMIN = "Administrador"

    # redirecting
    URL_REDIRECT_TO_PASSWORD_RESTORE = "http://127.0.0.1:8000/sesion/restablecer"

    # tags
    AUTH, CRUD, SERV, TRANS = 'AUTH', 'CRUD', 'SERV' ,'TRANS'

    # endpoint
    OAUTH2_SCHEMA_URL = 'http://127.0.0.1:8000/sesion/usuario'
    ROOT = '/santalucia/api/v/'
    BASE = '/'
    URL_ID = '{id}'

    # auth endpoint
    AUTH_SESSION = '/sesion'
    AUTH_USER_LOGIN = '/usuario'
    AUTH_ADMIN_LOGIN = '/admin'
    AUTH_PASSWORD_RECOVER = '/recuperar'
    AUTH_PASSWORD_RESTORE = '/restablecer'

    # crud endpoint
    CRUD_BASE = '/mantenimientos'
    URL_SIGN_OUT = "/cerrar_sesion"

    CRUD_USER_BASE = '/usuarios'
    CRUD_USER_CREATE = f'{CRUD_USER_BASE}/registrar'
    CRUD_USER_UPDATE = f'{CRUD_USER_BASE}/actualizar/{URL_ID}'
    CRUD_USER_ENABLE = f'{CRUD_USER_BASE}/estado_usuario/{URL_ID}'
    CRUD_USER_POST = f'{CRUD_USER_BASE}/actualizar'
    CRUD_USER_ENABLE_POST = f'{CRUD_USER_BASE}/estado_usuario'

    CRUD_ROLE_BASE = '/roles'
    CRUD_ROLE_CREATE = f'{CRUD_ROLE_BASE}/registrar'
    CRUD_ROLE_UPDATE = f'{CRUD_ROLE_BASE}/actualizar/{URL_ID}'
    CRUD_ROLE_POST = f'{CRUD_ROLE_BASE}/actualizar'

    CRUD_DEDUCTION_BASE = '/deducciones'
    CRUD_DEDUCTION_CREATE = f'{CRUD_DEDUCTION_BASE}/registrar'
    CRUD_DEDUCTION_UPDATE = f'{CRUD_DEDUCTION_BASE}/actualizar/{URL_ID}'
    CRUD_DEDUCTION_POST = f'{CRUD_DEDUCTION_BASE}/actualizar'

    CRUD_DEPARTMENT_BASE = '/departamentos'
    CRUD_DEPARTMENT_CREATE = f'{CRUD_DEPARTMENT_BASE}/registrar'
    CRUD_DEPARTMENT_UPDATE = f'{CRUD_DEPARTMENT_BASE}/actualizar/{URL_ID}'
    CRUD_DEPARTMENT_POST = f'{CRUD_DEPARTMENT_BASE}/actualizar'

    CRUD_PAYMENT_DATE_BASE = '/fechas_pago'
    CRUD_PAYMENT_DATE_CREATE = f'{CRUD_PAYMENT_DATE_BASE}/registrar'
    CRUD_PAYMENT_DATE_UPDATE = f'{CRUD_PAYMENT_DATE_BASE}/actualizar/{URL_ID}'
    CRUD_PAYMENT_DATE_POST = f'{CRUD_PAYMENT_DATE_BASE}/actualizar'

    CRUD_QUESTION_BASE = '/pregunta_evaluativa'
    CRUD_QUESTION_CREATE = f'{CRUD_QUESTION_BASE}/registrar'
    CRUD_QUESTION_UPDATE = f'{CRUD_QUESTION_BASE}/actualizar/{URL_ID}'
    CRUD_QUESTION_POST = f'{CRUD_QUESTION_BASE}/actualizar'

    CRUD_SCHEDULE_BASE = '/jornadas'
    CRUD_SCHEDULE_CREATE = f'{CRUD_SCHEDULE_BASE}/registrar'
    CRUD_SCHEDULE_UPDATE = f'{CRUD_SCHEDULE_BASE}/actualizar/{URL_ID}'
    CRUD_SCHEDULE_POST = f'{CRUD_SCHEDULE_BASE}/actualizar'

    # profile
    PROFILE_BASE = '/perfil'
    PROFILE_ADDRESS = f'{PROFILE_BASE}/domicilio'
    PROFILE_PASSWORD = f'{PROFILE_BASE}/contrasena'
    PROFILE_VACATIONS = f'{PROFILE_BASE}/vacaciones'
    PROFILE_EXTRA_HOURS = f'{PROFILE_BASE}/horas_extra'

    # checkin
    CHECKIN_BASE = '/marcas'
    CHECKIN_REGISTER = '/registrar'

    # inability
    URL_INABILITY = '/incapacidades/ce'
    URL_INABILITY_CREATE = f'/registrar'
    URL_INABILITY_DETAIL = f'/detalles/{URL_ID}'
    URL_INABILITY_APPROVAL = f'/aprobaciones/{URL_ID}'
    URL_INABILITY_UPDATE_POST = '/actualizar'
    URL_INABILITY_PDF = f'/detalles/{URL_ID}/documento'

    # permission
    URL_PERMISSION = '/solicitudes/ce'
    URL_PERMISSION_CREATE_HOUR = '/registrar/horas'
    URL_PERMISSION_CREATE_VACATION = '/registrar/vacaciones'
    URL_PERMISSION_APPROVALS = '/aprobaciones'
    URL_PERMISSION_APPROVALS_UPDATE = f'/actualizar/{URL_ID}'
    URL_PERMISSION_APPROVALS_UPDATE_POST = f'/actualizar'

    # bonus
    URL_BONUS = '/aguinaldos/ce'
    URL_BONUS_DETAILS = f'/detalles/{URL_ID}'
    URL_BONUS_ADJUST = f'/ajustes/{URL_ID}'

    # payroll
    URL_PAYROLL = '/planillas/ce'
    URL_PAYROLL_DETAILS = f'/detalles/{URL_ID}'
    URL_PAYROLL_ADJUST = f'/ajustes/{URL_ID}'

    # settlement
    URL_SETTLEMENT = '/liquidaciones/ce'
    URL_SETTLEMENT_DETAILS = f'/detalles/{URL_ID}'
    URL_SETTLEMENT_ADJUST = f'/ajustes/{URL_ID}'

    # evaluation
    URL_EVALUATION = '/evaluaciones/ce'
    URL_EVALUATION_EMPLOYEE = '/empleados'
    URL_EVALUATION_SUPERVISOR = '/supervisores'
    URL_EVALUATION_ENABLE = '/habilitar'
    URL_EVALUATION_POST_RESULT = '/resultados'

    # reports endpoint
    TRANS_REPORT = '/reportes'

    # operation messages
    OPS_CRUD = {
        '_user': {
            '_create': 'El registro de usuario fue creado de forma exitosa.',
            '_update': 'El registro de usuario fue actualizado de forma exitosa.',
            '_inactive': 'El estado de usuario fue actualizado a Inactivo de forma exitosa.',
            '_active': 'El estado de usuario fue actualizado a Activo de forma exitosa.',
            '_exc': {
                '_identification': 'El número de identificación ingresado, ya se encuentra registrado en la base de datos.',
                '_email': 'El correo electrónico ingresado, ya se encuentra registrado en la base de datos.',
                '_phone': 'El número de teléfono ingresado, ya se encuentra registrado en la base de datos.',
                '_termination': 'La fecha de terminación no puede estar antes de la fecha de contratación.'
            }
        },
        '_role': {
            '_create': 'El registro de rol de usuario fue creado de forma exitosa.',
            '_fail': {
                "_fail": "Operacion de registro de datos fallida.",
                "_data_error": "El nombre de rol de usuario excede el número de caracteres permitidos.",
                "_ops_error": "Se presentan interrupciones a nivel de conexión de base de datos. Se está trabajando para solucionar el inconveniente.",
                "_orm_error": "Existen errores en el registro de la información. No se puede completar la operación."
            },
            '_update': {
                "_update": 'El registro de rol de usuario fue actualizado de forma exitosa.',
                "_except": 'La fecha de actualización no puede estar antes de la fecha de creación en los registros.'
            }
        },
        '_department': {
            '_create': 'El registro departamento fue creado de forma exitosa.',
            '_update': 'El registro departamento fue actualizado de forma exitosa.',
            '_fail': 'Existen errores en la información ingresada.',
            '_before_date': 'La fecha de actualización no puede estar antes de la fecha de creación en los registros.',
        },
        '_schedule': {
            '_create': 'El registro de jornada laboral fue creado de forma exitosa.',
            '_update': 'El registro de jornada laboral fue actualizado de forma exitosa.',
        },
        '_deduction': {
            '_create': 'El registro de deducción fue creado de forma exitosa.',
            '_update': 'El registro de deducción fue actualizado de forma exitosa.',
        },
        '_pay_date': {
            '_create': 'El registro de fecha de pago fue creado de forma exitosa.',
            '_update': 'El registro de fecha de pago fue actualizado de forma exitosa.',
        },
        '_question': {
            '_create': 'El registro de pregunta de evaluación fue creado de forma exitosa.',
            '_update': 'El registro de pregunta de evaluación fue actualizado de forma exitosa.',
        },
        '_report': {
            '_generate': 'El reporte fue generado de forma exitosa. Revisar su bandeja de entrada de correo electrónico.',
        },
        '_evaluation': {
            '_not_active': 'La evaluación se encuentra en estado inactiva.',
            '_enable': 'La evaluación ha sido habilidata de forma exitosa.',
            '_employee': 'La evaluación del empleado ha sido completada de forma exitosa.',
            '_supervisor': 'La evaluación del supervisor ha sido completada de forma exitosa.',
            "_ops_error": "Se presentan interrupciones a nivel de conexión de base de datos. Se está trabajando para solucionar el inconveniente.",
            "_orm_error": "Existen errores en el registro de la información. No se puede completar la operación."
        },
        '_inability': {
            '_fail': 'Existen errores en la información ingresada.',
            '_except': 'Ya existe una solicitud de incapacidad con el número de boleta ingresada.',
            '_create': 'La solicitud de incapacidad fue registrada exitosamente.',
            '_update': 'La solicitud de incapacidad fue actualizada exitosamente.'
        },
        '_permission': {
            '_vacations': {
                '_create': 'La solicitud de vacaciones fue registrada de forma exitosa.',
                '_update': 'La solicitud de vacaciones fue actualizada de forma exitosa.',
            },
            '_extrahour': {
                '_create': 'La solicitud de horas extra fue registrada de forma exitosa.',
                '_update': 'La solicitud de horas extra fue actualizada de forma exitosa.',
            },
            '_approval': 'La solicitud de permiso fue actualizada de forma exitosa.',
        },
        "_payroll": {
            "_update": "El registro de planilla ha sido ajustado exitosamente."
        },
        "_settlement": {
            "_update": "El registro de liquidación ha sido ajustado exitosamente."
        },
        "_year_bonus": {
            "_update": "El registro de aguinaldo ha sido ajustado exitosamente.",
            "_fail": 'Existen errores en la información ingresada. Por favor validar.',
            "_bonus_update": "La fecha de actualización no puede estar antes de la fecha de creación en los registros."
        },
        '_profile': {
            '_errors': 'Existen errores en la información ingresada. Por favor validar.',
            '_email': 'El correo electrónico ingresado, ya se encuentra registrado en la base de datos.',
            '_phone': 'El número de teléfono ingresado, ya se encuentra registrado en la base de datos.',
            '_password': 'La contraseña actual ingresada no coincide con los registros.',
            '_credentials': 'La contraseña de usuario se ha actualizado exitosamente.',
            '_info': 'La información de contacto de usuario se ha actualizado exitosamente.',
            '_checkin': 'El registro de marcas fue ingresado exitosamente.'
        },
        '_session': {
            '_temp_password': 'La contraseña temporal ingresada es incorrecta.',
            '_user': 'La contraseña de usuario fue establecida correctamente. Iniciar Sesión.',
            '_admin': 'La contraseña de administrador fue establecida correctamente. Iniciar Sesión.',
            '_as_admin': 'Su usuario no cuenta con los permisos para iniciar sesión como administrador.',
            '_as_user': 'Iniciar sesión como administrador.',
            '_inactive': 'Su usuario se encuentra en estado inactivo. Comunicarse con su jefatura para su activacion.',
            '_recover': {
                '_fail': 'No existe registros con el correo electrónico ingresado. No se puede restablecer la contraseña.',
                '_recover': 'Se ha enviado un enlace para restablecer su contraseña al correo electrónico ingresado.',
            },
            '_fail': {
                '_error': 'Existen errores en la información ingresada. Por favor validar.',
                '_ident': 'No existen registros con el número de identificación ingresado.',
                '_bad_login': 'Correo electronico y/o contraseña incorrectos.',
                '_ops_error': "Se presentan interrupciones a nivel de conexión de base de datos. Se está trabajando para solucionar el inconveniente.",
                '_orm_error': "Existen errores en el registro de la información. No se puede completar la operación.",
                '_user_as_inactive': 'El usuario seleccionado ya se encuentra en estado Inactivo.',
                '_user_as_active': 'El usuario seleccionado ya se encuentra en estado Activo.'
            },
            '_expire': 'Su sesión ha expirado, ingresar credenciales nuevamente.'
        },
    }

    # calender
    CALENDAR = {
        "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                   "Noviembre", "Diciembre"],
        "days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31]
    }

    # exception Integrity codes
    PG_CONSTRAINT_CODES = {
        "23505": "unique_violation",
        "23503": "foreign_key_violation",
        "23502": "not_null_violation",
        "23514": "check_violation",
        "23P01": "exclusion_violation",
    }
