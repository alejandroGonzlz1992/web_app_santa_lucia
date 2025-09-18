// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";
import {Utils} from "../../utils/utils.js";


/* Permission Vacations Validator Class */
export class VacationsValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.PERMISSION_VACATION_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.vacationStartDateFieldValidate("start_date_field");

        this.vacationEndDateFieldValidate("start_date_field", "end_date_field");

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
        Static.PERMISSION_VACATION_BLANK_FIELDS.forEach((item) => {
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

    /* vacation start date field */
    vacationStartDateFieldValidate(fieldName) {
        /* get element by name attr */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.start_date_field.div_id.blank);
        let divCurrent = document.getElementById(this.data.start_date_field.div_id.current);
        let divSaturday = document.getElementById(this.data.start_date_field.div_id.on_saturday);
        let divSunday = document.getElementById(this.data.start_date_field.div_id.on_sunday);

        /* blank field listener */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.start_date_field.text.blank, this);

        /* if blank field do not submit */
        if(this.valid) {

            /* event listener on input field */
            inputField.addEventListener("input", () => {

                /* collect values from elements */
                let dateField = Utils.dateStartExtraHour(inputField);

                if(dateField.start < dateField.current) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divSaturday, divSunday]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divCurrent, this.data.start_date_field.text.current);
                    /* update flag */
                    this.valid = false;
                }

                else if(Utils.identifyingNotSaturday(inputField.value)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divCurrent, divSunday]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divSaturday, this.data.start_date_field.text.on_saturday);
                    /* update flag */
                    this.valid = false;
                }

                else if(Utils.identifyingNotSunday(inputField.value)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divCurrent, divSaturday]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divSunday, this.data.start_date_field.text.on_sunday);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divCurrent, divSaturday, divSunday]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* vacation end date field */
    vacationEndDateFieldValidate(startField, endField) {
        /* get element by name attr */
        let inputEndDateField = this.form.elements.namedItem(endField);
        let inputStartDateField = this.form.elements.namedItem(startField);

        let divBlank = document.getElementById(this.data.end_date_field.div_id.blank);
        let divBefore = document.getElementById(this.data.end_date_field.div_id.before);
        let divSaturday = document.getElementById(this.data.end_date_field.div_id.on_saturday);
        let divSunday = document.getElementById(this.data.end_date_field.div_id.on_sunday);

        /* blank field listener */
        Shared.validateInputBlankFields(inputEndDateField, divBlank, this.data.end_date_field.text.blank, this);

        /* if blank field do not submit */
        if(this.valid) {

            /* event listener on input field */
            inputEndDateField.addEventListener("input", () => {

                /* collect values from elements */
                let dateField = Utils.dateVacations(inputStartDateField, inputEndDateField);

                if(dateField.end < dateField.start) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputEndDateField, [divSaturday, divSunday]);
                    /* display errors */
                    Shared.displayErrorMessages(inputEndDateField, divBefore, this.data.end_date_field.text.before);
                    /* update flag */
                    this.valid = false;
                }

                else if(Utils.identifyingNotSaturday(inputEndDateField.value)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputEndDateField, [divBefore, divSunday]);
                    /* display errors */
                    Shared.displayErrorMessages(inputEndDateField, divSaturday, this.data.end_date_field.text.on_saturday);
                    /* update flag */
                    this.valid = false;
                }

                else if(Utils.identifyingNotSunday(inputEndDateField.value)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputEndDateField, [divBefore, divSaturday]);
                    /* display errors */
                    Shared.displayErrorMessages(inputEndDateField, divSunday, this.data.end_date_field.text.on_sunday);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputEndDateField, [divBefore, divSaturday, divSunday]);

                    /* fetch number of days */
                    Utils.fetchingDaysVacation(dateField, "id_day_field", "day_field_total");

                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}