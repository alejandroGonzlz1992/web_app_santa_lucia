// import
import {Static} from '../../../utils/contansts.js';
import {Shared} from '../../../utils/shared.js';


/* Users Validator form fields Class */
export class UsersValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.USER_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {
        /* on-time validators */
        this.userIdentificationFieldValidate('user_identification');

        this.userNameFieldValidate('user_name');

        this.userLastNameFieldValidate('user_lastname');

        this.userLastName2FieldValidate('user_lastname2');

        this.userBirthdayFieldValidate('user_birthday', 'user_gender');

        this.userGenderFieldValidate('user_gender');

        this.userMaritalStatusFieldValidate('user_marital_status');

        this.userChildrenFieldValidate('user_children');

        this.userEmailFieldValidate('user_email');

        this.userPhoneFieldValidate('user_phone');

        this.userRoleFieldValidate('user_role');

        this.userApprovalFieldValidate('user_approval');

        this.userGrossIncomeFieldValidate('user_gross_income');

        this.userCreateUpdateDateFieldValidate('user_create_date');

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
        Static.USER_BLANK_FIELDS.forEach((item) => {
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

    /* user name */
    userNameFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_name.div_id.blank);
        let divChars = document.getElementById(this.data.user_name.div_id.chars);
        let divLength = document.getElementById(this.data.user_name.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_name.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_name.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.NAME_LASTNAME_LASTNAME2_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.user_name.text.length);
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

    /* user lastname */
    userLastNameFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_lastname.div_id.blank);
        let divChars = document.getElementById(this.data.user_lastname.div_id.chars);
        let divLength = document.getElementById(this.data.user_lastname.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_lastname.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_lastname.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.NAME_LASTNAME_LASTNAME2_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.user_lastname.text.length);
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

    /* user lastname2 */
    userLastName2FieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_lastname2.div_id.blank);
        let divChars = document.getElementById(this.data.user_lastname2.div_id.chars);
        let divLength = document.getElementById(this.data.user_lastname2.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_lastname2.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_lastname2.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length < Static.NAME_LASTNAME_LASTNAME2_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.user_lastname2.text.length);
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

    /* user birthday */
    userBirthdayFieldValidate(fieldBirthday, fieldGender){
        /* get input element and div ids */
        let birthdayField = this.form.elements.namedItem(fieldBirthday);
        let genderField = this.form.elements.namedItem(fieldGender);
        let divBlank = document.getElementById(this.data.user_birthday.div_id.blank);
        let divUnder = document.getElementById(this.data.user_birthday.div_id.under);
        let divMan = document.getElementById(this.data.user_birthday.div_id.man);
        let divWoman = document.getElementById(this.data.user_birthday.div_id.woman);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(birthdayField, divBlank, this.data.user_birthday.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            birthdayField.addEventListener("input", () => {
                /* get input field value */
                let dateField = Shared.birthdayInputFormatting(birthdayField);
                let gender = genderField.value.trim();
                /* validate only letters are input */
                if(dateField.birth > dateField.under){
                    /* clear prev error message */
                    Shared.clearErrorMessages(birthdayField, [divMan, divWoman]);
                    /* display error message */
                    Shared.displayErrorMessages(birthdayField, divUnder, this.data.user_birthday.text.under);
                    /* update flag */
                    this.valid = false;
                }
                else if(gender === "Masculino" && dateField.birth < dateField.man){
                    /* clear prev error message */
                    Shared.clearErrorMessages(birthdayField, [divUnder, divWoman]);
                    /* display error message */
                    Shared.displayErrorMessages(birthdayField, divMan, this.data.user_birthday.text.man);
                    /* update flag */
                    this.valid = false;
                }
                else if(gender === "Femenino" && dateField.birth < dateField.woman){
                    /* clear prev error message */
                    Shared.clearErrorMessages(birthdayField, [divUnder, divMan]);
                    /* display error message */
                    Shared.displayErrorMessages(birthdayField, divWoman, this.data.user_birthday.text.woman);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(birthdayField, [divUnder, divMan, divWoman]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* user gender */
    userGenderFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.user_gender.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.user_gender.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.user_gender.text.status);
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

    /* user martial status */
    userMaritalStatusFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.user_marital_status.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.user_marital_status.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.user_marital_status.text.status);
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

    /* user children */
    userChildrenFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_children.div_id.blank);
        let divChars = document.getElementById(this.data.user_children.div_id.chars);
        let divMax = document.getElementById(this.data.user_children.div_id.max);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_children.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                let toInt = parseInt(value);
                /* validate only letters are input */
                if(!Static.REGEX.only_numbers.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divMax]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_children.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(toInt > Static.MAX_CHILDREN){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divMax, this.data.user_children.text.max);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divChars, divMax]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* user email */
    userEmailFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_email.div_id.blank);
        let divFormat = document.getElementById(this.data.user_email.div_id.format);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_email.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                /* validate only letters are input */
                if(!Static.REGEX.email_format.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divFormat, this.data.user_email.text.format);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* user phone */
    userPhoneFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_phone.div_id.blank);
        let divChars = document.getElementById(this.data.user_phone.div_id.chars);
        let divLength = document.getElementById(this.data.user_phone.div_id.length);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_phone.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_phone.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(value.length !== Static.PHONE_LENGTH){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divLength, this.data.user_phone.text.length);
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

    /* user role */
    userRoleFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.user_role.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.user_role.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.user_role.text.status);
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

    /* user gross income */
    userGrossIncomeFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_gross_income.div_id.blank);
        let divChars = document.getElementById(this.data.user_gross_income.div_id.chars);
        let divMin = document.getElementById(this.data.user_gross_income.div_id.min);
        let divMax = document.getElementById(this.data.user_gross_income.div_id.max);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_gross_income.text.blank, this);

        if(this.valid){
            /* add event listener to input field */
            inputField.addEventListener("input", () => {
                /* get input field value */
                let value = inputField.value.trim();
                let toInt = parseInt(value);
                /* validate only letters are input */
                if(!Static.REGEX.only_numbers.test(value)){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divMin, divMax]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divChars, this.data.user_gross_income.text.chars);
                    /* update flag */
                    this.valid = false;
                }
                else if(toInt < Static.GROSS_INCOME_MIN){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars, divMax]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divMin, this.data.user_gross_income.text.min);
                    /* update flag */
                    this.valid = false;
                }
                else if(toInt > Static.GROSS_INCOME_MAX){
                    /* clear prev error message */
                    Shared.clearErrorMessages(inputField, [divChars, divMin]);
                    /* display error message */
                    Shared.displayErrorMessages(inputField, divMax, this.data.user_gross_income.text.max);
                    /* update flag */
                    this.valid = false;
                }
                else {
                    /* clear error message */
                    Shared.clearErrorMessages(inputField, [divChars, divMin, divMax]);
                    /* update flag */
                    this.valid = true;
                }
            });
        }
    }

    /* user create/update date */
    userCreateUpdateDateFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.user_create_date.div_id.blank);
        let divBefore = document.getElementById(this.data.user_create_date.div_id.before);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divBlank, this.data.user_create_date.text.blank, this);

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
                    Shared.displayErrorMessages(inputField, divBefore, this.data.user_create_date.text.before);
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

    /* user approval */
    userApprovalFieldValidate(fieldName){
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.user_approver.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.user_approver.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.user_approver.text.status);
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

}