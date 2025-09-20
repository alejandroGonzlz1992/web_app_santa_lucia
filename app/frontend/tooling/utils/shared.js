// import
import {Static} from './contansts.js';
import {Utils} from "./utils.js";

/* Shared utilities functions for validators */
export class Shared {

    /* display error message */
    static displayErrorMessages(input, div, text) {
        /* modify inner attributes */
        input.style.border = "1px solid rgba(231, 76, 60, 0.6)";
        input.style.boxShadow = "0 0 8px rgba(231, 76, 60, 0.4)";
        div.style.display = "block";
        div.textContent = text;
    }

    /* clear error message */
    static clearErrorMessages(input, div, text) {
        /* modify inner attributes */
        input.style.border = "";
        input.style.boxShadow = "";
        div.forEach((field) => {
            field.style.display = "none";
        });
    }

    /* display error message radio button*/
    static displayCheckboxErrorMessage(targetElement, divField, text) {
        if(targetElement?.style) {
            targetElement.style.outline = "2px solid rgba(231, 76, 60, 0.8)";
            targetElement.style.boxShadow = "0 0 6px rgba(231, 76, 60, 0.8)";
        }
        if(divField?.style) {
            divField.style.display = "block";
            divField.textContent = text ?? "";
        }
    }

    /* validate input blank fields */
    static validateInputBlankFields(input, div, text, form) {
        /* while clicking on input, display style and error message */
        input.addEventListener("click", () => {
            if(input.value.trim() === ""){
                Shared.displayErrorMessages(input, div, text);
                form.valid = false;
            }
        });
        /* clear out style and error message after info is inputed */
        input.addEventListener("input", () => {
            if(input.value.trim() !== ""){
                Shared.clearErrorMessages(input, [div]);
                form.valid = true;
            }
        });
    }

    /* validate current date vs input date */
    static inputDateAndCurrentDateFormat(field){
        /* convert input to date object and format it */
        let createDate = new Date(field.value);
        let currentDate = new Date();

        createDate.setHours(0, 0, 0, 0);
        currentDate.setHours(0, 0, 0, 0);

        /* adjust create date to one day */
        createDate.setDate(createDate.getDate() + 1);

        return {"create": createDate, "current": currentDate};
    }

    /* formatting birthday date */
    static birthdayInputFormatting(field){
        /* convert input to date object and current date */
        let birthdayDate = new Date(field.value);
        let currentDate = new Date();

        currentDate.setHours(0, 0, 0, 0);

        /* underage and overage male, overage female */
        let underAge = new Date(currentDate);
        underAge.setFullYear(underAge.getFullYear() - Static.UNDERAGE);

        let overAgeMan = new Date(currentDate);
        overAgeMan.setFullYear(overAgeMan.getFullYear() - Static.RETIRE_AGE_MAN);

        let overAgeWoman = new Date(currentDate);
        overAgeWoman.setFullYear(overAgeWoman.getFullYear() - Static.RETIRE_AGE_WOMAN);

        /* return */
        return {"birth": birthdayDate, "under": underAge, "man": overAgeMan, "woman": overAgeWoman}
    }

    /* enable and disable password field values */
    static enableAndDisablePasswordField(passwordFields, buttonFields){
        /* define password and button lists */
        let passwords = [];
        let buttons = [];

        /* traverse passwords input fields and append element to list */
        passwordFields.forEach((passw) => {
            /* get element */
            let field = document.querySelector(passw);
            /* append */
            passwords.push(field);
        });

        /* traverse button fields and append element to list */
        buttonFields.forEach((button) => {
            /* get element */
            let bttn = document.querySelector(button);
            /* append */
            buttons.push(bttn);
        });

        /* combine both lists */
        let combine = passwords.map((field, index) => [field, buttons[index]]);

        /* event listener on combine list */
        combine.forEach(([passw, toggle]) => {
            if(passw && toggle) {
                /* event listener */
                toggle.addEventListener("click", function() {
                    /* change input attribute if button is click (hide or unhide) */
                    let type = passw.getAttribute("type") === "password" ? "text" : "password";
                    passw.setAttribute("type", type);

                    /* update eye-slash icon base on type change of input */
                    let icon = toggle.querySelector("i");
                    if(icon){
                        icon.classList.toggle("fa-eye");
                        icon.classList.toggle("fa-eye-slash");
                    }
                });
            }
        });
    }

    /* converting start time and end time field values */
    static convertingStartTimeEndTimeFormat(start, end, field) {
        /* get values */
        let [startTime, endTime] = [start.value, end.value];

        /* get hours and minutes from start and end in int value */
        let [startHours, startMinutes] = startTime.split(":").map(Number);
        let [endHours, endMinutes] = endTime.split(":").map(Number);

        /* get start and end time totals in minutes */
        let startTimeMinutesTotal = startHours * 60 + startMinutes;
        let endTimeMinutesTotal = endHours * 60 + endMinutes;

        /* measure the hours between start and end totals */
        let hoursTotal = (endTimeMinutesTotal - startTimeMinutesTotal) / 60;

        /* update hidden hours HTML input field */
        let scheduleHours = document.querySelector(field);

        if(scheduleHours) {
            scheduleHours.value = Math.round(hoursTotal);
        }

        /* return values */
        return {"start": startTimeMinutesTotal, "end": endTimeMinutesTotal, "hours": hoursTotal}
    }

