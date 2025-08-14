import {ajaxRequest} from "../core.js";

const inputs = {
    countrySelect: $('#country_select'),
    citySelect: $('#city_select')
}

Inputmask({
    "mask" : "(999) 999-9999",
    "clearIncomplete": true,
    "placeholder": "(___)-___-____",
}).mask("#phone_input");


function getCountries() {
    ajaxRequest('/get_countries/', {}, 'GET')
        .then(res => {
            inputs.countrySelect.append('<option value="">Seçiniz</option>');
            res.map(country => {
               inputs.countrySelect.append(`<option value="${country.fields.country_id}" data-kt-select2-country="assets/media/flags/afghanistan.svg">${country.fields.emoji} ${country.fields.name}</option>`)
            });
        });
}

function getCities(country_id) {
    ajaxRequest(`/get_cities/${country_id}/`, {}, 'GET')
        .then(res => {
            inputs.citySelect.empty().append('<option value="">Seçiniz</option>');
            res.map(city => {
               inputs.citySelect.append(`<option value="${city.pk}">${city.fields.name}</option>`)
            });
        });
}

getCountries();
inputs.countrySelect.change(()=> getCities(inputs.countrySelect.val()));