// import
import {Static} from "../../utils/contansts.js";
import {Shared} from "../../utils/shared.js";


/* Evaluations Employee/Supervisor Validator Class */
export class EvaluationValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.EVALUATION_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    initEventValidators(){

        /* on-time validators */
        this.evaluationEmployeeSelectFieldValidate('evaluation_user_name_field');

        this.evaluationRadioButtonItemFieldValidate();

        this.evaluationFeedbackDetailFieldValidate('evaluation_detail');

        /* form submission */
        this.form.addEventListener("submit", (e) => {

            /* prevent form auto submission */
            e.preventDefault();

            this.valid = true;

            /* run both validators */
            let nonRadioOk = this.validateBlankFields();
            let radiosOk = (typeof this._checkRadios === "function") ? this._checkRadios() : true;

            this.valid = nonRadioOk && radiosOk;

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
        Static.EVALUATION_BLANK_FIELDS.forEach((item) => {
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

    /* evaluation employee/supervisor select */
    evaluationEmployeeSelectFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.evaluation_user_name_field.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.evaluation_user_name_field.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.evaluation_user_name_field.text.status);
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

    /* radio item option select */
    evaluationRadioButtonItemFieldValidate() {
        /* get the error div by id */
        let errorDiv = document.getElementById('id_radio_button_not_check');

        /* set up dict (key:value) for question id -> [radio buttons] for each row */
        let buildGroups = () => {
          let map = new Map();
          let radios = this.form.querySelectorAll('input[type="radio"][name^="ratings["]');

          radios.forEach(rb => {
              let mark = rb.name.match(Static.REGEX_RADIO_BUTTONS);
              if(!mark){
                  return;
              }

              let qId = mark[1];
              if(!map.has(qId)){
                  map.set(qId, []);
              }
              map.get(qId).push(rb);
          });
          return map;
        };

        /* check that all the groups have at least one of its element radios checked */
        let areAllGroupsChecked = () => {
            let groups = buildGroups();

            for(let [, arr] of groups){
                if(!arr.some(r => r.checked)) {
                    return false;
                }
            }
            return true;
        };

        /* clear/display the single global error div */
        let updateGlobalError = (ok) => {
            if(!errorDiv){
                return;
            }
            errorDiv.style.display = ok ? "none" : "block";
            errorDiv.textContent = ok ? "" : this.data.question_item_field.text.check;
        };

        /* live: when radio button changes */
        this.form.addEventListener("change", (e) => {

            if(e.target.matches('input[type="radio"][name^="ratings["]')){
                updateGlobalError(areAllGroupsChecked());
            }
        });

        /* onsubmit: update this.valid global var and verify radio buttons */
        this._checkRadios = () => {
            let ok = areAllGroupsChecked();
            updateGlobalError(ok);
            return ok;
        };
    }

    /* feedback input field */
    evaluationFeedbackDetailFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.evaluation_detail.div_id.blank);
        let divChars = document.getElementById(this.data.evaluation_detail.div_id.chars);
        let divLength = document.getElementById(this.data.evaluation_detail.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.evaluation_detail.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(!Static.REGEX.address.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divLength]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.evaluation_detail.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.FEEDBACK_MIN_LENGTH) {
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.evaluation_detail.text.length);
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

}