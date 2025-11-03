# import
from fastapi.templating import Jinja2Templates
from enum import Enum
from zoneinfo import ZoneInfo
from datetime import datetime, date
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
    SUBJECT_EMAIL_TEMP_PASSWORD_FIRST_SIGNIN = "Ferretería Santa Lucía. Inicio de Sesión por primera vez."

    SUBJECT_EVALUATION_ENABLE_EMPLOYEE = "Ferretería Santa Lucía. Evaluación de empleado."
    SUBJECT_EVALUATION_ENABLE_SUPERVISOR = "Ferretería Santa Lucía. Evaluación de supervisor."

    SUBJECT_EVALUATION_RESULT_EMPLOYEE = "Ferretería Santa Lucía. Resultado Evaluación de empleado."
    SUBJECT_EVALUATION_RESULT_SUPERVISOR = "Ferretería Santa Lucía. Resultado Evaluación de supervisor."

    SUBJECT_PERMISSION_EXTRA_HOURS_REQUEST = "Ferretería Santa Lucía. Solicitud de Permiso. Horas Extra."
    SUBJECT_PERMISSION_EXTRA_HOURS_UPDATE_REQUEST = "Ferretería Santa Lucía. Actualización de Solicitud de Permiso. Horas Extra."

    SUBJECT_PERMISSION_VACATIONS_REQUEST = "Ferretería Santa Lucía. Solicitud de Permiso. Vacaciones."
    SUBJECT_PERMISSION_VACATIONS_UPDATE_REQUEST = "Ferretería Santa Lucía. Actualización de Solicitud de Permiso. Vacaciones."

    SUBJECT_INABILITY_REQUEST = "Ferretería Santa Lucía. Solicitud de Incapacidad."
    SUBJECT_INABILITY_UPDATE_REQUEST = "Ferretería Santa Lucía. Actualización de Solicitud de Incapacidad."

    SUBJECT_REPORT_REQUEST = "Ferretería Santa Lucía. Solicitud de Reporte."
    SUBJECT_PDF_PAYROLL_STATEMENT = "Ferretería Santa Lucía. Comprobante de Planilla."

    # email links
    EMAIL_TO_LOGIN_SESSION = "http://127.0.0.1:8000/sesion/usuario"

    # labels
    LABEL_ADMIN = "Administrador"

    # evaluation types
    EMPLOYEE_EVALUATION = "Rendimiento Empleado"
    SUPERVISOR_EVALUATION = "Evaluación Liderazgo"

    # vacations queue
    VACATIONS_QUEUE = 0

    # redirecting
    URL_REDIRECT_TO_PASSWORD_RESTORE = "http://127.0.0.1:8000/sesion/restablecer"
    URL_REDIRECT_TO_EVALUATION_MAIN = "http://127.0.0.1:8000/evaluaciones/ce/"

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
    PROFILE_BASE = '/perfil/ce'
    PROFILE_ADDRESS = f'{PROFILE_BASE}/domicilio'
    PROFILE_PASSWORD = f'{PROFILE_BASE}/contrasena'
    PROFILE_VACATIONS = f'{PROFILE_BASE}/vacaciones'
    PROFILE_EXTRA_HOURS = f'{PROFILE_BASE}/horas_extra'

    # checkin
    CHECKIN_BASE = '/marcas/ce'
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
    URL_PERMISSION_EXTRA_HOURS_MAIN = '/horas_extra'
    URL_PERMISSION_CREATE_EXTRA_HOURS = '/registrar/horas'
    URL_PERMISSION_UPDATE_EXTRA_HOURS = f'/actualizar/horas/{URL_ID}'
    URL_PERMISSION_UPDATE_EXTRA_HOURS_POST = '/actualizar/horas'

    URL_PERMISSION_VACATION_MAIN = '/vacaciones'
    URL_PERMISSION_CREATE_VACATION = '/registrar/vacaciones'
    URL_PERMISSION_UPDATE_VACATION = f'/actualizar/vacaciones/{URL_ID}'
    URL_PERMISSION_UPDATE_VACATION_POST = '/actualizar/vacaciones'

    # bonus
    URL_BONUS = '/aguinaldos/ce'
    URL_BONUS_GENERATE = "/generar_cuotas"
    URL_BONUS_DETAILS = f'/detalles/{URL_ID}'
    URL_BONUS_DETAILS_PDF = f'/detalles/{URL_ID}/aguinaldo'
    URL_BONUS_ADJUST = f'/ajustes/{URL_ID}'
    URL_BONUS_ADJUST_POST = '/ajustes'

    # payroll
    URL_PAYROLL = '/planillas/ce'
    URL_PAYROLL_GENERATE = "/generar_planillas"
    URL_PAYROLL_DETAILS = f'/detalles_planilla/{URL_ID}'
    URL_PAYROLL_DETAILS_PDF = f'/detalles/{URL_ID}/planilla'
    URL_PAYROLL_ADJUST = f'/ajustes_planilla/{URL_ID}'
    URL_PAYROLL_ADJUST_POST = '/ajustes_planilla'

    # settlement
    URL_SETTLEMENT = '/liquidaciones/ce'
    URL_SETTLEMENT_DETAILS = f'/detalles/{URL_ID}'
    URL_SETTLEMENT_DETAILS_PDF = f'/detalles/{URL_ID}/liquidacion'
    URL_SETTLEMENT_ADJUST = f'/ajustes/{URL_ID}'
    URL_SETTLEMENT_ADJUST_POST = '/ajustes'
    # settlement to redirect
    URL_SETTLEMENT_TO_REDIRECT = "http://127.0.0.1:8000/liquidaciones/ce/detalles"

    # evaluation
    URL_EVALUATION = '/evaluaciones/ce'
    URL_EVALUATION_EMPLOYEE = '/empleados'
    URL_EVALUATION_SUPERVISOR = '/supervisores'
    URL_EVALUATION_ENABLE = '/habilitar'
    URL_EVALUATION_POST_RESULT = '/resultados'

    # reports endpoint
    TRANS_REPORT = '/reportes/ce'

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
            "_update": "Se han generado los registros de planilla de manera exitosa.",
            "_period": "El periodo para la siguiente planilla aún no se ha completado para su generación."
        },
        "_settlement": {
            "_update": "El registro de liquidación ha sido ajustado exitosamente.",
            "_download": "Descarga de archivo exitosa."
        },
        "_bonus": {
            "_update": "El registro de aguinaldo ha sido ajustado exitosamente.",
            "_fail": 'Existen errores en la información ingresada. Por favor validar.',
            "_download": "Descarga de archivo exitosa.",
            "_not_start": "La cuota de aguinaldo solo puede ser generada hasta el 30 del mes.",
            "_duplicate": "Ya existe un registro de cuota para el periodo seleccionado."
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
                '_user_as_active': 'El usuario seleccionado ya se encuentra en estado Activo.',
                '_available': 'No cuenta con las vacaciones disponibles para procesar su solicitud.'
            },
            '_expire': 'Su sesión ha expirado, ingresar credenciales nuevamente.'
        }
    }

    # calender
    CALENDAR = {
        "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                   "Noviembre", "Diciembre"],
        "days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31]
    }

    # cr current year
    CR_YEAR = datetime.now(ZoneInfo("America/Costa_Rica")).year

    # holiday calendar
    HOLIDAY_CALENDAR = {
        "new_year": date(date.today().year, 1, 1),
        "juan_santamaria": date(date.today().year, 4, 11),
        "holy_thurs": date(date.today().year, 4, 17),
        "holy_friday": date(date.today().year, 4, 18),
        "labor_day": date(date.today().year, 5, 1),
        "nicoya": date(date.today().year, 7, 25),
        "mother_day": date(date.today().year, 8, 15),
        "independence": date(date.today().year, 9, 15),
        "christmas": date(date.today().year, 12, 25),
    }

    # reports name fields
    HEADERS = {
        'registro_marcas': {
            '_id': 'Cod', '_start_hour': 'Hora entrada', '_end_hour': 'Hora salida',
            '_hours': 'Horas', '_status': 'Estado registro', '_log_date': 'Fecha registro',
            '_subj_ident': 'Identificacion', '_subj_name': 'Nombre', '_subj_lastname': 'Apellido',
            '_subj_lastname2': 'Segundo apellido', '_subj_email': 'Correo electronico', '_subj_dept_name': 'Departamento',
            '_subj_role_name': 'Puesto', '_subj_role_type': 'Tipo de rol', '_apr_ident': 'Identificacion jefatura',
            '_apr_name': 'Nombre jefatura', '_apr_lastname': 'Apellido jefatura',
            '_apr_lastname2': 'Segundo apellido jefatura', 'Correo electronico jefatura': '_apr_email',
            '_apr_dept_name': 'Departamento jefatura', '_apr_role_name': 'Puesto jefatura',
            '_apr_role_type': 'Tipo de rol'
        },
        'incapacidades': {
            '_id': 'Cod', '_date_start': 'Fecha salida', '_date_return': 'Fecha retorno',
            '_details': 'Detalles', '_doc_number': 'Número boleta', '_status': 'Estado incapacidad',
            '_subj_ident': 'Identificacion', '_subj_name': 'Nombre', '_subj_lastname': 'Apellido',
            '_subj_lastname2': 'Segundo apellido', '_subj_email': 'Correo electronico', '_subj_dept_name': 'Departamento',
            '_subj_role_name': 'Puesto', '_subj_role_type': 'Tipo de rol', '_apr_ident': 'Identificacion jefatura',
            '_apr_name': 'Nombre jefatura', '_apr_lastname': 'Apellido jefatura',
            '_apr_lastname2': 'Segundo apellido jefatura', 'Correo electronico jefatura': '_apr_email',
            '_apr_dept_name': 'Departamento jefatura', '_apr_role_name': 'Puesto jefatura',
            '_apr_role_type': 'Tipo de rol'
        },
        'liquidaciones': {
            '_id': 'Cod', '_total_amount': 'Monto total', '_status': 'Estado Liquidación',
            '_type': 'Tipo liquidación', '_details': 'Detalles',
            '_subj_ident': 'Identificacion', '_subj_name': 'Nombre', '_subj_lastname': 'Apellido',
            '_subj_lastname2': 'Segundo apellido', '_subj_email': 'Correo electronico',
            '_subj_dept_name': 'Departamento',
            '_subj_role_name': 'Puesto', '_subj_role_type': 'Tipo de rol', '_apr_ident': 'Identificacion jefatura',
            '_apr_name': 'Nombre jefatura', '_apr_lastname': 'Apellido jefatura',
            '_apr_lastname2': 'Segundo apellido jefatura', 'Correo electronico jefatura': '_apr_email',
            '_apr_dept_name': 'Departamento jefatura', '_apr_role_name': 'Puesto jefatura',
            '_apr_role_type': 'Tipo de rol'
        },
        'registro_horas_extra': {
            '_id': 'Cod', '_hours': 'Horas', '_date_request': 'Fecha solicitud',
            '_type': 'Tipo solicitud', '_status': 'Estado solicitud',
            '_subj_ident': 'Identificacion', '_subj_name': 'Nombre', '_subj_lastname': 'Apellido',
            '_subj_lastname2': 'Segundo apellido', '_subj_email': 'Correo electronico',
            '_subj_dept_name': 'Departamento',
            '_subj_role_name': 'Puesto', '_subj_role_type': 'Tipo de rol', '_apr_ident': 'Identificacion jefatura',
            '_apr_name': 'Nombre jefatura', '_apr_lastname': 'Apellido jefatura',
            '_apr_lastname2': 'Segundo apellido jefatura', 'Correo electronico jefatura': '_apr_email',
            '_apr_dept_name': 'Departamento jefatura', '_apr_role_name': 'Puesto jefatura',
            '_apr_role_type': 'Tipo de rol'
        },
        'aguinaldos': {
            '_id': 'Cod', '_total_amount': 'Monto total', '_month_amount': 'Monto mensual',
            '_month': 'Mes',
            '_subj_ident': 'Identificacion', '_subj_name': 'Nombre', '_subj_lastname': 'Apellido',
            '_subj_lastname2': 'Segundo apellido', '_subj_email': 'Correo electronico',
            '_subj_dept_name': 'Departamento',
            '_subj_role_name': 'Puesto', '_subj_role_type': 'Tipo de rol', '_apr_ident': 'Identificacion jefatura',
            '_apr_name': 'Nombre jefatura', '_apr_lastname': 'Apellido jefatura',
            '_apr_lastname2': 'Segundo apellido jefatura', 'Correo electronico jefatura': '_apr_email',
            '_apr_dept_name': 'Departamento jefatura', '_apr_role_name': 'Puesto jefatura',
            '_apr_role_type': 'Tipo de rol'
        },
        'registro_vacaciones': {
            '_id': 'Cod', '_days': 'Días', '_date_start': 'Fecha de inicio',
            '_date_return': 'Fecha retorno', '_type': 'Tipo solicitud', '_status': 'Estado solicitud',
            '_subj_ident': 'Identificacion', '_subj_name': 'Nombre', '_subj_lastname': 'Apellido',
            '_subj_lastname2': 'Segundo apellido', '_subj_email': 'Correo electronico',
            '_subj_dept_name': 'Departamento',
            '_subj_role_name': 'Puesto', '_subj_role_type': 'Tipo de rol', '_apr_ident': 'Identificacion jefatura',
            '_apr_name': 'Nombre jefatura', '_apr_lastname': 'Apellido jefatura',
            '_apr_lastname2': 'Segundo apellido jefatura', 'Correo electronico jefatura': '_apr_email',
            '_apr_dept_name': 'Departamento jefatura', '_apr_role_name': 'Puesto jefatura',
            '_apr_role_type': 'Tipo de rol'
        },
    }

    # settlement query context
    SETTLE_QUERY_CONTEXT = {
        'name': None, 'lastname': None, 'lastname2': None, 'current_date': None, 'identification': None,
        'settlement_id': None, 'termination_date': None, 'jf_name': None, 'jf_lastname': None, 'jf_lastname2': None,
        'total_amount': None, 'payroll_amount': None, 'cesantia_amount': None, 'vacations_amount': None,
        'bonus_amount': None, 'other_amount': None, 'settlement_details': None
    }

    # bonus query context
    BONUS_QUERY_CONTEXT = {
        'name': None, 'lastname': None, 'lastname2': None, 'current_date': None, 'identification': None,
        'bonus_id': None, 'hire_date': None, 'jf_name': None, 'jf_lastname': None, 'jf_lastname2': None,
        'gross_amount': None, 'total_amount': None, "month_amount": None, 'year': None, 'month': None,
        'details': None
    }

    # payroll query context
    PAYROLL_QUERY_CONTEXT = {
        'name': None, 'lastname': None, 'lastname2': None, 'current_date': None, 'identification': None,
        'payroll_id': None, 'payment_date': None, 'payment_date2': None, 'frecuency': None, 'jf_name': None,
        'jf_lastname': None, 'jf_lastname2': None, 'gross_amount': None, 'net_amount': None, 'rent_tax': None,
        'ccss_ivm': None, 'ccss_eme': None, 'rop': None, 'vacations': None, 'extra_hours': None, 'holidays': None,
        'debt': None, 'support': None, 'others': None, 'payment_details': None
    }

    # payroll periods
    PAYROLL_PERIODS = {
        "Agosto Periodo 15": [date(date.today().year, 7, 31), date(date.today().year, 8, 15)],
        "Agosto Periodo 30": [date(date.today().year, 8, 16), date(date.today().year, 8, 30)],
        "Septiembre Periodo 15": [date(date.today().year, 9, 1), date(date.today().year, 9, 15)],
        "Septiembre Periodo 30": [date(date.today().year, 9, 16), date(date.today().year, 9, 30)],
        "Octubre Periodo 15": [date(date.today().year, 10, 1), date(date.today().year, 10, 15)],
        "Octubre Periodo 30": [date(date.today().year, 10, 16), date(date.today().year, 10, 31)],
        "Noviembre Periodo 15": [date(date.today().year, 11, 1), date(date.today().year, 11, 15)],
        "Noviembre Periodo 30": [date(date.today().year, 11, 16), date(date.today().year, 11, 30)],
        "Diciembre Periodo 15": [date(date.today().year, 12, 1), date(date.today().year, 12, 15)],
        "Diciembre Periodo 30": [date(date.today().year, 12, 16), date(date.today().year, 12, 31)],
    }

    # bonus periods
    BONUS_PERIODS = {
        "Periodo Agosto": [date(date.today().year, 8, 1), date(date.today().year, 8, 30)],
        "Periodo Septiembre": [date(date.today().year, 9, 1), date(date.today().year, 9, 30)],
        "Periodo Octubre": [date(date.today().year, 10, 1), date(date.today().year, 10, 30)],
        "Periodo Noviembre": [date(date.today().year, 11, 1), date(date.today().year, 11, 30)],
        "Periodo Diciembre": [date(date.today().year, 12, 1), date(date.today().year, 12, 30)],
    }

    # month catalog
    MONTHS_CAT = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
