// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Password Recover Validator Class */
export class RecoverValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.AUTH_RECOVER_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.passwordRecoverEmailFieldGenerator("email_recover_field");

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
        Static.AUTH_RECOVER_BLANK_FIELDS.forEach((item) => {
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

    /* email access validate */
    passwordRecoverEmailFieldGenerator(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.email_recover_field.div_id.blank);
        let divFormat = document.getElementById(this.data.email_recover_field.div_id.format);

        // blank field listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.email_recover_field.text.blank, this);

        // if blank field, do not submit
        if(this.valid) {
            inputField.addEventListener("input", () => {
                let value = inputField.value.trim();

                if(!Static.REGEX.email_format.test(value)) {
                    // clear previous errors
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    // display error
                    Shared.displayErrorMessages(inputField, divFormat, this.data.email_recover_field.text.format);
                    this.valid = false;
                }
                else {
                    // if validation pass
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    this.valid = true;
                }
            });
        }
    }

}