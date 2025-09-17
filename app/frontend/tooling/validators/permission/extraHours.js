// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";
import {Utils} from "../../utils/utils.js";


/* Permission Extra Hours Validator Class */
export class ExtraHourValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.PERMISSION_EXTRA_HOUR_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.extraHoursDateFieldValidate("hour_date_field");

        this.extraHoursScheduleTypeFieldValidate("hour_schedule_type");

        this.extraHoursQuantityFieldValidate("hour_quantity_field");

        /* form submission */
        this.form.addEventListener("submit", (e) => {

            /* prevent form auto submission */
            e.preventDefault();

            /* validate blank fields and selections */
            if(!this.validateBlankFields()) {
                /* return to on-time validators */
                return;
            }

            if(this.valid){
                /* submit form */
                this.form.submit();
            }
        });
    }

    /* blank fields */
    validateBlankFields() {
        /* flag */
        let allValid = true;

        /* traverse list of blank field div names */
        Static.PERMISSION_EXTRA_HOUR_BLANK_FIELDS.forEach((item) => {
            /* current div element */
            let fieldData = this.data[item];
            /* dropdown and input field validation */
            let inputField = this.form.elements.namedItem(item);

            /* validate input field type dropdown */
            if(inputField.tagName === "SELECT" && inputField.value === "not_select") {
                /* change flag */
                allValid = false;
                /* get error div element from current div element */
                let errorDiv = document.getElementById(fieldData.div_id.status);
                /* display error message */
                if(errorDiv){
                    Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.status);
                }
            }
            /* validate input field type text or date */
            else if(!inputField || inputField.value.trim() === "") {
                /* change flag */
                allValid = false;
                /* get error div element from current div element */
                let errorDiv = document.getElementById(fieldData.div_id.blank);
                /* display error message */
                if(errorDiv){
                    Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.blank);
                }
            }
        });

        /* validate flag status */
        if(this.valid) {
            this.valid = allValid;
        }
        return this.valid;
    }

    /* extra hour date field */
    extraHoursDateFieldValidate(fieldName) {
        /* get element by name attribute */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.hour_date_field.div_id.blank);
        let divBefore = document.getElementById(this.data.hour_date_field.div_id.before);
        let divSunday = document.getElementById(this.data.hour_date_field.div_id.sunday);

        /* blank field listener */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.hour_date_field.text.blank, this);

        /* if blank field do not submit */
        if(this.valid) {
            /* event listener on input field */
            inputField.addEventListener("input", () => {

                /* collect values from elements */
                let dateField = Utils.dateStartExtraHour(inputField);

                if(dateField.start < dateField.current) {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divSunday]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divBefore, this.data.hour_date_field.text.before);
                    /* update flag */
                    this.valid = false;
                }

                else if(Utils.identifyingNotSunday(inputField.value)) {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divBefore]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divSunday, this.data.hour_date_field.text.sunday);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divBefore, divSunday]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* extra hour schedule type */
    extraHoursScheduleTypeFieldValidate(fieldName) {
        /* get element by name attr */
        let selectField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.hour_schedule_type.div_id.status);

        /* blank field listener */
        Shared.validateInputBlankFields(selectField, divStatus, this.data.hour_schedule_type.text.status, this);

        /* event listener */
        if(this.valid) {
            selectField.addEventListener("input", () => {

                /* collect value */
                let value = selectField.value.trim();

                if(value === "not_select") {
                    /* clear prev errors */
                    Shared.clearErrorMessages(selectField, [divStatus]);
                    /* display error msgs */
                    Shared.displayErrorMessages(selectField, divStatus, this.data.hour_schedule_type.text.status);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(selectField, [divStatus]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* extra hour quantity */
    extraHoursQuantityFieldValidate(fieldName) {
        /* get element by name attribute */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.hour_quantity_field.div_id.blank);
        let divChars = document.getElementById(this.data.hour_quantity_field.div_id.chars);
        let divExceed = document.getElementById(this.data.hour_quantity_field.div_id.exceed);

        /* blank field listener */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.hour_quantity_field.text.blank, this);

        /* if blank field do not submit */
        if(this.valid) {

            /* event listener on input field */
            inputField.addEventListener("input", () => {

                /* collect values from elements */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divExceed]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.hour_quantity_field.text.chars);
                    /* update flag */
                    this.valid = false;
                }

                else if(value > Static.MAX_EXTRA_HOURS) {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divExceed, this.data.hour_quantity_field.text.exceed);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divExceed, divChars]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}