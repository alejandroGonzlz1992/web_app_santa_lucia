// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Payroll Adjustment Validator Class */
export class AdjustValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.PAYROLL_ADJUST_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.ccssIvmFieldValidate("ccss_ivm");

        this.ccssEmeFieldValidate("ccss_eme");

        this.ropPopularFieldValidate("rop_popular");

        this.rentTaxFieldValidate("rent_tax");

        this.loanRequestFieldValidate("loan_request");

        this.childSupportFieldValidate("child_support");

        this.requireLoanRequestFieldValidate("require_loans");

        this.otherDeductionRequestFieldValidate("other_deductions");

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
        Static.PAYROLL_ADJUST_BLANK_FIELDS.forEach((item) => {
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

    /* ccss ivm validate field */
    ccssIvmFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.ccss_ivm.div_id.blank);
        let divChars = document.getElementById(this.data.ccss_ivm.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.ccss_ivm.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.ccss_ivm.text.chars);
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

    /* ccss eme validate field */
    ccssEmeFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.ccss_eme.div_id.blank);
        let divChars = document.getElementById(this.data.ccss_eme.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.ccss_eme.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.ccss_eme.text.chars);
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

    /* rop popular validate field */
    ropPopularFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.rop_popular.div_id.blank);
        let divChars = document.getElementById(this.data.rop_popular.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.rop_popular.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.rop_popular.text.chars);
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

    /* rent tax validate field */
    rentTaxFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.rent_tax.div_id.blank);
        let divChars = document.getElementById(this.data.rent_tax.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.rent_tax.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.rent_tax.text.chars);
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

    /* loan request validate field */
    loanRequestFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.loan_request.div_id.blank);
        let divChars = document.getElementById(this.data.loan_request.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.loan_request.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.loan_request.text.chars);
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

    /* child support validate field */
    childSupportFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.child_support.div_id.blank);
        let divChars = document.getElementById(this.data.child_support.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.child_support.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.child_support.text.chars);
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

    /* require loan request validate field */
    requireLoanRequestFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.require_loans.div_id.blank);
        let divChars = document.getElementById(this.data.require_loans.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.require_loans.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.require_loans.text.chars);
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

    /* other deduction validate field */
    otherDeductionRequestFieldValidate(fieldName) {
        /* get input element and div Id */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.other_deductions.div_id.blank);
        let divChars = document.getElementById(this.data.other_deductions.div_id.chars);

        /* validate blank field */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.other_deductions.text.blank, this);

        /* event listener */
        if(this.valid) {
            inputField.addEventListener("input", () => {

                /* collect element value */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev error msgs */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.other_deductions.text.chars);
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