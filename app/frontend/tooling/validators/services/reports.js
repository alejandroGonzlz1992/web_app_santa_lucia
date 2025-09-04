// import
import {Static} from '../../utils/contansts.js';
import {Shared} from '../../utils/shared.js';


/* Reports Validator form fields Class */
export class ReportsValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.REPORT_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {
        /* on-time validators */
        this.reportNameFieldValidate('report_name_field');

        this.reportStartDateFieldValidate('start_date_field', 'end_date_field');

        this.reportEndDateFieldValidate('start_date_field', 'end_date_field');

        this.reportDeliveryFieldValidate('report_deliver');

        /* form submission */
        this.form.addEventListener('submit', (e) => {
            /* prevent autoform submission */
            e.preventDefault();

            /* validate blank fields */
            if(!this.validateBlankFields()) {
                /* return to on-time validators */
                return;
            }

            if(this.valid) {
                /* submit form */
                this.form.submit();
            }
        });
    }

    /* validate blank fields */
    validateBlankFields() {
        /* tracking flag */
        let flag = true;

        /* traverse list of blank form fields' name attrs */
        Static.REPORT_BLANK_FIELDS.forEach((item) => {
            /* get the current div element attrs using name attr */
            let fieldData = this.data[item];

            /* collect the current input field using name attr from traversed list */
            let inputField = this.form.elements.namedItem(item);

            /* validate if current input field is dropdown type */
            if(inputField.tagName === "SELECT" && inputField.value === "not_select") {
                /* update tracking flag */
                flag = false;

                /* get error div element using fieldData info */
                let errorDiv = document.getElementById(fieldData.div_id.status);

                if(errorDiv) {
                    /* display error message */
                    Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.status);
                }
            }
            /* validate if current input field is None or has blank info */
            else if(!inputField || inputField.value.trim() === "") {
                /* update tracking flag */
                flag = false;

                /* get error div element using fieldData info */
                let errorDiv = document.getElementById(fieldData.div_id.blank);

                if(errorDiv) {
                    /* display error message */
                    Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.blank);
                }
            }
        });

        /* validate tracking flag status */
        if(this.valid) {
            this.valid = flag;
        }

        /* return global this.valid var */
        return this.valid;
    }

    /* report name field */
    reportNameFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.report_name_field.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.report_name_field.text.status, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(value === "not_select"){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divStatus]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divStatus, this.data.report_name_field.text.status);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divStatus]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* report start date field */
    reportStartDateFieldValidate(startField, endField) {
        /* get input element and div ids */
        let inputStartField = this.form.elements.namedItem(startField);
        let inputEndField = this.form.elements.namedItem(endField);
        let divBlank = document.getElementById(this.data.start_date_field.div_id.blank);
        let divAfter = document.getElementById(this.data.start_date_field.div_id.after);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputStartField, divBlank, this.data.start_date_field.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputStartField.addEventListener("input", () => {
                /* get input field value */
                let dateField = Shared.reportDatesFormatting(inputStartField, inputEndField);

                /* validate only letters are input */
                if(dateField.start > dateField.current){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputStartField, [divAfter]);
                    /* display error message */
                    Shared.displayErrorMessages(inputStartField, divAfter, this.data.start_date_field.text.after);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputStartField, [divAfter]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* report end date field */
    reportEndDateFieldValidate(startField, endField) {
        /* get input element and div ids */
        let inputEndField = this.form.elements.namedItem(endField);
        let inputStartField = this.form.elements.namedItem(startField);
        let divBlank = document.getElementById(this.data.end_date_field.div_id.blank);
        let divBefore = document.getElementById(this.data.end_date_field.div_id.before);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputEndField, divBlank, this.data.end_date_field.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputEndField.addEventListener("input", () => {
                /* get input field value */
                let dateField = Shared.reportDatesFormatting(inputStartField, inputEndField);

                /* validate only letters are input */
                if(dateField.start > dateField.end){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputEndField, [divBefore]);
                    /* display error message */
                    Shared.displayErrorMessages(inputEndField, divBefore, this.data.end_date_field.text.before);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputEndField, [divBefore]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* report delivery form field */
    reportDeliveryFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.report_deliver.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.report_deliver.text.status, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(value === "not_select"){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divStatus]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divStatus, this.data.report_deliver.text.status);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divStatus]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}