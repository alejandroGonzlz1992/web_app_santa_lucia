// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Evaluations Enable Validator Class */
export class EnableValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.INABILITY_ENABLE_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.inabilityEnableStatusFieldValidate("inability_status_field");

        this.inabilityEnableCheckboxConfirmFieldValidate("delete_switch_field");

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

        /* traverse list of blank name fields */
        Static.INABILITY_ENABLE_BLANK_FIELDS.forEach((field) => {
            /* get element by name */
            let inputField = this.form.elements.namedItem(field);

            /* validate input field not blank of none */
            if(!inputField || inputField.value.trim() === "not_select") {
                /* change flag */
                allValid = false;

                /* get the div element using its name attr */
                let fieldData = this.data[field];

                if(fieldData) {

                    /* get element div */
                    let errorDiv = document.getElementById(fieldData.div_id.status);

                    if(errorDiv) {
                        /* display error mssg */
                        Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.status);
                    }
                }
            }
            else if(inputField.type === "checkbox") {
                /* get the element value */
                if(!inputField.checked) {
                    allValid = false;

                    /* get the div element using its name attr */
                    let fieldData = this.data[field];
                    if(fieldData) {

                        /* get element div */
                        let errorDiv = document.getElementById(fieldData.div_id.confirm);
                        if(errorDiv) {
                            /* display error mssg */
                            Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.confirm);
                        }
                    }
                }
            }
        });

        if(this.valid) {
            this.valid = allValid;
        }
        return this.valid;
    }

    /* status dropdown select */
    inabilityEnableStatusFieldValidate(fieldName) {
        /* get element by name attr */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.inability_status_field.div_id.status);

        /* blank field listener */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.inability_status_field.text.status, this);

        /* event listener */
        if(this.valid) {

            /* input field */
            inputField.addEventListener("input", () => {
                /* collect values */
                let value = inputField.value.trim();

                if(value === "not_select") {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divStatus]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divStatus, this.data.inability_status_field.text.status);
                    /* update flag */
                    this.valid = false;

                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divStatus]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* checkbox confirmation */
    inabilityEnableCheckboxConfirmFieldValidate(fieldName) {
        /* get element by name attr */
        let inputField = this.form.elements.namedItem(fieldName);
        let divConfirm = document.getElementById(this.data.delete_switch_field.div_id.confirm);

        /* blank field listener */
        Shared.validateInputBlankFields(inputField, divConfirm, this.data.delete_switch_field.text.confirm, this);

        /* event listener */
        if(this.valid) {
            /* input field */
            inputField.addEventListener("change", () => {

                if(!inputField.checked) {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divConfirm]);
                    /* display errors */
                    Shared.displayErrorMessages(inputField, divConfirm, this.data.delete_switch_field.text.confirm);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(inputField, [divConfirm]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}