/*
|--------------------------------------------------------------------------
| Datetimepicker Tempus Dominus
|--------------------------------------------------------------------------
| @link https://getdatepicker.com/6/functions/display.html
| @link https://github.com/Eonasdan/tempus-dominus
|
| Helper Links
| @link https://momentjs.com/timezone/
| @link https://devhints.io/datetime
| @link https://www.timeanddate.com/worldclock/converter.html
| @link https://www.jqueryscript.net/time-clock/date-time-picker-tempus-dominus.html
|
| Tempus Dominus is the upgraded version of eonasdan-bootstrap-datetimepicker
|
| This functionality loads the tempus dominus library and extrapolates the universal date from the event.
| We will then return the string on button submission.
|
| Bind datepicker w/ element so that any datetime or date field will use this library. If there is an element, and it
| has a pristine date, set convert it into ISO, otherwise set the date as null.
| If we want to modify the date we simply get the dirty date and convert that to ISO so that when a button is clicked we
| have a UTC ISO formatted date that is sent to the server.
| Example: "2023-04-20T16:05:37.342Z"
|
*/

import $ from 'jquery';
import moment from 'moment-timezone';

const BACKSPACE_VALUE = 8;
let selectTimezone = document.getElementById('timezone');

export default class {
    constructor(el, opts) {
        const $el = $(el);
        const element = $el[0];

        if (element) {
            // Define datepicker for any date or datetime inputs
            const picker = new tempusDominus.TempusDominus(element, opts);
            const saveBtn = document.getElementById('save-btn');
            const downloadBtn = document.getElementById('download-btn');

            let isoDate = '';
            let timezone = this.initTimeZone(element);
            const pristineValue = picker.dates.picked[0];

            // On page load get UTC ISO date of pristine value.  If datetime is empty, ignore.
            if (pristineValue) {
                isoDate = this.getUtcIsoDate(pristineValue, timezone);
            }

            // If datepicker becomes dirty, convert date to UTC then convert that date to ISO before we save.
            picker.subscribe(tempusDominus.Namespace.events.change, event => {
                
                // The variable event.date is the dirty date.  Convert to UTC then format to ISO
                isoDate = this.getUtcIsoDate(event.date, timezone);

                // NOTE: If no button is detected ignore the element.  This is mainly for date elements that
                // are used as filters.  The filtering of dates will be performed by searchable.js.
            });

            // Listen to timezone selector.  If changed run logic to update datetime, display new date
            if (selectTimezone) {
                selectTimezone.addEventListener('change', () => {
                    // Get updated timezone
                    timezone = selectTimezone.value;
                    moment.tz.setDefault(timezone);

                    // Is there a date to update? When creating a session the initial value is undefined so only run
                    // this if the ISO date has been set.
                    if (isoDate) {
                        // Update input field w/ new localized datetime, make sure format is like pristine format
                        const displayDate = this.getDisplayDate(isoDate, timezone);
                        picker.dates.setFromInput(displayDate);
                    }
                });
            }

            // Assuming save button is on the UI check if data is pristine or dirty to send the proper value
            if (saveBtn !== null) {
                saveBtn.addEventListener('click', function () {
                    element.value = isoDate;
                });
            }

            // Listen for the download button if you're on the Reports page.
            if (downloadBtn != null) {
                downloadBtn.addEventListener('click', function () {
                    element.value = isoDate;
                });
            }

            // Clear the input field to start over.
            element.addEventListener('keydown', function (event) {
                if (event.key === 'Backspace' || event.keyCode === BACKSPACE_VALUE || event.which === BACKSPACE_VALUE) {
                    picker.dates.setFromInput('');
                }
            });
        }
    }

    /**
     * Check if the GMT matches the local machine timezone settings.  If not, manipulate the string and replace the offset
     * with the given local datetime offset and create a completely new JS date.
     *
     * NOTE: Javascript uses your system preference timezone to determine your GMT.  This is fine if you're in the timezone
     * of your country, but if you are not the dates will be inaccurate.  What this function does is check
     * the machine's timezone to match the timezone of your country and if it doesn't match it adjusts
     * so that no matter where you are in the world, your local display datetime will convert when sending to the server.
     *
     * @param value
     * @param timezone
     * @returns {*}
     */
    getUtcIsoDate(value, timezone) {
        const machineTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        const machineOffset = this.getTimezoneOffset(machineTimezone);
        const localeOffset = this.getTimezoneOffset(timezone);

        // Convert value to string
        if (machineOffset !== localeOffset) {
            value = this.convertDatetimeToStr(value);
        }

        // Return date after converting to UTC and formatted that to ISO
        return moment.tz(value, timezone).utc().format();
    }

    /**
     * Converts ISO date string to local date time string to parse for display.  The display date is what is put in the
     * input field that the user will see when the timezone is manually changed.
     *
     * @param value
     * @param timezone
     * @returns {string}
     */
    getDisplayDate(value, timezone) {
        return moment.tz(value, 'UTC').clone().tz(timezone).format('YYYY-MM-DD hh:mm a');
    }

    /**
     * Get the timezone offset to know how to offset the local time for country.
     *
     * @param timezone
     * @returns {number}
     */
    getTimezoneOffset(timezone) {
        const offset = moment.tz(new Date(), timezone).utcOffset();

        return offset / 60;
    }

    /**
     * Get timezone either by retrieving the attribute or the ID.
     *
     * @param element
     * @returns {string}
     */
    initTimeZone(element) {
        let timezone = 'UTC';

        if (element.attributes['data-timezone']) {
            timezone = element.attributes['data-timezone'].value;
        } else if (selectTimezone) {
            timezone = selectTimezone.value;
        }

        moment.tz.setDefault(timezone);

        return timezone;
    }

    /**
     * Returns string from date in YYYY-MM-DD HH:mm:ss
     * If the value has been cleared out with a backspace key input then skip the conversion process and return undefined.
     *
     * @param date
     * @returns {string}
     */
    convertDatetimeToStr(date) {
        if (date === undefined) {
            return undefined;
        }

        let year = date.getFullYear();
        let month = ('0' + (date.getMonth() + 1)).slice(-2);
        let day = ('0' + date.getDate()).slice(-2);
        let hours = ('0' + date.getHours()).slice(-2);
        let minutes = ('0' + date.getMinutes()).slice(-2);
        let seconds = ('0' + date.getSeconds()).slice(-2);

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
}
