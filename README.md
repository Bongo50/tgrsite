# tgrsite
tabletop games and roleplaying society's website
For "feature list", see [#2](https://github.com/ashbc/tgrsite/issues/2)

## Notes for running, mainly so Finnbar doesn't forget
* To set up, run. This is needed if you change the models also:
```
python manage.py makemigrations bugreports forum exec messaging rpgs users
python manage.py migrate
```
* To run the actual server: ```python manage.py runserver```. This watches changes (but **is not** aware of new files!)!
* If debug = False, set to true. You possibly need to add an allowed host, but that's trivial. (tgrsite/settings.py)
* To do fab admin stuff:
    * ```python manage.py createsuperuser```
    * Then log onto <root>/admin
    * Go into site, add a Member, setting its equivalent to the created one
