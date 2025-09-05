// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Password Restore Validator Class */
export class RestoreValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.AUTH_RESTORE_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* enable and disable password */
        Shared.enableAndDisablePasswordField(
            Static.ENABLE_USER_RESTORE_PASSWORD[0],
            Static.ENABLE_USER_RESTORE_PASSWORD[1]
        );

        /* on-time validators */
        this.userIdentificationFieldValidate("user_identification");

        this.passwordRestoreTempPasswordFieldGenerator("temp_password_field");

        this.passwordRestoreNewPasswordFieldGenerator("new_password_field");

        this.passwordRestoreConfirmPasswordFieldGenerator("confirm_password_field", "new_password_field");

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
        Static.AUTH_RESTORE_BLANK_FIELDS.forEach((item) => {
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

    /* user identification */
    userIdentificationFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_identification.div_id.blank);
        let divChars = document.getElementById(this.data.user_identification.div_id.chars);
        let divLength = document.getElementById(this.data.user_identification.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_identification.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(!Static.REGEX.only_numbers.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divLength]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_identification.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length !== Static.IDENTIFICATION_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.user_identification.text.length);
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

    /* temp password restore validate */
    passwordRestoreTempPasswordFieldGenerator(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.temp_password_field.div_id.blank);

        // blank field listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.temp_password_field.text.blank, this);

        if(this.valid) {
            inputField.addEventListener("input", () => {

                if(!inputField || inputField.value.trim() === "") {
                    // clear previous errors
                    Shared.clearErrorMessages(inputField, [divBlank]);
                    // display error
                    Shared.displayErrorMessages(inputField, divBlank, this.data.temp_password_field.text.blank);
                    this.valid = false;
                }
                else {
                    // clear previous errors
                    Shared.clearErrorMessages(inputField, [divBlank]);
                    this.valid = true;
                }
            });
        }
    }

    /* new password restore validate */
    passwordRestoreNewPasswordFieldGenerator(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.new_password_field.div_id.blank);
        let divFormat = document.getElementById(this.data.new_password_field.div_id.format);
        let divLength = document.getElementById(this.data.new_password_field.div_id.length);

        // blank field listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.new_password_field.text.blank, this);

        if(this.valid) {
            inputField.addEventListener("input", () => {
                let value = inputField.value.trim();

                if(value < Static.PASSWORD_MIN_LENGTH) {
                    // clear previous errors
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    // display error
                    Shared.displayErrorMessages(inputField, divLength, this.data.new_password_field.text.length);
                    this.valid = false;
                }
                else if(!Static.REGEX.password.test(value)) {
                    // clear previous errors
                    Shared.clearErrorMessages(inputField, [divLength]);
                    // display error
                    Shared.displayErrorMessages(inputField, divFormat, this.data.new_password_field.text.format);
                    this.valid = false;
                }
                else {
                    // clear previous errors
                    Shared.clearErrorMessages(inputField, [divFormat, divLength]);
                    this.valid = true;
                }
            });
        }
    }

    /* confirm password restore validate */
    passwordRestoreConfirmPasswordFieldGenerator(fieldConfirm, fieldPassword) {
        let confirmPassword = this.form.elements.namedItem(fieldConfirm);
        let inputPassword = this.form.elements.namedItem(fieldPassword);
        let divBlank = document.getElementById(this.data.confirm_password_field.div_id.blank);
        let divMismatch = document.getElementById(this.data.confirm_password_field.div_id.mismatch);

        // blank field validator
        Shared.validateInputBlankFields(confirmPassword, divBlank, this.data.confirm_password_field.text.blank, this);

        if(this.valid) {
            confirmPassword.addEventListener("input", () => {
                let valueConfirm = confirmPassword.value.trim();
                let value = inputPassword.value.trim();

                if(valueConfirm !== value) {
                    // clear error
                    Shared.clearErrorMessages(confirmPassword, [divMismatch]);
                    // display error
                    Shared.displayErrorMessages(confirmPassword, divMismatch, this.data.confirm_password_field.text.mismatch);
                    this.valid = false;
                }

                else {
                    // clear error
                    Shared.clearErrorMessages(confirmPassword, [divMismatch]);
                    this.valid = true;
                }
            });
        }
    }

}