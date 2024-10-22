# Dockerizing Django with Postgres, Gunicorn, and Redis

## Want to use this project?

### Development

Uses the default Django development server.

1. Create virtual environment
2. Install requierements.dev.txt
3. Make migrations and create super user
4. Open another terminal, install dependences tailwind and start tailwind
5. Run Django, has browser reload
6. Once the application is finished, the Tailwind build must be executed

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate

    pip install -r requirements.dev.txt

    python manage.py migrate
    python manage.py createsuperuser

    npm --prefix theme/static_src/ install
    python manage.py tailwind start

    python manage.py runserver

    python manage.py tailwind build

    ```

    Test it out at [http://localhost:8000](http://localhost:8000).

### Production

Uses gunicorn + Redis.

1. Rename an edit *.env.sample* to *.env*. Update the environment variables.
2. Build the images and run the containers:

    ```sh
    docker-compose up -d --build
    docker-compose exec sup-dj python manage.py collectstatic --settings=config.prod
    docker-compose exec sup-dj python manage.py makemigrations --settings=config.prod
    docker-compose exec sup-dj python manage.py migrate --settings=config.prod
    docker-compose exec sup-dj python manage.py createsuperuser --settings=config.prod


    docker-compose exec sup-dj python manage.py dumpdata > datos.json --indent=2
    scp -P 38 gonzalo@75.119.135.38:/home/gonzalo/Django/sup/datos.json .
    python manage.py loaddata datos.json

    scp -r -P 38 gonzalo@75.119.135.38:/home/gonzalo/Django/sup/media/* ./media/
    scp -r -P 38 ./media/* gonzalo@75.119.135.38:/home/gonzalo/Django/sup/media/

    rsync -avz --ignore-existing -e "ssh -p 38" gonzalo@75.119.135.38:/home/gonzalo/Django/sup/media/ ./media/


    ```

    Test it out at [http://localhost:8003](http://localhost:8003).
