# WANPLAC RESERVATION PANEL


Simple booking kayak panel. WanPlac Booking is a panel that will make kayak booking easier and faster.

## Tasks
- Creation Form
  In an easy and transparent way we can create a reservation for an interesting day.

- PayU online payment
  We can pay for the reservation thanks to the available PayU payment (function in creation).

- E-mail confirmation
  After completing the reservation form, we send a link confirming the booking (function in creation).

- Booking list
  It displays information about every reservation we have made.
    - Delete reservation
    - Click an reservation to update & details view

- List of kayaks and available trails
  Basic information about available kayaks and trails that will help us make a choice when making a reservation.
  
 ### Help in the implementation of the task

* [Django] - https://docs.djangoproject.com/en/3.0/
  #### Libraries DJANGO
      * [django-bootstrap3] - https://django-bootstrap3.readthedocs.io/en/latest/
      * [django-celery] - https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
      * [django-getpaid] - https://django-getpaid.readthedocs.io/en/latest/
      * [django-widget-tweaks] - https://github.com/jazzband/django-widget-tweaks
      * [django-phonenumber-field] - https://github.com/stefanfoulis/django-phonenumber-field
* [PostgreSQL] - https://www.postgresql.org/docs/
* [Pickadate.js] - https://amsul.ca/pickadate.js/
* [Intl-tel-input] - https://github.com/jackocnr/intl-tel-input

#### RUN PANEL
1. Install the requirements for the package:
  ```sh
    pip install -r requirements.txt
  ```
2. Make and apply migrations
  ```sh
    python manage.py makemigrations
    python manage.py migrate
  ```
3. Run the server
  ```sh
    python manage.py runserver
  ```
4. Access from the browser at http://127.0.0.1:8000

##### Demonstrative Image
<p align="center">
  <img src="https://github.com/mstelwach/wanplac_booking/blob/master/demonstrative_image.png">
</p>
