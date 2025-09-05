// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";
import {Utils} from "../../utils/utils.js";


/* Inabilities Validator Class */
export class InabilityValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.INABILITY_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.inabilityStartAndEndDateFieldValidate("start_date", "return_date");

        this.inabilityNumberFieldValidate("inability_number");

        this.inabilityFileFieldValidate("inability_file");

        this.inabilityDetailsFieldValidate("inability_detail");

        /* collect days */
        Shared.calculatingInabilityDaysDifference(
            this.form, "start_date", "return_date", "inability_day");

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
        Static.INABILITY_BLANK_FIELDS.forEach((item) => {
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

    /* star and end date inability field */
    inabilityStartAndEndDateFieldValidate(fieldStart, fieldEnd) {
        /* get element by name attr */
        let inputFieldStart = this.form.elements.namedItem(fieldStart);
        let inputFieldReturn = this.form.elements.namedItem(fieldEnd);

        let divBlankStart = document.getElementById(this.data.start_date.div_id.blank);
        let divBlankReturn = document.getElementById(this.data.return_date.div_id.blank);

        let divBefore = document.getElementById(this.data.return_date.div_id.before);

        /* blank field listener */
        Shared.validateInputBlankFields(inputFieldStart, divBlankStart, this.data.start_date.text.blank, this);
        Shared.validateInputBlankFields(inputFieldReturn, divBlankReturn, this.data.return_date.text.blank, this);

        /* event listener */
        if(this.valid) {

            /* input field */
            inputFieldReturn.addEventListener("input", () => {
                /* collect values */
                let dateField = Utils.dateVacations(inputFieldStart, inputFieldReturn);

                if(dateField.end < dateField.start) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputFieldReturn, [divBefore]);
                    /* display errors */
                    Shared.displayErrorMessages(inputFieldReturn, divBefore, this.data.return_date.text.before);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputFieldReturn, [divBefore]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* inability number field */
    inabilityNumberFieldValidate(fieldName) {
        /* get element by name attr */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.inability_number.div_id.blank);
        let divLength = document.getElementById(this.data.inability_number.div_id.length);
        let divChars = document.getElementById(this.data.inability_number.div_id.chars);

        /* blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.inability_number.text.blank, this);

        /* event listener */
        if(this.valid) {

            inputField.addEventListener("input", () => {
                /* get values */
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divLength]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divChars, this.data.inability_number.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.MIN_INABILITY_NUMBER) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divLength, this.data.inability_number.text.length);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divLength, divChars]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* inability file field */
    inabilityFileFieldValidate(fieldName) {
        /* get element by name attr */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.inability_file.div_id.blank);
        let divFormat = document.getElementById(this.data.inability_file.div_id.format);

        /* blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.inability_file.text.blank, this);

        /* event listener */
        if(this.valid) {

            inputField.addEventListener("input", () => {

                /* collect values */
                let file = inputField.files[0].name;
                let fileExtension = file.split(".").pop().toLowerCase();

                if(!Static.ALLOW_FILE_EXT.includes(fileExtension)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    /* display error mssg */
                    Shared.displayErrorMessages(inputField, divFormat, this.data.inability_file.text.format);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* inability details field */
    inabilityDetailsFieldValidate(fieldName) {
        /* get element by name attr */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.inability_detail.div_id.blank);
        let divLength = document.getElementById(this.data.inability_detail.div_id.length);
        let divChars = document.getElementById(this.data.inability_detail.div_id.chars);

        /* blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.inability_detail.text.blank, this);

        /* event listener */
        if(this.valid) {

            inputField.addEventListener("input", () => {
                /* collect values */
                let value = inputField.value.trim();

                if(!Static.REGEX.address.test(value)) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divLength]);
                    /* display error mssg */
                    Shared.displayErrorMessages(inputField, divChars, this.data.inability_detail.text.chars);
                    /* update flag */
                    this.valid = false;
                }

                else if(value.length < Static.ADDRESS_LENGTH) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error mssg */
                    Shared.displayErrorMessages(inputField, divLength, this.data.inability_detail.text.length);
                    /* update flag */
                    this.valid = false;

                }
                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divChars, divLength]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}