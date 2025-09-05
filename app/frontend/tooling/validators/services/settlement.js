// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Settlement Adjustment Hours Validator Class */
export class AdjustValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.SETTLEMENT_ENABLE_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.cesantiaFieldValidate("cesantia_amount");

        this.vacationAmountFieldValidate("vacation_amount");

        this.bonusAmountFieldValidate("bonus_amount");

        this.salaryUpToTodayAmountFieldValidate("payroll_amount");

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
        Static.SETTLEMENT_ENABLE_BLANK_FIELDS.forEach((item) => {
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

    /* cesantia field validate */
    cesantiaFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.cesantia_amount.div_id.blank);
        let divChars = document.getElementById(this.data.cesantia_amount.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.cesantia_amount.text.blank, this);

        /* event listener */
        if(this.valid) {

            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {

                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);

                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.cesantia_amount.text.chars);

                    /* update flag */
                    this.valid = false;
                }
                else {

                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);

                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* vacactions field validate */
    vacationAmountFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.vacation_amount.div_id.blank);
        let divChars = document.getElementById(this.data.vacation_amount.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.vacation_amount.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.vacation_amount.text.chars);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* bonus amount field validate */
    bonusAmountFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.bonus_amount.div_id.blank);
        let divChars = document.getElementById(this.data.bonus_amount.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.bonus_amount.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.bonus_amount.text.chars);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* salary up-today validate field */
    salaryUpToTodayAmountFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.payroll_amount.div_id.blank);
        let divChars = document.getElementById(this.data.payroll_amount.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.payroll_amount.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.payroll_amount.text.chars);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }


}