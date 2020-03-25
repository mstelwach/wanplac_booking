function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix, button) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        if (this.nodeName == 'INPUT' || this.nodeName == 'BUTTON') {
            this.setAttribute('disabled', 'disabled')
        }
        var name = $(this).attr('name');
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('-');
    // document.querySelector('.btn-primary').removeAttribute('disabled');
    return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
function rangeList(start, end) {
    return Array(end - start + 1).fill().map((_, idx) => start + idx)
}
function setDisabledOption(button) {
    const selectElement = $(button).closest('.form-row').find('select')[0];
    const nextFormRow = $(button).closest('.form-row')[0].nextElementSibling;
    const nextSelectElement = $(nextFormRow).find('select')[0];
    nextSelectElement.options[selectElement.selectedIndex].setAttribute('disabled', 'disabled');
    $(selectElement).css('pointer-events','none');
    const selectArrow = selectElement.nextElementSibling;
    selectArrow.remove();
}
function deleteDisabledOption(button, prefix) {
    const rangeKayak = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    const selectElement = $(button).closest('.form-row').find('select')[0];
    rangeList(0, rangeKayak-1).forEach(function (id) {
        const selectKayak = document.querySelector(`#id_details-${id}-kayak`);
        selectKayak.options[selectElement.selectedIndex].removeAttribute('disabled');
    })
}
function totalCostKayak(button) {
    const selectKayak = $(button).closest('.form-row').find('select')[0];
    const quantityKayak = parseInt($(button).closest('.form-row').find('input').val());
    const priceKayak = parseInt(selectKayak.options[selectKayak.selectedIndex].innerText.replace(/.*\D(?=\d)|\D+$/g, ""));
    const submitReservation = document.querySelector('.btn-primary');
    let totalCost = parseInt(submitReservation.innerText.replace(/^\D+|\D+$/g, ""));
    if ($(button).hasClass('add-form-row')) {
        totalCost += priceKayak * quantityKayak;
    }
    else if ($(button).hasClass('remove-form-row')) {
        totalCost -= priceKayak * quantityKayak;
    }
    submitReservation.textContent = `Zapłać i zarezerwuj | Kwota: ${totalCost} PLN`;
}
function validateKayak(selectOption) {
    const selectKayak = selectOption.options[selectOption.selectedIndex];
    const idQuantity = String(selectOption.id);
    const inputQuantity = document.querySelector(`#id_details-${idQuantity.match(/\d+/)[0]}-quantity`);
    inputQuantity.removeAttribute('disabled');
    $.ajax({
        url: '/reservation/create/',
        data: {
            selectKayakId: selectKayak.value,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            $(inputQuantity).html(data)
        }
    })
}
function validateQuantity(selectQuantity) {
    const buttonAdd = $(selectQuantity).closest('.form-row').find('button')[0];
    const buttonReservation = document.querySelector('.btn-primary');
    let totalCost = parseInt(buttonReservation.innerText.replace(/^\D+|\D+$/g, ""));
    if (selectQuantity.value > 0) {
        const selectKayak = $(selectQuantity).closest('.form-row').find('select')[0];
        const priceKayak = parseInt(selectKayak.options[selectKayak.selectedIndex].innerText.replace(/.*\D(?=\d)|\D+$/g, ""));
        let previousValue = $(selectQuantity).attr('data-old') !== typeof undefined? $(selectQuantity).attr('data-old') :"";
        let currentValue = $("option:selected",selectQuantity).text();
        $(selectQuantity).attr('data-old',currentValue);
        if (!previousValue) {
            previousValue = 0
        }
        buttonAdd.removeAttribute('disabled');
        buttonReservation.removeAttribute('disabled')
    }
    else {
        buttonReservation.setAttribute('disabled', 'disabled');
        if ($(buttonAdd).hasClass('add-form-row')) {
            buttonAdd.setAttribute('disabled', 'disabled')
        }
    }
    console.log(totalCost);
    buttonReservation.textContent = `Zapłać i zarezerwuj | Kwota: ${totalCost} PLN`;
}
function validatePhone(valueNumber) {
    if ($(valueNumber).intlTelInput("isValidNumber")) {
        let getFullNumber = $(valueNumber).intlTelInput("getNumber");
        $(valueNumber).val(getFullNumber);
    }
}