# Customer Certificates

## About
I built this certificate management API using Python, Falcon (REST API framework), SQLAlchemy, PostgreSQL, Redis, and Docker. Tests are written with the `pytest` testing framework.

## Building / Running Locally
To build this application, it assumes you have `docker` and/or `docker-compose` installed (the latter is technically optional).

Simply `cd` into `customer_certificates` and run the following command:

```
docker-compose build api
```

The first time you run this API (or its test suites below), you will need to run the database migrations:

```
docker-compose run api alembic upgrade head
```

Finally, to run the application, execute:
```
docker-compose up api
```

The API is exposed at `localhost:9000`. You can change this in `docker-compose.yaml` or when you run the Docker container.

## Usage
This a HTTP-based / RESTful API. The only supported serialization format is JSON - ensure your `Accept` header is set properly / will accept a `application/json` response. Your `Content-Type` header should also be set to `application/json` and ensure you are sending a JSON request body (when applicable). Trying to use any other format will result in a 400-level error.

A few examples below demonstrate how to use the API with a REST / HTTP client (not exhaustive, please refer to the `swagger.yaml` file or even `app.py` for a complete list of endpoints):

### Users

Creating a user:

```
HTTP POST Request: /users/
{
	"name": "John Smith",
	"email": "jsmith@example.com",
	"password": "password"
}

HTTP Response:
{
	"id": 1
}
```

Getting a user:

```
HTTP GET Request: /users/1

HTTP Response:
{
	"name": "John Smith",
	"email": "jsmith@example.com"
}
```


### Certificates

Creating a certificate

```
HTTP POST Request: /users/1/certificates
{
	"private_key": [base64 encoded bytes],
	"body": "test body",
	"active": true
}

HTTP Response:
{
	"id": 1,
	"user_id": 1
}
```

Listing active certificates

```
HTTP GET Request: /users/1/certificates?active=true

HTTP Response:
[{
	"id": 1,
	"active": true
	"body": "test body"
}]
```

### Future Work / Other considerations

There are a bunch of things I would want some answers to / addressed if I were to release this app as a real production service. For example, how many users are expected, what are the expected read and write patterns (which may bring into questions optimizations like schema denormalization), the expected throughput, acceptable latency, SLAs, etc. This app and its dependencies (database, cache, etc) would absolutely need load-balancing, replication, possibly sharding or federation, more thoughtful caching, etc. applied to them if this was truly going to be deployed as a fault-tolerant, performant service.

A few particular things are also notably missing here:

* HTTPS / SSL Termination (data is insecurely transmitted right now)
	* Could use nginx for this or something similar
* Private Key Encryption (as waived in the prompt)
* Authentication (as waived in the prompt)
* Monitoring and Logging

These would all be requirements if this were to be deployed in the real world as well.

As far as coding design goes I would like to add at least the following:

* Error handling middleware (removing resource-level error handling).
* Better test coverage

### Some Design Decisions

* Foreign Keys
	* I thought it would be best to apply maximum data integrity constraints without knowing more about the application.
* Composite Index
	* I added a composite index on `user_id` and `id` on the certificates table.
* Hard Deletes
	* When a user or certificate is deleted, it is actually deleted. I would want to know more information about the system to make a fully-educated decision on what to do here - moving deleted users to a separate archive table or just simply using soft deletes may be better alternatives if given more context.
* Caching
	* I implemented some pretty basic object caching in front of SQL Alchemy with Redis and Dogpile.
	* I actually disabled this for the certificates GET endpoint as I was having some invalidation bugs and couldn’t fix them in time.
	* There may be better caching strategies to employ here given more context.
* Integer IDs / Primary Key
	* Would need to know what was consuming the API to make the best decision here. Ints seemed satisfactory and performant for the time being (will allow for more than 2 billion rows on its own).
* Base64-encoded Bytes
	* Sending raw bytes (private keys) is done by Base64-encoding them in a JSON object. Again, there are other options (like `multipart/form-data`), but I think is pretty RESTful and not too space inefficient for private keys (~33% expansion).

## Tests
Tests are run in their own container so they can rely on their own environment / config block. By default, the setup is mostly the same as the `lcl` environment, but you could change it as you see fit.

To run all test suites, just run the following (beware of pesky Docker caching if you end up changing anything). Make sure you have run the database migrations as noted above afterwards as well:

```
docker-compose up api-test
```

You can also run individual suites by overriding the default command for the container - see PyTest docs for how that’s done.

## Structure
The API entry point is defined in the `app.py` file.

#### Models

I have defined my DB schema using the `SQLAlchemy` ORM - if you are unfamiliar, this basically is an object-oriented schema definition which creates a mapping to actual DB table schemas in the background. You can find these in the `models` dir. I also used `Alembic` to run / keep track of migrations (more on that below).

#### Resources / Endpoints

I used Swagger to define my API spec - this mostly just served as a planning template and reference it is not ingested by the Falcon framework. You might find it helpful to get an good overview of how I designed the API.

You can find each resource in the `resources` dir. They are mapped / registered to actual paths in the `app.py` file. I have added docstrings wherever possible to make understanding easier.

#### Services

I have defined several helper services in the `services` dir. These are used for setting the db, cache, config blocks, etc.

#### Middleware

There are a few middleware layers that I added - they enforce a JSON-only serialization format (to keep things simple) and ensure atomic transactions for each request. You can find them in the `middleware` dir.

## Running Migrations
The app uses `Alembic` in tandem with `SQLAlchemy` to manage migrations. Whenever you make changes to the models, you will need to generate a migration script using the  `alembic` cli and apply it manually - i.e. the application code will not manage your schema changes for you :)

General usage:

	1. Make some changes to your models.
	2. Run your api (ensuring your database is up to date).
	3. Autogenerate migrations from models.
		1. Alembic is hooked into your database config and knows the location of your db instance as well as your models.
		2. Alembic will also utilize your `env` environment variable to figure out which db config it should use.

Detailed usage with `docker-compose`:

To make a new migration after adjusting your model code:

1. Make sure your API and DB are built:

`docker-compose build api`

2. Run migration auto generator - provide description of the migration.

`docker-compose run api alembic revision --autogenerate -m "migration description"`

3. Follow steps below to apply this new migration.

To apply the latest migration (or initialize your database) using `docker-compose`:

1. Make sure your API and DB are built:

`docker-compose build api`

2. Apply the latest `head` of revisions to your database by running: 

`docker-compose run api alembic upgrade head`

Without `docker-compose`:

You can more or less run the same commands sans the `docker-compose run/up` prefix in whatever context you need. If you are using vanilla docker, just supply the command when running the container.
