// import
import {Static} from '../../../utils/contansts.js';
import {Shared} from '../../../utils/shared.js';


/* Deduction Validator form fields Class */
export class DeductionValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.DEDUCTIONS_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {
        /* on-time validators */
        this.deductionNameFieldValidate('deduction_name');

        this.deductionPercentageFieldValidate('deduction_percentage');

        this.deductionCreateDateFieldValidate('deduction_create_date');

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
        Static.DEDUCTIONS_BLANK_FIELDS.forEach((item) => {
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

    /* deduction name field */
    deductionNameFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.deduction_name.div_id.blank);
        let divChars = document.getElementById(this.data.deduction_name.div_id.chars);
        let divLength = document.getElementById(this.data.deduction_name.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.deduction_name.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(!Static.REGEX.only_letters.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divLength]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.deduction_name.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.MIN_DEDUCTION_NAME_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.deduction_name.text.length);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divChars, divLength]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* deduction percentage field */
    deductionPercentageFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.deduction_percentage.div_id.blank);
        let divFormat = document.getElementById(this.data.deduction_percentage.div_id.format);
        let divMin = document.getElementById(this.data.deduction_percentage.div_id.min);
        let divMax = document.getElementById(this.data.deduction_percentage.div_id.max);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.deduction_percentage.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();

                /* validate only letters are input */
                if(!Static.REGEX.percentage.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divMin, divMax]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divFormat, this.data.deduction_percentage.text.format);
                    /* update flag */
                    this.valid = false;
                }
                else if(value < Static.MIN_PERCENTAGE){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divFormat, divMax]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divMin, this.data.deduction_percentage.text.min);
                    /* update flag */
                    this.valid = false;
                }
                else if(value > Static.MAX_PERCENTAGE){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divFormat, divMin]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divMax, this.data.deduction_percentage.text.max);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divFormat, divMin, divMax]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* deduction create date field */
    deductionCreateDateFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.deduction_create_date.div_id.blank);
        let divBefore = document.getElementById(this.data.deduction_create_date.div_id.before);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.deduction_create_date.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divBefore, this.data.deduction_create_date.text.before);
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