function setQuantity() {
    function range(start, end) {
        return Array(end - start + 1).fill().map((_, idx) => start + idx)
    }
    const countInput = range(0, 20);
    countInput.forEach(function (id) {
        const inputQuantity = document.querySelector(`#id_details-${id}-quantity`);
        const inputKayak = document.querySelector(`#id_details-${id}-kayak`);
        if (inputQuantity) {
            const selectKayak = inputKayak.options[inputKayak.selectedIndex].text;
            const maxQuantity = selectKayak.match(/\d+/)[0];
            console.log(inputKayak);
            inputQuantity.setAttribute('max', maxQuantity)
        }
    });
}
