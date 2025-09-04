// import
import { Static } from "./contansts.js";

// utils functions
export class Utils {

    static stylingDateField(status, date, payDate) {

        if(status === "change") {
            /* style input field */
            date.disabled = true;
            date.style.backgroundColor = "#e9ecef";
            date.value = payDate.value;
        }
        else if(status === "unchange") {
            /* style input field */
            date.disabled = false;
            date.style.backgroundColor = "";
        }
    }

    static formatTime(date) {

        /* collect hours and minutes from input date */
        let hours = date.getHours();
        let minutes = date.getMinutes();

        /* define if hour is am or pm */
        let ampm = hours >= 12 ? 'pm' : 'am';

        /* define hours to 24h format */
        hours = hours % 12 || 12;

        /* append initial 0 to minutes -> 05 min */
        minutes = minutes.toString().padStart(2, '0');

        /* return formatted time */
        return `${hours}:${minutes} ${ampm}`;
    }

    static injectHTMLStyleCheckIn(component, timeStr) {

        /* remove any style from element */
        component.checkin_div.removeAttribute("style");

        /* add new style to element along with timeStr */
        component.checkin_div.innerHTML = `
            <div class="card shadow-sm h-100">
                <div class="card-body text-center">
                    <h6 class="card-subtitle mb-2 text-muted">Ingreso registrado a las: </h6>
                    <h4 class="card-text text-primary">${timeStr}</h4>
                </div>
            </div>
        `;
    }

    static dateVacations(start, end) {
        /* set input start/end/current date to date object */
        let startDate = new Date(start.value);
        let endDate = new Date(end.value);
        let currentDate = new Date();

        /* adjust start/end date to +1 day */
        startDate.setDate(startDate.getDate() + 1);
        endDate.setDate(endDate.getDate() + 1);

        /* remove hh and minutes */
        startDate.setHours(0, 0, 0, 0);
        endDate.setHours(0, 0, 0, 0);
        currentDate.setHours(0, 0, 0, 0);

        /* return dict */
        return {"start": startDate, "end": endDate, "current": currentDate};
    }

    static dateStartExtraHour(start) {
        /* set input start date to date object */
        let startDate = new Date(start.value);
        /* adjust start date to +1 day */
        startDate.setDate(startDate.getDate() + 1);
        /* remove hh and minutes */
        startDate.setHours(0, 0, 0, 0);

        /* set current date */
        let currentDate = new Date();
        /* remove hh and minutes */
        currentDate.setHours(0, 0, 0, 0);

        /* return dict */
        return {"start": startDate, "current": currentDate};
    }

    static fetchingDaysVacation(dates, field, inputField) {
        /* get the days */
        let totalDays = Math.max((dates["end"] - dates["start"]) / Static.MILLISECONDS_PER_DAY + 1);
        /* fetch value into element */
        let fieldValue = document.getElementById(field);

        if(fieldValue) {
            fieldValue.value = totalDays;
        }

        let el = document.querySelector(`input[name="${inputField}"]`);
        if (el) el.value = String(totalDays);

    }

    static convertCheckIn24hModel(timeStore) {

        /* split localStorage checkIn time by time/am-pm */
        let [time, amPm] = timeStore.split(" ");

        /* split time by hh/mm and parse them to int base 10 */
        let [hours, minutes] = time.split(":");

        let intHours = parseInt(hours, 10);
        let intMins = parseInt(minutes, 10);

        /* check if checkIn time is pm and not 12 in hh */
        if(amPm === "pm" && intHours !== 12) {
            /* add +12h to amPm to get 24h */
            intHours += 12;
        }
        /* check if checkIn time is am and 12 in hh */
        else if(amPm === "am" && intHours === 12) {
            /* set hours to 0h */
            intHours = 0;
        }

        /* return formatted mark in 24h */
        return `${intHours.toString().padStart(2, "0")}:${intMins}`;
    }

    static convertToMinutes(timeString) {
        /* split input time string by hh, cast it to Number */
        let [hours, minutes] = timeString.split(":").map(Number);
        /* return hh in minutes + minutes */
        return hours * 60 + minutes;
    }

    static convertCheckOut12hModel(time24hour) {

        /* split input 24h value into hh:mm */
        let [hours, minutes] = time24hour.split(":").map(Number);

        /* set up am/pm based on hours value */
        let amPm = hours >= 12 ? 'pm': 'am';

        /* convert hours from 24h to 12h model */
        hours = hours % 12 || 12;

        /* return formatted 12h mark */
        return `${hours}:${minutes.toString().padStart(2, "0")} ${amPm}`;

    }

    static calculateHours(checkIn24hour, checkOut24hour) {

        /* split hour/minutes values from checkin and checkout input */
        let [h1, m1] = checkIn24hour.split(":").map(Number);
        let [h2, m2] = checkOut24hour.split(":").map(Number);

        /* convert hour values in minutes */
        let checkInMinutes = h1 * 60 + m1;
        let checkOutMinutes = h2 * 60 + m2;

        /* calculate difference between minutes */
        let diffMinutes = checkOutMinutes - checkInMinutes;

        /* return */
        return (diffMinutes / 60).toFixed(2);

    }

}