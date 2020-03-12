(function ($) {
    $('.booking-container').on('click', function (e) {
      e.preventDefault();
      const bookingHeader = this;
      const elementTab = this.querySelector('.tab-text');

      if (bookingHeader.classList.contains('active')) {
          bookingHeader.classList.remove('active');
          elementTab.firstElementChild.innerHTML = 'Rozwiń'
      }
      else {
          bookingHeader.classList.add('active');
          elementTab.firstElementChild.innerHTML = 'Schowaj'
      }

      const bookingDetail = this.nextElementSibling;
        if (bookingDetail.classList.contains('hide')) {
            bookingDetail.classList.remove('hide')
        }
        else {
            bookingDetail.classList.add('hide')
        }
    });
    $('.nav-pills li a').filter(function(){return this.href==location.href}).parent().addClass('active').siblings().removeClass('active');
    $('.nav-pills li a').click(function(){
			$(this).parent().addClass('active').siblings().removeClass('active')
    })
})(jQuery);