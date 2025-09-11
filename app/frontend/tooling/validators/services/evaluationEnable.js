// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Evaluations Employee/Supervisor Enable Validator Class */
export class EvaluationEnableValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.EVALUATION_ENABLE_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    initEventValidators() {
        /* on-time validators */
        this.evaluationEnableStatusFieldValidate('evaluation_type');

        this.evaluationEnableCheckboxConfirmFieldValidate('confirm_switch_field');

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
        Static.EVALUATION_ENABLE_BLANK_FIELDS.forEach((item) => {
            /* current div element */
            let fieldData = this.data[item];

            /* dropdown and input field validation */
            let inputField = this.form.elements.namedItem(item);
            let confirmField = this.form.elements.namedItem("confirm_switch_field");
            let confirmDiv = document.getElementById(this.data.confirm_switch_field.div_id.confirm)

            if(!confirmField.checked) {
                /* change flag */
                allValid = false;
                /* display error message */
                Shared.displayCheckboxErrorMessage(confirmField, confirmDiv, this.data.confirm_switch_field.text.confirm);
            }

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
        });

        /* validate flag status */
        if(this.valid) {
            this.valid = allValid;
        }
        return this.valid;




    }

    /* status dropdown select */
    evaluationEnableStatusFieldValidate(fieldName) {
        /* get element by name attr */
        let selectField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.evaluation_type.div_id.status);

        /* blank field listener */
        Shared.validateInputBlankFields(selectField, divStatus, this.data.evaluation_type.text.status, this);

        /* event listener */
        if(this.valid) {
            selectField.addEventListener("input", () => {

                /* collect value */
                let value = selectField.value.trim();

                if(value === "not_select") {
                    /* clear prev errors */
                    Shared.clearErrorMessages(selectField, [divStatus]);
                    /* display error msgs */
                    Shared.displayErrorMessages(selectField, divStatus, this.data.evaluation_type.text.status);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.clearErrorMessages(selectField, [divStatus]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* checkbox confirmation */
    evaluationEnableCheckboxConfirmFieldValidate(fieldName) {
        /* get element by name attr */
        let checkBoxField = this.form.elements.namedItem(fieldName);
        let divConfirm = document.getElementById(this.data.confirm_switch_field.div_id.confirm);

        /* event listener */
        if(this.valid) {
            checkBoxField.addEventListener("change", () => {

                if(!checkBoxField.checked) {
                    /* clear prev errors */
                    Shared.cleanCheckboxErrorMessage(checkBoxField, divConfirm);
                    /* display error msgs */
                    Shared.displayCheckboxErrorMessage(checkBoxField, divConfirm, this.data.confirm_switch_field.text.confirm);
                    /* update flag */
                    this.valid = false;
                }

                else {
                    /* clear prev errors */
                    Shared.cleanCheckboxErrorMessage(checkBoxField, divConfirm);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

}