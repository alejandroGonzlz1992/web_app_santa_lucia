// import

/* global static dict class for static values */
export const Static = {

    /* general */
    MIN_ROLE_NAME_LENGTH: 5,
    MIN_DEPARTMENT_NAME_LENGTH: 5,
    MIN_DEDUCTION_NAME_LENGTH: 5,
    IDENTIFICATION_LENGTH: 9,
    NAME_LASTNAME_LASTNAME2_LENGTH: 4,
    FEEDBACK_MIN_LENGTH: 15,
    UNDERAGE: 18,
    MIN_INABILITY_NUMBER: 4,
    RETIRE_AGE_MAN: 65,
    RETIRE_AGE_WOMAN: 63,
    MAX_CHILDREN: 12,
    PASSWORD_MIN_LENGTH: 9,
    PHONE_LENGTH: 8,
    GROSS_INCOME_MIN: 250000,
    GROSS_INCOME_MAX: 3000000,
    DIURNO_MAX_HOURS: 8,
    NOCTURNO_MAX_HOURS: 6,
    MAX_EXTRA_HOURS: 5,
    MIXTO_MAX_HOUR: 7,
    MIN_PERCENTAGE: 1,
    POSTAL_CODE_LENGTH: 5,
    MAX_PERCENTAGE: 25,
    EVALUATION_QUESTION_LENGTH: 10,
    ALLOW_FILE_EXT: ["png", "jpg", "jpeg", "pdf"],
    ADDRESS_LENGTH: 10,
    MILLISECONDS_PER_DAY: 86_400_000,
    REGEX_RADIO_BUTTONS: /^ratings\[(\d+)\]$/,

    TIME_12_HOUR_FORMAT: /^(\d{1,2}):(\d{2})\s?(am|pm)$/i,

    ENABLE_USER_RESTORE_PASSWORD: [
        ["#id_temp_password_field", "#id_new_password_field", "#id_confirm_password_field"],
        ["#id_password_temp_bttn", "#id_new_password_bttn", "#id_confirm_password_bttn"]
    ],

    ENABLE_USER_PROFILE_PASSWORD: [
        ["#id_user_password_field", "#id_new_password_field", "#id_confirm_password_field"],
        ["#id_user_password_bttn", "#id_new_password_bttn", "#id_confirm_password_bttn"]
    ],

    /* regex Dictionary */
    REGEX: {
        "only_numbers": /^\d+$/,
        "amount_format": /^\d+(\.\d+)?$/,
        "only_letters": /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/,
        "email_format": /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        "address": /^(?!\d+$)[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,]+$/,
        "percentage": /^\d+(\.\d{1,3})?$/,
        "question": /^[a-zA-Z0-9\s¿?.]+$/,
        "numbers_decimals": /^\d+(\.\d+)?$/,
        "password": /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]+$/,
        "evaluation": /^(?=.*[A-Za-zÁÉÍÓÚáéíóúÑñ])[A-Za-zÁÉÍÓÚáéíóúÑñ0-9¿?,.\s]+$/
    },

    /* Form Fields -> Contains a dict of form field div names, errors, and messages */

    // USER ROLES
    USER_ROLE_FORM_DICT: {
        "role_name": {
            "div_id": {
                "blank": "id_role_name_blank_field_error",
                "chars": "id_role_name_chars_field_error",
                "length": "id_role_name_length_field_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar letras únicamente.",
                "length": "Nombre de rol debe tener mínimo cinco caracteres."
            }
        },
        "role_type": {
            "div_id": {
                "status": "id_role_type_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "role_department": {
            "div_id": {
                "status": "id_role_department_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "role_schedule": {
            "div_id": {
                "status": "id_role_schedule_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "role_create_date": {
            "div_id": {
                "blank": "id_role_create_date_blank_field_error",
                "before": "id_role_create_date_before_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de registro no puede estar antes de la fecha actual.",
            }
        }
    },

    USER_ROLE_BLANK_FIELDS: [
        "role_name", "role_type", "role_department", "role_schedule", "role_create_date",
    ],

    // USER
    USER_FORM_DICT: {
        "user_identification": {
            "div_id": {
                "blank": "id_identification_blank_field_error",
                "chars": "id_identification_chars_field_error",
                "length": "id_identification_length_field_error"
            },
            "text": {
                "blank": "Campo obligatorio.",
                "length": "El número de identificación debe contener nueve dígitos.",
                "chars": "El número de identificación solamente pueden ser números.",
            }
        },
        "user_name": {
            "div_id": {
                "blank": "id_name_blank_field_error",
                "chars": "id_name_chars_field_error",
                "length": "id_name_length_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "length": "El nombre de usuario debe tener mínimo cuatro caracteres.",
                "chars": "El nombre de usuario solamente pueden ser letras.",
            }
        },
        "user_lastname": {
            "div_id": {
                "blank": "id_lastname_blank_field_error",
                "chars": "id_lastname_chars_field_error",
                "length": "id_lastname_length_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "length": "El apellido de usuario debe tener mínimo cuatro caracteres.",
                "chars": "El apellido de usuario solamente pueden ser letras.",
            }
        },
        "user_lastname2": {
            "div_id": {
                "blank": "id_lastname2_blank_field_error",
                "chars": "id_lastname2_chars_field_error",
                "length": "id_lastname2_length_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "length": "El segundo apellido de usuario debe tener mínimo cuatro caracteres.",
                "chars": "El segundo apellido de usuario solamente pueden ser letras.",
            }
        },
        "user_birthday": {
            "div_id": {
                "blank": "id_birthday_date_blank_field_error",
                "under": "id_birthday_date_underage_field_error",
                "man": "id_birthday_date_overage_man_field_error",
                "woman": "id_birthday_date_overage_woman_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "under": "No se permite el registro de menores de edad.",
                "man": "La edad máxima de registro es de 65 años para hombres.",
                "woman": "La edad máxima de registro es de 63 años para mujeres.",
            }
        },
        "user_gender": {
            "div_id": {
                "status": "id_user_gender_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "user_marital_status": {
            "div_id": {
                "status": "id_user_marital_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "user_children": {
            "div_id": {
                "blank": "id_user_children_blank_field_error",
                "chars": "id_user_children_chars_field_error",
                "max": "id_user_children_max_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "chars": "Ingresar números únicamente.",
                "max": "La cantidad máxima de hijos es de doce.",
            }
        },
        "user_email": {
            "div_id": {
                "blank": "id_email_blank_field_error",
                "format": "id_email_format_field_error"
            },
            "text": {
                "blank": "Campo obligatorio.",
                "format": "Formato incorrecto de correo electrónico.",
            }
        },
        "user_phone": {
            "div_id": {
                "blank": "id_phone_blank_field_error",
                "chars": "id_phone_chars_field_error",
                "length": "id_phone_length_field_error"
            },
            "text": {
                "blank": "Campo obligatorio.",
                "chars": "Ingresar números únicamente.",
                "length": "El número telefónico debe tener nueve dígitos únicamente."
            }
        },
        "user_role": {
            "div_id": {
                "status": "id_user_role_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "user_gross_income": {
            "div_id": {
                "blank": "id_gross_income_blank_field_error",
                "chars": "id_gross_income_chars_field_error",
                "min": "id_gross_income_min_field_error",
                "max": "id_gross_income_max_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "chars": "Ingresar números únicamente.",
                "min": "El ingreso bruto mínimo es de 250.000 CRC.",
                "max": "El ingreso bruto máximo es de 3.000.000 CRC.",
            }
        },
        "user_create_date": {
            "div_id": {
                "blank": "id_user_create_date_blank_field_error",
                "before": "id_user_create_date_before_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "before": "La fecha de registro no puede estar antes de la fecha actual.",
            }
        },
        "user_approval": {
            "div_id": {
                "status": "id_user_approval_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
    },

    USER_BLANK_FIELDS: [
        "user_identification", "user_name", "user_lastname", "user_lastname2", "user_birthday", "user_gender",
        "user_marital_status", "user_children", "user_email", "user_phone", "user_role", "user_gross_income",
        "user_create_date", "user_approval"
    ],

    // USER STATUS
    USER_STATUS_FORM_DICT: {
        "user_status": {
            "div_id": {
                "status": "id_user_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú."
            }
        },
        "termination_date": {
            "div_id": {
                "blank": "id_termination_create_date_blank_field_error",
                "before": "id_termination_date_before_current_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de terminación no puede estar antes de la fecha actual.",
            }
        }
    },

    USER_STATUS_BLANK_FIELDS: ["user_status", "termination_date"],

    // DEDUCTIONS
    DEDUCTIONS_FORM_DICT: {
        "deduction_name": {
            "div_id": {
                "blank": "id_deduction_blank_field_error",
                "length": "id_deduction_length_field_error",
                "chars": "id_deduction_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "length": "Nombre de la deducción debe tener mínimo cinco caracteres.",
                "chars": "Ingresar letras únicamente."
            }
        },
        "deduction_percentage": {
            "div_id": {
                "blank": "id_percentage_blank_field_error",
                "format": "id_percentage_chars_field_error",
                "min": "id_percentage_min_field_error",
                "max": "id_percentage_max_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "format": "Formato de porcentaje incorrecto.",
                "min": "El porcentaje mínimo de deducción es de 1%.",
                "max": "El porcentaje máximo de deducción es de 25%."
            }
        },
        "deduction_create_date": {
            "div_id": {
                "blank": "id_deduction_create_date_blank_field_error",
                "before": "id_deduction_create_date_before_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de registro no puede estar antes de la fecha actual.",
            }
        }

    },

    DEDUCTIONS_BLANK_FIELDS: ["deduction_name", "deduction_percentage", "deduction_create_date"],

    // DEPARTMENTS
    DEPARTMENTS_FORM_DICT: {
        "department_name": {
            "div_id": {
                "blank": "id_department_blank_field_error",
                "chars": "id_department_chars_field_error",
                "length": "id_department_length_field_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar letras únicamente.",
                "length": "Nombre del departamento debe tener mínimo cinco caracteres."
            }
        },
        "department_status": {
            "div_id": {
                "status": "id_department_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "department_create_date": {
            "div_id": {
                "blank": "id_department_create_date_blank_field_error",
                "before": "id_department_create_date_before_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de registro no puede estar antes de la fecha actual.",
            }
        },
    },

    DEPARTMENTS_BLANK_FIELDS: ["department_name", "department_status", "department_create_date"],

    // PAYMENT DATE
    PAYMENT_DATE_FORM_DICT: {
        "payment_frecuency": {
            "div_id": {
                "status": "id_frecuency_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "payment_date": {
            "div_id": {
                "blank": "id_payment_blank_field_error",
                "after": "id_payment_after_payment2_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "after": "La primera fecha de pago no puede ser después de la segunda fecha de pago.",
            }
        },
        "payment2_date": {
            "div_id": {
                "blank": "id_payment2_blank_field_error",
                "before": "id_payment2_before_payment_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La segunda fecha de pago no puede ser antes de la primera fecha de pago.",
            }
        },
    },

    PAYMENT_DATE_BLANK_FIELDS: ["payment_frecuency", "payment_date", "payment2_date"],

    // QUESTIONS
    QUESTIONS_FORM_DICT: {
        "evaluation_type": {
            "div_id": {
                "status": "id_evaluation_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "evaluation_question": {
            "div_id": {
                "blank": "id_evaluation_question_blank_field_error",
                "chars": "id_evaluation_question_chars_field_error",
                "length": "id_evaluation_question_length_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "La pregunta evaluativa no debe contener caracteres especiales.",
                "length": "La pregunta evaluativa debe contener mínimo 10 caracteres.",
            }
        },
    },

    QUESTIONS_BLANK_FIELDS: ["evaluation_type", "evaluation_question"],

    // SCHEDULE
    SCHEDULE_FORM_DICT: {
        "schedule_type": {
            "div_id": {
                "status": "id_schedule_type_not_selected_field_error",
                "diurna": "id_diurna_hours_exceeded_field_error",
                "nocturna": "id_nocturna_hours_exceeded_field_error",
                "mixta": "id_mixta_hours_exceeded_field_error"
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
                "diurna": "La jornada laboral diurna no puede exceder las 8 horas.",
                "nocturna": "La jornada laboral nocturna no puede exceder las 6 horas.",
                "mixta": "La jornada laboral mixta no puede exceder las 7 horas."
            }
        },
        "schedule_start_time": {
            "div_id": {
                "blank": "id_start_time_blank_field_error",
                "after": "id_start_time_after_end_time_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "after": "La hora de inicio no puede estar después de la hora de finalización."
            }
        },
        "schedule_end_time": {
            "div_id": {
                "blank": "id_end_time_blank_field_error",
                "before": "id_end_time_before_end_time_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La hora de finalización no puede estar antes de la hora de inicio."
            }
        },
        "schedule_create_date": {
            "div_id": {
                "blank": "id_schedule_create_date_blank_field_error",
                "before": "id_schedule_create_date_before_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de registro no puede estar antes de la fecha actual."
            }
        },
    },

    SCHEDULE_BLANK_FIELDS: ["schedule_type", "schedule_start_time", "schedule_end_time", "schedule_create_date"],

    // REPORT
    REPORT_FORM_DICT: {
        "report_name_field": {
            "div_id": {
                "status": "id_report_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "start_date_field": {
            "div_id": {
                "blank": "id_start_date_blank_field_error",
                "after": "id_start_date_after_current_date_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "after": "La fecha de inicio de reporte no puede estar después de la fecha actual."
            }
        },
        "end_date_field": {
            "div_id": {
                "blank": "id_end_date_blank_field_error",
                "before": "id_end_date_before_start_date_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de finalización de reporte no puede estar antes de la fecha de inicio."
            }
        },
        "report_deliver": {
            "div_id": {
                "status": "id_download_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
    },

    REPORT_BLANK_FIELDS: ["report_name_field", "start_date_field", "end_date_field", "report_deliver"],

    // EVALUATION
    EVALUATION_FORM_DICT: {
        "evaluation_user_name_field": {
            "div_id": {
                "status": "id_status_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "question_item_field": {
            "div_id": {
                "check": "id_error_question_item_blank_field_error",
            },
            "text": {
                "check": "Debe seleccionar una de las opciones para evaluar la pregunta. (De 1 a 5)",
            }
        },
        "evaluation_detail": {
            "div_id": {
                "blank": "id_feedback_blank_field_error",
                "chars": "id_feedback_not_special_chars_field_error",
                "length": "id_feedback_length_field_error",
            },
            "text": {
                "blank": "Campo obligatorio.",
                "chars": "No se permiten caracteres especiales.",
                "length": "El detalle de incapacidad debe tener mínimo 10 caracteres.",
            }
        }
    },

    EVALUATION_BLANK_FIELDS: ["evaluation_user_name_field", "evaluation_detail"],

    // EVALUATION ENABLE
    EVALUATION_ENABLE_FORM_DICT: {
        "evaluation_type": {
            "div_id": {
                "status": "id_status_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "confirm_switch_field": {
            "div_id": {
                "confirm": "id_record_not_confirm_field_error",
            },
            "text": {
                "confirm": "Campo obligatorio.",
            }
        },
    },

    EVALUATION_ENABLE_BLANK_FIELDS: ["evaluation_type", "confirm_switch_field"],

    // INABILITY
    INABILITY_FORM_DICT: {
        "start_date": {
            "div_id": {
                "blank": "id_start_date_blank_field",
                "on_saturday": "id_start_date_on_saturday_field",
                "on_sunday": "id_start_date_on_sunday_field"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "on_saturday": "La fecha de inicio de incapacidad no puede ser un sábado.",
                "on_sunday": "La fecha de inicio de incapacidad no puede ser un domingo.",
            }
        },
        "return_date": {
            "div_id": {
                "blank": "id_return_date_blank_field",
                "before": "id_return_date_before_start_date",
                "on_saturday": "id_return_date_on_saturday_field",
                "on_sunday": "id_return_date_on_sunday_field"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de retorno no puede estar antes de la fecha de inicio.",
                "on_saturday": "La fecha de retorno de incapacidad no puede ser un sábado.",
                "on_sunday": "La fecha de retorno de incapacidad no puede ser un domingo.",
            }
        },
        "inability_number": {
            "div_id": {
                "blank": "id_inability_number_blank_field",
                "length": "id_inability_number_length_field",
                "chars": "id_inability_number_chars_field",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "length": "El número de boleta debe tener mínimo 4 caracteres.",
                "chars": "El número de boleta debe contener números únicamente",
            }
        },
        "inability_file": {
            "div_id": {
                "blank": "id_file_blank_field_error",
                "format": "id_file_format_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "format": "Formato incorrecto de documento. Adjuntar .png, .jpg, jpeg, .pdf",
            }
        },
        "inability_detail": {
            "div_id": {
                "blank": "id_detail_blank_field_error",
                "length": "id_detail_length_error",
                "chars": "id_detail_special_chars_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "length": "El detalle de incapacidad debe tener mínimo 10 caracteres.",
                "chars": "No se permiten caracteres especiales.",
            }
        }
    },

    INABILITY_BLANK_FIELDS: ["start_date", "return_date", "inability_number", "inability_file", "inability_detail"],

    // INABILITY ENABLE
    INABILITY_ENABLE_FORM_DICT: {
        "inability_status_field": {
            "div_id": {
                "status": "id_status_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "delete_switch_field": {
            "div_id": {
                "confirm": "id_confirm_not_selected_field_error"
            },
            "text": {
                "confirm": "Debe seleccionar la opción de Confirmar."
            }
        },
    },

    INABILITY_ENABLE_BLANK_FIELDS: ["inability_status_field", "delete_switch_field"],

    // PERMISSION EXTRA HOUR
    PERMISSION_EXTRA_HOUR_FORM_DICT: {
        "hour_date_field": {
            "div_id": {
                "blank": "id_hour_date_blank_field",
                "before": "id_hour_date_before_current_date_field",
                "sunday": "id_hour_date_on_sunday_date_field"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de solicitud de hora extra no puede estar antes de la fecha actual.",
                "sunday": "La fecha de solicitud de hora extra no puede ser los Domingos."
            }
        },
        "hour_schedule_type": {
            "div_id": {
                "status": "id_hour_schedule_type_selected_field",
            },
            "text": {
                "status": "Se debe seleccionar una jornada laboral.",
            }
        },
        "hour_quantity_field": {
            "div_id": {
                "blank": "id_hours_blank_error_field",
                "chars": "id_hours_not_numbers_error_field",
                "exceed": "id_hours_exceed_error_field",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente.",
                "exceed": "Cantidad de horas excede el máximo de 5 horas diarias.",
            }
        },
    },

    PERMISSION_EXTRA_HOUR_BLANK_FIELDS: ["hour_date_field", "hour_schedule_type", "hour_quantity_field"],

    // PERMISSION VACATION
    PERMISSION_VACATION_FORM_DICT: {
        "start_date_field": {
            "div_id": {
                "blank": "id_start_date_blank_field",
                "current": "id_start_date_before_current_date_field",
                "on_saturday": "id_start_date_on_saturday_field",
                "on_sunday": "id_start_date_on_sunday_field",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "current": "La fecha de inicio no puede estar antes de la fecha actual.",
                "on_saturday": "La fecha de inicio de vacación no puede ser un sábado.",
                "on_sunday": "La fecha de inicio de vacación no puede ser un domingo.",
            }
        },
        "end_date_field": {
            "div_id": {
                "blank": "id_return_date_blank_field",
                "before": "id_return_date_before_start_date_field",
                "on_saturday": "id_return_date_on_saturday_field",
                "on_sunday": "id_return_date_on_sunday_field",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de retorno no puede estar antes de la fecha de inicio.",
                "on_saturday": "La fecha de retorno de vacación no puede ser un sábado.",
                "on_sunday": "La fecha de retorno de vacación no puede ser un domingo.",
            }
        },
    },

    PERMISSION_VACATION_BLANK_FIELDS: ["start_date_field", "end_date_field"],

    // PERMISSION ENABLE
    PERMISSION_ENABLE_FORM_DICT: {
        "permission_status_field": {
            "div_id": {
                "status": "id_status_not_selected_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "delete_switch_field": {
            "div_id": {
                "confirm": "id_record_not_confirm_field_error",
            },
            "text": {
                "confirm": "Campo obligatorio.",
            }
        },
    },

    PERMISSION_ENABLE_BLANK_FIELDS: ["permission_status_field", "delete_switch_field"],

    // PAYROLL ADJUST
    PAYROLL_ADJUST_FORM_DICT: {
        "ccss_ivm": {
            "div_id": {
                "blank": "id_ccss_ivm_blank_field_error",
                "chars": "id_ccss_ivm_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "ccss_eme": {
            "div_id": {
                "blank": "id_ccss_eme_blank_field_error",
                "chars": "id_ccss_eme_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "rop_popular": {
            "div_id": {
                "blank": "id_rop_popular_blank_field_error",
                "chars": "id_rop_popular_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "rent_tax": {
            "div_id": {
                "blank": "id_rent_tax_blank_field_error",
                "chars": "id_rent_tax_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "loan_request": {
            "div_id": {
                "blank": "id_loan_request_blank_field_error",
                "chars": "id_loan_request_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "child_support": {
            "div_id": {
                "blank": "id_child_support_blank_field_error",
                "chars": "id_child_support_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "association": {
            "div_id": {
                "blank": "id_association_blank_field_error",
                "chars": "id_association_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "other_deductions": {
            "div_id": {
                "blank": "id_other_deductions_blank_field_error",
                "chars": "id_other_deductions_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "payroll_details": {
            "div_id": {
                "blank": "id_payroll_details_blank_field_error",
                "chars": "id_payroll_details_chars_field_error",
                "length": "id_payroll_details_length_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "No se permiten caracteres especiales.",
                "length": "Detalle de planilla debe tener mínimo 10 caracteres."
            }
        }
    },

    PAYROLL_ADJUST_BLANK_FIELDS: ["ccss_ivm", "ccss_eme", "rop_popular", "rent_tax", "loan_request",
        "child_support", "association", "other_deductions", "payroll_details"],

    // SETTLEMENT ADJUST
    SETTLEMENT_ENABLE_FORM_DICT: {
        "cesantia_amount": {
            "div_id": {
                "blank": "id_cesantia_amount_blank_field_error",
                "chars": "id_cesantia_amount_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "vacation_amount": {
            "div_id": {
                "blank": "id_vacation_amount_blank_field_error",
                "chars": "id_vacation_amount_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "bonus_amount": {
            "div_id": {
                "blank": "id_bonus_amount_blank_field_error",
                "chars": "id_bonus_amount_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "payroll_amount": {
            "div_id": {
                "blank": "id_payroll_amount_blank_field_error",
                "chars": "id_payroll_amount_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "settlement_type": {
            "div_id": {
                "status": "id_settlement_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "settlement_status": {
            "div_id": {
                "status": "id_settlement_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "settlement_details": {
            "div_id": {
                "blank": "id_settle_details_blank_field_error",
                "chars": "id_settle_details_chars_field_error",
                "length": "id_settle_details_length_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "No se permiten caracteres especiales.",
                "length": "Detalle de liquidación debe tener mínimo 10 caracteres."
            }
        }
    },

    SETTLEMENT_ENABLE_BLANK_FIELDS: ["cesantia_amount", "vacation_amount", "bonus_amount",
        "payroll_amount", "settlement_type", "settlement_status", "settlement_details"],

    // BONUS ADJUST
    BONUS_ENABLE_FORM_DICT: {
        "bonus_month": {
            "div_id": {
                "status": "id_bonus_month_status_field_error",
            },
            "text": {
                "status": "Debe seleccionar una de las opciones del menú.",
            }
        },
        "bonus_year": {
            "div_id": {
                "blank": "id_bonus_year_blank_field_error",
                "chars": "id_bonus_year_chars_field_error",
                "after": "id_bonus_year_after_current_field_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente.",
                "after": "El año del monto de la cuota no puede ser mayor al año actual."
            }
        },
        "bonus_amount": {
            "div_id": {
                "blank": "id_bonus_amount_blank_field_error",
                "chars": "id_bonus_amount_chars_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar números únicamente."
            }
        },
        "bonus_update_date": {
            "div_id": {
                "blank": "id_bonus_update_date_blank_field_error",
                "before": "id_bonus_update_date_before_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "before": "La fecha de registro no puede estar antes de la fecha actual."
            }
        },
    },

    BONUS_ENABLE_BLANK_FIELDS: ["bonus_month", "bonus_year", "bonus_amount", "bonus_update_date"],

    // PROFILE TRACKER
    PROFILE_TRACKER_FORM_DICT: {
        "check_out_date_field": {
            "div_id": {
                "blank": "id_checkout_blank_field_error",
                "disable": "id_checkin_date_disable_field_error",
                "before": "id_checkout_before_checkin_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "disable": "No se puede ingresar marca de salida sin haber ingresado marca de entrada primero.",
                "before": "Registro de salida no puede ser menor al registro de entrada.",
            }
        },
    },

    PROFILE_TRACKER_BLANK_FIELDS: ["check_out_date_field"],

    // PROFILE CONTACT INFO
    PROFILE_CONTACT_INFO_FORM_DICT: {
        "province_field": {
            "div_id": {
                "status": "id_province_blank_field_error",
            },
            "text": {
                "status": "Campo Obligatorio.",
            }
        },
        "canton_field": {
            "div_id": {
                "status": "id_canton_blank_field_error",
            },
            "text": {
                "status": "Campo Obligatorio.",
            }
        },
        "district_field": {
            "div_id": {
                "status": "id_district_blank_field_error",
            },
            "text": {
                "status": "Campo Obligatorio.",
            }
        },
        "postal_code_field": {
            "div_id": {
                "blank": "id_postal_code_blank_field_error",
                "number": "id_postal_code_chars_format_field_error",
                "length": "id_postal_code_length_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "number": "Ingresar únicamente números.",
                "length": "El código postal debe tener 5 dígitos."
            }
        },
        "address_detail_field": {
            "div_id": {
                "blank": "id_address_detail_blank_field_error",
                "chars": "id_address_detail_spec_chars_field_error",
                "length": "id_address_detail_length_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "No se permiten caracteres especiales.",
                "length": "Detalle de dirección debe tener mínimo 10 caracteres."
            }
        },
        "email_field": {
            "div_id": {
                "blank": "id_email_blank_field_error",
                "format": "id_email_format_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "format": "Formato incorrecto de correo electrónico.",
            }
        },
        "phone_field": {
            "div_id": {
                "blank": "id_phone_blank_field_error",
                "chars": "id_phone_chars_field_error",
                "length": "id_phone_length_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "chars": "Ingresar únicamente números.",
                "length": "El número telefónico debe tener 8 dígitos."
            }
        },
    },

    PROFILE_CONTACT_INFO_BLANK_FIELDS: ["province_field", "canton_field", "district_field", "postal_code_field",
        "address_detail_field", "email_field", "phone_field"],

    // PROFILE PASSWORD
    PROFILE_PASSWORD_UPDATE_FORM_DICT: {
        "password_current_field": {
            "div_id": {
                "blank": "id_current_password_blank_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
            }
        },
        "new_password_field": {
            "div_id": {
                "blank": "id_new_password_blank_field_error",
                "length": "id_new_password_length_field_error",
                "format": "id_new_password_format_field_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "length": "La nueva contraseña debe tener mínimo 9 caracteres.",
                "format": "La contraseña debe contener mínimo una letra mayúscula o minúscula, números y signos de puntuación."
            }
        },
        "confirm_password_field": {
            "div_id": {
                "blank": "id_password_confirm_blank_field_error",
                "mismatch": "id_password_confirm_mismatch_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "mismatch": "Las contraseñas no coinciden."
            }
        },
    },

    PROFILE_PASSWORD_UPDATE_BLANK_FIELDS: ["password_current_field", "new_password_field", "confirm_password_field"],

    // AUTH LOGIN
    AUTH_LOGIN_FORM_DICT: {
        'email_login_field': {
            'div_id': {
                'blank': 'id_email_blank_field_error',
                'format': 'id_email_format_field_error'
            },
            'text': {
                'blank': 'Campo Obligatorio.',
                'format': 'Formato incorrecto de correo electrónico.'
            },
        },
        'password_login_field': {
            'div_id': {
                'blank': 'id_password_blank_field_error'
            },
            'text': {
                'blank': 'Campo Obligatorio.',
            }
        }
    },

    AUTH_LOGIN_BLANK_FIELDS: ["email_login_field", "password_login_field"],

    // AUTH RECOVER
    AUTH_RECOVER_FORM_DICT: {
        "email_recover_field": {
            "div_id": {
                "blank": "id_email_blank_field_error",
                "format": "id_email_format_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "format": "Formato incorrecto de correo electrónico.",
            }
        },
    },

    AUTH_RECOVER_BLANK_FIELDS: ["email_recover_field"],

    // AUTH RESTORE
    AUTH_RESTORE_FORM_DICT: {
        "user_identification": {
            "div_id": {
                "blank": "id_identification_blank_field_error",
                "chars": "id_identification_chars_field_error",
                "length": "id_identification_length_field_error"
            },
            "text": {
                "blank": "Campo obligatorio.",
                "length": "El número de identificación debe contener nueve dígitos.",
                "chars": "El número de identificación solamente pueden ser números.",
            }
        },
        "temp_password_field": {
            "div_id": {
                "blank": "id_temp_password_blank_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
            }
        },
        "new_password_field": {
            "div_id": {
                "blank": "id_new_password_blank_field_error",
                "length": "id_new_password_length_field_error",
                "format": "id_new_password_format_field_error"
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "length": "La nueva contraseña debe tener mínimo 9 caracteres.",
                "format": "La contraseña debe contener mínimo una letra mayúscula o minúscula, números y signos de puntuación."
            }
        },
        "confirm_password_field": {
            "div_id": {
                "blank": "id_confirm_password_blank_field_error",
                "mismatch": "id_confirm_password_mismatch_field_error",
            },
            "text": {
                "blank": "Campo Obligatorio.",
                "mismatch": "Las contraseñas no coinciden."
            }
        },
    },

    AUTH_RESTORE_BLANK_FIELDS: ["user_identification", "temp_password_field", "new_password_field",
        "confirm_password_field"],

}