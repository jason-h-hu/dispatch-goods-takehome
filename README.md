# Running

## Prerequisites

- python3
- pip3
- a running instance of PostgreSQL. If you don't, I followed [this tutorial](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/) to start a local instance. Specifically, I ran an image with the following: `docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=directory_app
-d -p 5432:5432 postgres`

## In `/server`

1. Activate the python env with `mkvirtualenv [name]`
2. Install dependencies with `pip install -r requirements.txt`
3. Initialize env variables `export DATABASE_URL=[URL]`. If you're copying my docker instance from the prerequisites, that URL is `postgres://postgres:mysecretpassword@localhost:5432/directory_app`
4. Start the server with `python3 manage.py runserver`, using the URL specific to your PostgreSQL instance.
5. Populate the DB by running `python manage.py migrate`
6. Navigate to `http://127.0.0.1:8000/admin/` to see the admin page. You may need to run `python manage.py createsuperuser` to login.

## In `/client`

1. Install all dependencies with `npm install`
2. Start the client server with `ng serve --open`. This should open a window at `http://localhost:4200/`
3. You are now free to upload CSVs

## Testing

### Manual Testing

1. In `http://localhost:4200/`, you can upload a valid CSV. You can then go to `http://127.0.0.1:8000/admin/` and see that all the entries have been added to the DB
2. In `http://localhost:4200/`, after you upload a valid CSV, you see that many QR codes. To test the QR code, you can use a [third-party parser like this](https://dnschecker.org/qr-code-scanner.php) to decode the data, and then manually navigate to the URL. You should see the corresponding record
3. In `http://localhost:4200/`, you get an error message if you upload a CSV that:
   - doesn't have all the fields `first_name`, `last_name`, `age`, `address` in the header
   - has entries that are missing a field

### Automated Testing

In `/server`, run `python3 manage.py test`.

# Discussion

## Note for the Reviewer

This project made use of two scripts:

- `django-admin startproject [project]`
- `ng new [project]`

To generate the server and the client respectively. As a result, most of the code is generic and non-unique to this project. Project-specific code can be found in:

- `client/src/app/*`
- `server/qrsite/views/*`
- `server/qrsite/templates`
- `server/qrsite/models.py`
- `server/qrsite/tests.py`
- `server/qrsite/urls.py`

## JSON v. URL in the QR Code

QR codes can encode arbitrary data, and I was choosing between whether to encode a stringified JSON object of the record, or whether to encode a URL that pointed to the record. I decided to do the latter because:

- It slightly future-proofs the design, if we ever add additional fields to each record
- It doesn't require a dedicated client: Smartphones will automatically direct to a URL from a QR code

## Dynamically-Generated v. Static QR Codes

Rather than generating and saving a QR code upon ingesting the CSV, I instead generate the QR code just-in-time, when we receive a request for the PNG. This has a modest performance cost, since Django now has to serve these as in-memory requests rather than as a static asset. However, this significantly simplifies the implementation, since I don't have to worry about persisting PNGs (or cleaning them up). In the future, this web-app might need to support more sophisticated record management, a CDN, an event-driven architecture, etc. Because all these would affect the right way to manage static QR codes, we can keep this hacky, nimble solution until those needs are clarified.

## Angular App v. Django Template Views

My initial implementation of the UI used Django's view templates, rather than defining a separate Angular app. To be honest, Angular felt like overkill. The requirements weren't complex enough to necessitate Angular's dependency injection system, and because the Angular app is being served from a different address, it led to the hack of needing to disable CORS protection.

I left the implementation of the Django views as part of the repo (it was fun learning a completely new library, and I was a bit sentimental). It can be accessed as `http://127.0.0.1:8000/`.

**Open Question:** If this were a real-world project, I'd ask why was using Angular part of the technical requirements. Keeping the UI entirely in Django would significantly shrink the complexity of the app. Do we have a clear vision of how the product will grow, to justify the extra initial overhead?

## Next Steps

The current app is a proof-of-concept at best, and needs significant investment to before being remotely production ready:

1. Add styling to the UIs
2. Re-enable the protections against CORS. Because the UI and backend are being served from different addresses, I had to disable this to allow them to communicate. We could do this by making Django responsible for serving the UI, or by having the client server relaying all requests to Django.
3. Remove the hard-coded URLs for the HTTP requests in the client.
4. Define a build pipeline and container images for deployment

# Disclosures

Because this was my first time using Django and my first time in a decade writing python, I made extensive use of external resources such as ChatGPT, and [this tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) from MDN.

The prompt also recommended "a few hours of focused engineering work". I took a bit more than a few hours, since I was relatively unconstrained with my own time, and was happy to go down rabbitholes to try and better understand best-practices in Django.
