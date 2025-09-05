// import


/* filtering class per criteria */
export class FilterSearching {

    /* constructor */
    constructor(elements) {
        this.input = elements["input"];
        this.search = elements["search"];
        this.reset = elements["reset"];
        this.row = elements["row"];

        /* init even filter */
        this.initEventFiltering();
    }

    /* event filtering */
    initEventFiltering() {

        /* filter results */
        this.filterInputOptions();

        /* reset results */
        this.resetResultOptions();
    }

    /* filter dropdown option */
    filterInputOptions() {

        /* get elements button and dropdown item */
        let filterButton = document.getElementById(this.search);
        let dropdownItem = document.getElementById(this.input);

        /* confirm both elements exits */
        if(filterButton && dropdownItem) {

            /* get elements button and dropdown item */
            filterButton.addEventListener("click", () => {

                /* get value from dropdown item and the table rows */
                let valueItem = dropdownItem.value.trim();
                let tableRows = document.querySelectorAll("table tbody tr");

                /* traverse table rows and filter by dropdown item value and row child field */
                tableRows.forEach(row => {

                    /* get the value provided at this.row param */
                    let cellValue = row.querySelector(`td:nth-child(${this.row})`);
                    let textAtCell = cellValue ? cellValue.textContent.trim() : "";

                    if(textAtCell === valueItem) {
                        row.style.display = "";
                    }
                    else {
                        row.style.display = "none";
                    }
                })
            });
        }
    }

    /* reset results */
    resetResultOptions() {

        /* get element reset button */
        let resetButton = document.getElementById(this.reset);

        if(resetButton) {

            /* reset button event listener */
            resetButton.addEventListener("click", () => {
                let rowFields = document.querySelectorAll("table tbody tr");

                rowFields.forEach(row => {
                    row.style.display = "";
                });
            });
        }
    }

}