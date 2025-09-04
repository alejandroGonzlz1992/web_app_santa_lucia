// import
import {Static} from '../../../utils/contansts.js';
import {Shared} from '../../../utils/shared.js';


/* Questions Validator form fields Class */
export class QuestionsValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.QUESTIONS_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {
        /* on-time validators */
        this.evaluationTypeFieldValidate('evaluation_type');

        this.evaluationQuestionFieldValidate('evaluation_question');

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
        Static.QUESTIONS_BLANK_FIELDS.forEach((item) => {
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

    /* evaluation type field */
    evaluationTypeFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.evaluation_type.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.evaluation_type.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.evaluation_type.text.status);
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

    /* evaluation question field */
    evaluationQuestionFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.evaluation_question.div_id.blank);
        let divChars = document.getElementById(this.data.evaluation_question.div_id.chars);
        let divLength = document.getElementById(this.data.evaluation_question.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.evaluation_question.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(!Static.REGEX.evaluation.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divLength]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.evaluation_question.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.EVALUATION_QUESTION_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.evaluation_question.text.length);
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