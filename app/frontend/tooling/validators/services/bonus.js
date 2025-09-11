// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Bonus Adjustment Hours Validator Class */
export class AdjustValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.BONUS_ENABLE_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.bonusMonthQuotaFieldValidate("bonus_month");

        this.bonusAmountQuotaFieldValidate("bonus_amount");

        this.bonusAmountUpdateDateFieldValidate("bonus_update_date");

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
        Static.BONUS_ENABLE_BLANK_FIELDS.forEach((item) => {
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

    /* month of quota field */
    bonusMonthQuotaFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.bonus_month.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.bonus_month.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.bonus_month.text.status);
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

    /* month amount quota field */
    bonusAmountQuotaFieldValidate(fieldName) {
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

    /* bonus update field */
    bonusAmountUpdateDateFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.bonus_update_date.div_id.blank);
        let divBefore = document.getElementById(this.data.bonus_update_date.div_id.before);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.bonus_update_date.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* format input date */
                let dates = Shared.inputDateAndCurrentDateFormat(inputField);
                /* validate create date before current date */
                if(dates.create < dates.current){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divBefore]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divBefore, this.data.bonus_update_date.text.before);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divBefore]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}