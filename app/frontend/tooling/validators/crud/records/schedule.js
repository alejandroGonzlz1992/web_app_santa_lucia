// import
import {Static} from '../../../utils/contansts.js';
import {Shared} from '../../../utils/shared.js';


/* Schedule Validator form fields Class */
export class ScheduleValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.SCHEDULE_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {
        /* on-time validators */
        this.scheduleStatusFieldValidate('schedule_type');

        this.scheduleStartTimeFieldValidate(
            'schedule_start_time', 'schedule_end_time', 'schedule_type');

        this.scheduleEndTimeFieldValidate(
            'schedule_start_time', 'schedule_end_time', 'schedule_type');

        this.scheduleCreateDateFieldValidate('schedule_create_date');

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
        Static.SCHEDULE_BLANK_FIELDS.forEach((item) => {
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

    /* schedule type field */
    scheduleStatusFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.schedule_type.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.schedule_type.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.schedule_type.text.status);
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

    /* schedule start date field */
    scheduleStartTimeFieldValidate(fieldStart, fieldEnd, fieldType) {
        /* get input element and div ids */
        let inputStartField = this.form.elements.namedItem(fieldStart);
        let inputEndField = this.form.elements.namedItem(fieldEnd);
        let inputTypeField = this.form.elements.namedItem(fieldType);

        let divBlank = document.getElementById(this.data.schedule_start_time.div_id.blank);
        let divAfter = document.getElementById(this.data.schedule_start_time.div_id.after);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputStartField, divBlank, this.data.schedule_start_time.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputStartField.addEventListener("input", () => {

                /* get input field values and convert them */
                let time = Shared.convertingStartTimeEndTimeFormat(
                    inputStartField, inputEndField, "[name='schedule_total_hours']")

                let type = inputTypeField.value;

                /* compare start time vs end time */
                if(type !== "Nocturna" && time.start > time.end){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputStartField, [divAfter]);
                    /* display error message */
                    Shared.displayErrorMessages(inputStartField, divAfter, this.data.schedule_start_time.text.after);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputStartField, [divAfter]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* schedule end date field */
    scheduleEndTimeFieldValidate(fieldStart, fieldEnd, fieldType) {
        /* get input element and div ids */
        let inputStartField = this.form.elements.namedItem(fieldStart);
        let inputEndField = this.form.elements.namedItem(fieldEnd);
        let inputTypeField = this.form.elements.namedItem(fieldType);

        let divBlank = document.getElementById(this.data.schedule_end_time.div_id.blank);
        let divBefore = document.getElementById(this.data.schedule_end_time.div_id.before);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputEndField, divBlank, this.data.schedule_end_time.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputEndField.addEventListener("input", () => {

                /* get input field values and convert them */
                let time = Shared.convertingStartTimeEndTimeFormat(
                    inputStartField, inputEndField, "[name='schedule_total_hours']")

                let type = inputTypeField.value;

                /* compare start time vs end time */
                if(type !== "Nocturna" && time.end < time.start){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputEndField, [divBefore]);
                    /* display error message */
                    Shared.displayErrorMessages(inputEndField, divBefore, this.data.schedule_end_time.text.before);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputEndField, [divBefore]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* schedule create date field */
    scheduleCreateDateFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.schedule_create_date.div_id.blank);
        let divBefore = document.getElementById(this.data.schedule_create_date.div_id.before);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.schedule_create_date.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divBefore, this.data.schedule_create_date.text.before);
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