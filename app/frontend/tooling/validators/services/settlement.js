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

        this.settlementTypeFieldValidate("settlement_type");

        this.settlementStatusFieldValidate("settlement_status");

        this.settlementDetailFieldValidate("settlement_details");

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

                if(!Static.REGEX.amount_format.test(value)) {

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

    /* vacations field validate */
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

                if(!Static.REGEX.amount_format.test(value)) {
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

                if(!Static.REGEX.amount_format.test(value)) {
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

                if(!Static.REGEX.amount_format.test(value)) {
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

    /* settlement type validation */
    settlementTypeFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.settlement_type.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.settlement_type.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.settlement_type.text.status);
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

    /* settlement status validation */
    settlementStatusFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.settlement_status.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.settlement_status.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.settlement_status.text.status);
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

    /* settlement detail validation */
    settlementDetailFieldValidate(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.settlement_details.div_id.blank);
        let divChars = document.getElementById(this.data.settlement_details.div_id.chars);
        let divLength = document.getElementById(this.data.settlement_details.div_id.length);

        // listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.settlement_details.text.blank, this);

        if(this.valid) {
            inputField.addEventListener("input", () => {
                let value = inputField.value.trim();

                if(!Static.REGEX.address.test(value)) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divLength]);
                    // display error
                    Shared.displayErrorMessages(inputField, divChars, this.data.settlement_details.text.chars);
                    this.valid = false;
                }
                else if(value.length < Static.ADDRESS_LENGTH) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divChars]);
                    // display error
                    Shared.displayErrorMessages(inputField, divLength, this.data.settlement_details.text.length);
                    this.valid = false;
                }
                else {
                    // clear errors
                    Shared.clearErrorMessages(inputField, [divChars, divLength]);
                    this.valid = true;
                }
            });
        }
    }

}