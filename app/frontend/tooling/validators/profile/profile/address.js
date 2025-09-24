// import
import {Static} from "../../../utils/contansts.js";
import {Shared} from "../../../utils/shared.js";


/* Contact Info Update Validator Class */
export class ContactValidator {

    /* constructor */
    constructor(idForm) {
        this.form = document.getElementById(idForm);
        this.valid = true;
        this.data = Static.PROFILE_CONTACT_INFO_FORM_DICT;

        /* init event validators */
        this.initEventValidators();
    }

    /* event validators */
    initEventValidators() {

        /* on-time validators */
        this.contactInfoProvinceSelectFieldValidate("province_field");

        this.contactInfoCantonSelectFieldValidate("canton_field");

        this.contactInfoDistrictSelectFieldValidate("district_field");

        this.contactInfoAddressDetailFieldValidate("address_detail_field");

        this.contactInfoPostalCodeFieldValidate("postal_code_field");

        this.contactInfoEmailFieldValidate("email_field");

        this.contactInfoPhoneFieldValidate("phone_field");

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
        Static.PROFILE_CONTACT_INFO_BLANK_FIELDS.forEach((item) => {
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

    /* province select validation */
    contactInfoProvinceSelectFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.province_field.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.province_field.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.province_field.text.status);
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

    /* canton select validation */
    contactInfoCantonSelectFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.canton_field.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.canton_field.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.canton_field.text.status);
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

    /* district select validation */
    contactInfoDistrictSelectFieldValidate(fieldName) {
        /* get input element and div ids */
        let inputField = this.form.elements.namedItem(fieldName);
        let divStatus = document.getElementById(this.data.district_field.div_id.status);

        /* validate on-time blank fields */
        Shared.validateInputBlankFields(inputField, divStatus, this.data.district_field.text.status, this);

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
                    Shared.displayErrorMessages(inputField, divStatus, this.data.district_field.text.status);
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

    /* address detail validation */
    contactInfoAddressDetailFieldValidate(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.address_detail_field.div_id.blank);
        let divChars = document.getElementById(this.data.address_detail_field.div_id.chars);
        let divLength = document.getElementById(this.data.address_detail_field.div_id.length);

        // listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.address_detail_field.text.blank, this);

        if(this.valid) {
            inputField.addEventListener("input", () => {
                let value = inputField.value.trim();

                if(!Static.REGEX.address.test(value)) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divLength]);
                    // display error
                    Shared.displayErrorMessages(inputField, divChars, this.data.address_detail_field.text.chars);
                    this.valid = false;
                }
                else if(value.length < Static.ADDRESS_LENGTH) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divChars]);
                    // display error
                    Shared.displayErrorMessages(inputField, divLength, this.data.address_detail_field.text.length);
                    this.valid = false;
                }
                else {
                    // clear errors
                    Shared.clearErrorMessages(inputField, [divChars, divLength]);
                    this.valid = true;
                }
            });
        }
    }

    /* postal code validation */
    contactInfoPostalCodeFieldValidate(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.postal_code_field.div_id.blank);
        let divNumber = document.getElementById(this.data.postal_code_field.div_id.number);
        let divLength = document.getElementById(this.data.postal_code_field.div_id.length);

        // listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.postal_code_field.text.blank, this);

        // listener
        inputField.addEventListener("input", () => {
            let value = inputField.value.trim();

            if(!Static.REGEX.only_numbers.test(value)) {
                // clear previous error
                Shared.clearErrorMessages(inputField, [divLength]);
                // display error
                Shared.displayErrorMessages(inputField, divNumber, this.data.postal_code_field.text.number);
                this.valid = false;
            }
            else if(value.length !== Static.POSTAL_CODE_LENGTH) {
                // clear previous error
                Shared.clearErrorMessages(inputField, [divNumber]);
                // display error
                Shared.displayErrorMessages(inputField, divLength, this.data.postal_code_field.text.length);
                this.valid = false;
            }
            else {
                // validation pass
                Shared.clearErrorMessages(inputField, [divNumber, divLength]);
                this.valid = true;
            }
        });
    }

    /* email validation */
    contactInfoEmailFieldValidate(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.email_field.div_id.blank);
        let divFormat = document.getElementById(this.data.email_field.div_id.format);

        // listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.email_field.text.blank, this);

        if(this.valid) {
            inputField.addEventListener("input", () => {
                let value = inputField.value.trim();

                if(!Static.REGEX.email_format.test(value)) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    // display error
                    Shared.displayErrorMessages(inputField, divFormat, this.data.email_field.text.format);
                    this.valid = false;
                }
                else {
                    // clear erros
                    Shared.clearErrorMessages(inputField, [divFormat]);
                    this.valid = true;
                }
            });
        }
    }

    /* phone validation */
    contactInfoPhoneFieldValidate(fieldName) {
        let inputField = this.form.elements.namedItem(fieldName);
        let divBlank = document.getElementById(this.data.phone_field.div_id.blank);
        let divChars = document.getElementById(this.data.phone_field.div_id.chars);
        let divLength = document.getElementById(this.data.phone_field.div_id.length);

        // listener
        Shared.validateInputBlankFields(inputField, divBlank, this.data.phone_field.text.blank, this);

        if(this.valid) {
            inputField.addEventListener("input", () => {
                let value = inputField.value.trim();

                if(!Static.REGEX.only_numbers.test(value)) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divLength]);
                    // display error
                    Shared.displayErrorMessages(inputField, divChars, this.data.phone_field.text.chars);
                    this.valid = false;
                }
                else if(value.length !== Static.PHONE_LENGTH) {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divChars]);
                    // display error
                    Shared.displayErrorMessages(inputField, divLength, this.data.phone_field.text.length);
                    this.valid = false;
                }
                else {
                    // clear previous error
                    Shared.clearErrorMessages(inputField, [divChars, divLength]);
                    this.valid = true;
                }
            });
        }
    }

}