    /* disable and auto update second payment date */
    static disableEnablePayDateField(type, firstDate, secondDate, hiddenField) {

        /* collect elements by id */
        let [pType, first, second, hidden] = [
            document.getElementById(type),
            document.getElementById(firstDate),
            document.getElementById(secondDate),
            document.getElementById(hiddenField),
        ];

        /* inner function for styling */
        let handleChange = () => {
            if(pType.value === "Mensual") {
                /* add styling */
                Utils.stylingDateField("change", second, first);
            }
            else {
                /* add styling */
                Utils.stylingDateField("unchange", second, first);
            }
        };
        /* keep second date sync while editing the first date */
        let handleFirstDateChange = () => {
            if(pType.value === "Mensual") {
                second.value = first.value;
                hidden.value = second.value;
            }
        };

        /* attach event listeners */
        pType.addEventListener("change", handleChange);
        first.addEventListener("input", handleFirstDateChange);

        /* init on page load */
        handleChange();
    }

    /* format payment dates objects */
    static firstPayDateSecondPayDate(start, end) {

        /* format input to date add +1 day */
        let startDate = new Date(start.value);
        startDate.setDate(startDate.getDate() + 1);
        startDate.setHours(0, 0, 0, 0);

        let endDate = new Date(end.value);
        endDate.setDate(endDate.getDate() + 1);
        endDate.setHours(0, 0, 0, 0);

        return {"start": startDate, "end": endDate};

    }

    /* generate and style check in and check out marks */
    static generateCheckInCheckOut(components) {

        /* load checkin mark if already in localStorage */
        let checkinStore = localStorage.getItem("checkin");

        if(checkinStore) {
            Utils.injectHTMLStyleCheckIn(components, checkinStore);
        }

        /* checkin button event */
        components["checkin_btn"].addEventListener("click", () => {

            /* store current Date information and apply dd/mm/yyyy am/pm format */
            let nowTime = new Date();
            let formatTime = Utils.formatTime(nowTime);

            /* store checkin in localStorage */
            localStorage.setItem("checkin", formatTime);

            /* display checkin in mark */
            Utils.injectHTMLStyleCheckIn(components, formatTime);

            /* enable checkout input field */
            components["checkout_input"].value = formatTime;
            components["checkout_input"].disabled = false;
        });
    }

    /* report dates formatting */
    static reportDatesFormatting(start, end) {

        /* format input to date add +1 day */
        let currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);

        let startDate = new Date(start.value);
        startDate.setDate(startDate.getDate() + 1);
        startDate.setHours(0, 0, 0, 0);

        let endDate = new Date(end.value);
        endDate.setDate(endDate.getDate() + 1);
        endDate.setHours(0, 0, 0, 0);

        return {"start": startDate, "end": endDate, "current": currentDate};
    }

    /* radio button clear error */
    static cleanRadioErrorMessage(targetElement, divField) {
        if (targetElement?.style) {
        targetElement.style.outline = "none";
        targetElement.style.boxShadow = "none";
        }
        if (divField?.style) {
            divField.style.display = "none";
            divField.textContent = "";
        }
    }

    /* checkbox clear error */
    static cleanCheckboxErrorMessage(inputField, errorDiv) {
        if(errorDiv) {
            errorDiv.style.display = "none";
		    errorDiv.innerText = "";
        }
        inputField.style.outline = "";
	    inputField.style.boxShadow = "";
    }

    /* compare check in and check out field */
    static comparingCheckInCheckOut(checkIn, checkOut) {
        /* convert checkIn/checkOut value to 24h format */
        let to24HourCheckIn = Utils.convertCheckIn24hModel(checkIn);

        /* convert checkIn and checkOut in minutes */
        let checkInMinutes = Utils.convertToMinutes(to24HourCheckIn);
        let checkOutMinutes = Utils.convertToMinutes(checkOut);

        /* return true if checkout minutes >= checkin minutes */
        return checkOutMinutes >= checkInMinutes;

    }

    /* fetch time values to hidden fields */
    static fetchValuesHiddenInput(fields, checkInValue, checkOutValue) {

        /* convert checkIn value to 24h format */
        let checkIn24HourModel = Utils.convertCheckIn24hModel(checkInValue);
        /* convert checkOut value to 12h format */
        let checkOutValueAmPm = Utils.convertCheckOut12hModel(checkOutValue);
        /* calculate hours between */
        let totalHour = Utils.calculateHours(checkIn24HourModel, checkOutValue);

        /* set values to hidden fields */
        fields["check_in"] = checkInValue;
        fields["check_out"] = checkOutValueAmPm;
        fields["hours"] = totalHour;

    }

}