// import
import {Static} from "../../../utils/contansts.js";
import {Shared} from "../../../utils/shared.js";


/* Tracker Validator Class */
export class CheckInValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.PROFILE_TRACKER_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators()  {

        /* on-time validators */
        this.trackerCheckInFieldGenerator(
            "id_check_out_date_field", "id_checkin_display_message",
            "id_check_in_bttn");

        this.trackerCheckOutFieldValidate("check_out_date_field");

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
                /* clear check in mark */
                this.trackerClearingRecordFields("id_checkin_display_message")
            }
        });
    }

    /* blank fields */
    validateBlankFields() {
        /* boolean variable */
        let allValid = true;

        /* iterate over list of form field names */
        Static.PROFILE_TRACKER_BLANK_FIELDS.forEach((field) => {
            let inputField = this.form.elements.namedItem(field);

            /* collect empty fields */
            let fieldData = this.data[field];

            /* verify items are None or Disable status */
            if(!inputField || inputField.disable) {
                return;
            }

            /* verify items are Empty */
            if(inputField.disabled) {
                allValid = false;

                /* get the error div by Id from this.data */
                let errorDiv = document.getElementById(fieldData.div_id.disable);

                /* if error div by Id, display error text and style */
                if(errorDiv) {
                    Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.disable);
                }
            }
            else if(inputField.value.trim() === "") {
                allValid = false;

                if(fieldData) {
                    /* get the error div by Id from this.data */
                    let errorDiv = document.getElementById(fieldData.div_id.blank);

                    /* if error div by Id, display error text and style */
                    if(errorDiv) {
                        Shared.displayErrorMessages(inputField, errorDiv, fieldData.text.blank);
                    }
                }
            }
        });

        /* if this.valid, then set it to local boolean variable */
        if(this.valid) {
            this.valid = allValid;
        }
        /* return updated this.valid */
        return this.valid;
    }

    /* generate check in field and style */
    trackerCheckInFieldGenerator(checkOutInput, displayDivId, checkInButtonId) {
        let components = {
            "checkin_btn": document.getElementById(checkInButtonId),
            "checkin_div": document.getElementById(displayDivId),
            "checkout_input": document.getElementById(checkOutInput),
        }

        /* pass components dict to Shared.method to generate checkin mark */
        Shared.generateCheckInCheckOut(components);
    }

    /* checkout time validator */
    trackerCheckOutFieldValidate(fieldName) {
        /* setting up variables */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.check_out_date_field.div_id.blank);
        let divDisable = document.getElementById(this.data.check_out_date_field.div_id.disable);
        let divBefore = document.getElementById(this.data.check_out_date_field.div_id.before);

        /* validate no blank fields before submit form */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.check_out_date_field.text.blank, this);

        /* validate enable field before submit form */
        Shared.validateInputBlankFields(inputField, divDisable, this.data.check_out_date_field.text.disable, this);

        if(this.valid) {

            inputField.addEventListener("input", () => {
                let value = inputField.value;
                let checkInValue = localStorage.getItem("checkin");

                /* validate checkout is not less than or equal to check in */
                if(!Shared.comparingCheckInCheckOut(checkInValue, value)) {
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divBefore]);
                    /* display error messages */
                    Shared.displayErrorMessages(inputField, divBefore, this.data.check_out_date_field.text.before);
                    /* update valid var */
                    this.valid = false;
                }
                else {
                    /* set hidden input fields */
                    let hiddenFields = this.trackerSettingHiddenInputFields();
                    /* fetch data into hidden input fields */
                    Shared.fetchValuesHiddenInput(hiddenFields, checkInValue, value);
                    /* clear previous errors */
                    Shared.clearErrorMessages(inputField, [divBefore]);
                    /* update valid var */
                    this.valid = true;
                }
            });
        }
    }

    /* updating hidden input fields */
    trackerSettingHiddenInputFields() {
        /* collect Ids from hidden elements in form */
        let checkInInput = document.getElementById("id_checkin_value");
        let checkOutInput = document.getElementById("id_checkout_value");
        let hoursInput = document.getElementById("id_hours_value");

        /* return dict */
        return {
            "check_in": checkInInput,
            "check_out": checkOutInput,
            "hours": hoursInput,
        }
    }

    /* clearing records from screen */
    trackerClearingRecordFields(divId) {
        /* remove value at divId from localStore object */
        localStorage.removeItem("checkin");
        /* get value at divId and clean out text and style */
        let message = document.getElementById(divId);
        message.innerText = "";
        message.style.display = "none";
    }

}