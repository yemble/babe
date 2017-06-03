# build a back-end

Minimal template for a web service:

* PostgreSQL database container
  * Simple sql scripts to initialize with schema and data
* Python [Flask](http://flask.pocoo.org/) app container
  * REST API endpoint for a smart front end to talk to the database
  * Custom API *hello* endpoint example
  * Custom actions to do whatever with *hello* example
  * [Jinja2](http://jinja.pocoo.org/) templated html pages with *hello* example
  * Static file serving fallback
 
## Quick start

1. Install [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/)
1. Copy / fork this code into your own workspace or git repo
1. Run `docker-compose up`

This will start up the database and app containers, logging to stdout.

Load http://localhost:8000/ to access the app.
REST example: http://localhost:8000/api/v1/data/sprocket/id/1

## Customizing

* `sql/*.sql` initializes the database
* `app/app.py` has the http route (path) definitions
* `app/actions.py` has custom http action handlers
* `app/api.py` has rest api handlers
* Static files go in `app/static`
* Template files go in `app/templates`
