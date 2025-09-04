// import
import {Static} from '../../../utils/contansts.js';
import {Shared} from '../../../utils/shared.js';


/* Questions Validator form fields Class */
export class PaymentDateValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.PAYMENT_DATE_FORM_DICT;

        /* Enable and disable "Mensual" payment type */
        Shared.disableEnablePayDateField(
            'id_payment_frecuency', 'id_payment_date',
            'id_payment2_date', 'id_payment2_hidden');

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {
        /* on-time validators */
        this.paymentDateTypeFieldValidate('payment_frecuency');

        this.paymentFirstDateFieldValidate('payment_date', 'payment2_date');

        this.paymentSecondDateFieldValidate('payment2_date', 'payment_date');

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
        Static.PAYMENT_DATE_BLANK_FIELDS.forEach((item) => {
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

    /* payment date type field */
    paymentDateTypeFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.payment_frecuency.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.payment_frecuency.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.payment_frecuency.text.status);
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

    /* payment first date field */
    paymentFirstDateFieldValidate(first, second) {
        /* get input and div elements */
        let inputFirstDate = this.form.elements.namedItem(first);
        let inputSecondDate = this.form.elements.namedItem(second);
        let divBlank = document.getElementById(this.data.payment_date.div_id.blank);
        let divAfter = document.getElementById(this.data.payment_date.div_id.after);

        /* blank field listener */
        Shared.validateInputBlankFields(inputFirstDate, divBlank, this.data.payment_date.text.blank, this);

        /* input event listener */
        if(this.valid) {
            inputFirstDate.addEventListener("input", () => {

                let dateField = Shared.firstPayDateSecondPayDate(inputFirstDate, inputSecondDate);

                if(dateField.start > dateField.end) {
                    /* clear prev error msg */
                    Shared.clearErrorMessages(inputFirstDate, [divAfter]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputFirstDate, divAfter, this.data.payment_date.text.after);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev error msg */
                    Shared.clearErrorMessages(inputFirstDate, [divAfter]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* payment second date field */
    paymentSecondDateFieldValidate(second, first) {
        /* get input and div elements */
        let inputSecondDate = this.form.elements.namedItem(second);
        let inputFirstDate = this.form.elements.namedItem(first);
        let divBlank = document.getElementById(this.data.payment2_date.div_id.blank);
        let divBefore = document.getElementById(this.data.payment2_date.div_id.before);

        /* blank field listener */
        Shared.validateInputBlankFields(inputSecondDate, divBlank, this.data.payment2_date.text.blank, this);

        /* input event listener */
        if(this.valid) {
            inputSecondDate.addEventListener("input", () => {

                let dateField = Shared.firstPayDateSecondPayDate(inputFirstDate, inputSecondDate);

                if(dateField.end < dateField.start) {
                    /* clear prev error msg */
                    Shared.clearErrorMessages(inputSecondDate, [divBefore]);
                    /* display error msg */
                    Shared.displayErrorMessages(inputSecondDate, divBefore, this.data.payment2_date.text.before);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev error msg */
                    Shared.clearErrorMessages(inputSecondDate, [divBefore]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}