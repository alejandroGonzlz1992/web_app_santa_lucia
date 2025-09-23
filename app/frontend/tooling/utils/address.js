/* import */

/* addressing class */
export class Addressing {

    constructor(cantons, districts) {
        this.allCantons = (cantons ?? []).map(c => ({
            id: Number(String(c.id ?? c._cant_id).trim()),
            name: c.name ?? c._cant_name,
            prov_id: Number(String(c.prov_id ?? c.id_province ?? c._prov_id).trim()),
        }));
        this.allDistricts = (districts ?? []).map(d => ({
            id: Number(String(d.id ?? d._dist_id).trim()),
            name: d.name ?? d._dist_name,
            cant_id: Number(String(d.cant_id  ?? d.id_canton  ?? d._cant_id).trim()),
        }));

        /* init event address */
        this.initEventAddressing();

    }

    /* event addressing */
    initEventAddressing() {
        /* define vars for html elements */
        let provinceElem = document.getElementById('id_province_field');
        let cantonElem = document.getElementById('id_canton_field');
        let districtElem = document.getElementById('id_district_field');

        /* clear input fields */
        this.resetInputSelectFields(cantonElem, "Seleccione un Cantón");
        this.resetInputSelectFields(districtElem, "Seleccione un Distrito");

        /* Province -> Cantons */
        provinceElem.onchange = (e) => {
            let provinceId = Number(String(e.target.value || '').trim());

            /* clear inputs */
            this.resetInputSelectFields(cantonElem, "Seleccione un Cantón");
            this.resetInputSelectFields(districtElem, "Seleccione un Distrito");

            if(!provinceId || provinceId === "not_select") return;

            let cantons = this.allCantons
                .filter(c => c.prov_id === provinceId)
                .sort((a, b) => a.name.localeCompare(b.name));

            /* fill the input with the item selected */
            this.fillSelectedElements(cantonElem, cantons);
        };

        /* Cantons -> Districts */
        cantonElem.onchange = (e) => {
            let cantonId = Number(String(e.target.value || '').trim());

            console.log(cantonId);
            console.log(typeof cantonId);

            /* clear input fields */
            this.resetInputSelectFields(districtElem, "Seleccione un Distrito");

            if(!cantonId || cantonId === "not_select") return;

            let districts = this.allDistricts
                .filter(d => d.cant_id === cantonId)
                .sort((a, b) => a.name.localeCompare(b.name));

            this.fillSelectedElements(districtElem, districts);

        };

        /* auto fill if province is already selecte */
        if(provinceElem.value && provinceElem.value !== 'not_select') {
            provinceElem.dispatchEvent(new Event('change'));
        }
    }

    /* reset input select fields */
    resetInputSelectFields(element, placeholder) {
        element.innerHTML = `<option value='not_select' selected>${placeholder}</option>`;
    }

    /* fill out selected element */
    fillSelectedElements(element, items) {
        for(let i = 0; i < items.length; i++) {
            let option = document.createElement("option");
            option.value = items[i].id;
            option.textContent = items[i].name;
            element.appendChild(option);
        }
    }

}