(function ($) {
    $('.booking-tab').on('click', function (e) {
      e.preventDefault();
      const bookingTab = this;
      const bookingContainer = $(bookingTab).closest('.booking-container')[0];
      const bookingDetail = $(bookingContainer).next();
      $(bookingDetail).toggleClass('hide');

      // CHANGE TEXT BUTTON
      $(bookingTab).html($(bookingTab).html() == '<b>Ukryj szczegóły rekrutacji</b>' ?
      '<b>Kliknij, aby rozwinąć szczegóły rekrutacji</b>' : '<b>Ukryj szczegóły rekrutacji</b>');
    });

    $('.nav-pills li a').filter(function(){return this.href==location.href}).parent().addClass('active').siblings().removeClass('active');
    $('.nav-pills li a').click(function(){
			$(this).parent().addClass('active').siblings().removeClass('active')
    })
})(jQuery);