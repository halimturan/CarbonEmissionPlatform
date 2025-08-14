const images = {
    visa: $('#visa_img'),
    mastercard: $('#master_img'),
    amex: $('#amex_img')
}

const inputs = {
    company_id: $('#company_id'),
    card_name: $('#card_name'),
    card_number: $('#card_number'),
    card_expiry_month: $('#card_expiry_month'),
    card_expiry_year: $('#card_expiry_year'),
    card_cvv: $('#card_cvv'),
    card_number_warning: $('#card_number_warning'),
    informCheck: $('#inform_check'),
}

const buttons = {
    submitBtn: $('#pay_btn')
}

function formControl() {
    let status = 0;
    inputs.card_name.val() ? status += 1 : null;
    inputs.card_number.val() ? status += 1 : null;
    inputs.card_expiry_month.val() ? status += 1 : null;
    inputs.card_expiry_year.val() ? status += 1 : null;
    inputs.card_cvv.val() ? status += 1 : null;
    return status === 5
}

function validateCardNumber() {
    images.amex.addClass('d-none').removeClass('d-block');
    images.visa.addClass('d-none').removeClass('d-block');
    images.mastercard.addClass('d-none').removeClass('d-block');
    images.amex.addClass('d-none').removeClass('d-block');
    images.visa.addClass('d-none').removeClass('d-block');
    images.mastercard.addClass('d-none').removeClass('d-block');
    const cardNumber = inputs.card_number.val();
    let sum = 0;
    let isEven = false;

    for (let i = cardNumber.length - 1; i >= 0; i--) {
        let digit = parseInt(cardNumber.charAt(i), 10);

        if (isEven) {
            digit *= 2;
            if (digit > 9) {
                digit -= 9;
            }
        }

        sum += digit;
        isEven = !isEven;
    }
    let cardType = null;
    const patterns = {
        visa: /^4[0-9]{12}(?:[0-9]{3})?$/,
        mastercard: /^5[1-5][0-9]{14}$/,
        amex: /^3[47][0-9]{13}$/,
        discover: /^6(?:011|5[0-9]{2})[0-9]{12}$/,
    };

    for (const cType in patterns) {
        if (patterns[cType].test(cardNumber)) {
            cardType = cType;
        }
    }
    if(cardType){
        inputs.card_number_warning.removeClass('d-block').addClass('d-none');
        images[cardType].addClass('d-block').removeClass('d-none');
    } else {
        inputs.card_number_warning.addClass('d-block').removeClass('d-none');
    }
}

function submitProcess() {
    const status = formControl();
    const companyValidator = inputs.company_id.val();
    if (!companyValidator) {
        Swal.fire({
            text: "Firma bilgilerini girmeniz gerekmektedir!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Anlaşıldı!",
            customClass: {
                confirmButton: "btn btn-primary"
            }});
    } else if (status && companyValidator) {
        createOrder();
    } else {
        Swal.fire({
            text: "Lütfen tüm alanları doldurduğunuzdan emin olunuz!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Anlaşıldı!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    }
}

function createOrder() {
     $.ajax({
        url : '/tr/online_islemler/odeme/' + this.inputs.slug.val(),
        type : 'POST',
        data : {
            'user_name' : this.inputs.user.name.val(),
            'user_lastname' : this.inputs.user.lastName.val(),
            'user_identity' : this.inputs.user.identity.val(),
            'user_phone' : parseInt(this.inputs.user.phone.val().replace("(", "").replace(")", "").replace("-", "").replace("-", "")),
            'user_mail' : this.inputs.user.mail.val(),
            'user_address': this.inputs.user.address.val(),
            'user_gender': this.inputs.user.gender.val(),
            'user_birth_date': this.inputs.user.birthDate.val(),
            'card_number' : this.inputs.card.number.val(),
            'card_month' : this.inputs.card.month.val(),
            'card_year' : this.inputs.card.year.val()
        },
        success : data => {
            for (const key in data) {
                this.form.append($("<input>").attr("type", "hidden").attr("name", key).val(data[key]));
            }
            this.form.submit();
        },
        error : function(){
            Swal.fire({
                text: "Bir hata oluştu!",
                icon: "error",
                buttonsStyling: false,
                confirmButtonText: "Anlaşıldı!",
                customClass: {
                    confirmButton: "btn btn-primary"
                }
            });
        }
    });
}

inputs.card_number.keyup(() => validateCardNumber());
inputs.informCheck.change(() => {
    inputs.informCheck.is(':checked') ? buttons.submitBtn.removeAttr('disabled') : buttons.submitBtn.attr('disabled', 'disabled');
});
buttons.submitBtn.click(() => submitProcess());
