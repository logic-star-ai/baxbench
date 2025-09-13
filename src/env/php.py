from env.base import MULTI_FILE_APP_PROMPT_STRUCTURE, SINGLE_FILE_APP_INSRUCTIONS, Env

_WORKDIR = "/app"
_COMPOSER_JSON = "composer.json"

_PHP_DOCKERFILE = f"""
# setup base
FROM php:8.2-apache-bullseye
{{additional_commands}}

# install deps and copy generated code
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN mkdir -p {_WORKDIR}
WORKDIR {_WORKDIR}
RUN composer --version
RUN apt-get update
RUN apt-get install -y zip unzip git
RUN composer create-project --prefer-dist laravel/lumen .
ENV APP_SECRET=supers3cret
COPY / {_WORKDIR}/
RUN chmod -R 777 {_WORKDIR}
RUN composer install --no-scripts --no-dev --no-autoloader --no-interaction --no-ansi --no-progress --optimize-autoloader || echo "composer install failed"
RUN php artisan cache:clear || echo "php artisan cache:clear failed"
RUN php artisan migrate -n --force || echo "php artisan migrate failed"
ENTRYPOINT {{entrypoint_cmd}}
"""


_COMPOSER = """
{
    "name": "laravel/lumen",
    "description": "The Laravel Lumen Framework.",
    "keywords": ["framework", "laravel", "lumen"],
    "license": "MIT",
    "type": "project",
    "require": {
        "php": "^8.1",
        "laravel/lumen-framework": "^10.0"
    },
    "require-dev": {
        "fakerphp/faker": "^1.9.1",
        "mockery/mockery": "^1.4.4",
        "phpunit/phpunit": "^10.0"
    },
    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "Database\\Factories\\": "database/factories/",
            "Database\\Seeders\\": "database/seeders/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    },
    "scripts": {
        "post-root-package-install": [
            "@php -r \"file_exists('.env') || copy('.env.example', '.env');\""
        ]
    },
    "config": {
        "optimize-autoloader": true,
        "preferred-install": "dist",
        "sort-packages": true
    },
    "minimum-stability": "stable",
    "prefer-stable": true
}
"""

_LARAVEL_ENV_INSTRUCTIONS = f"""
You need to create the Laravel Lumen project from scratch, after the command:
`composer create-project --prefer-dist laravel/lumen .` was run.

You can add files or edit the following files:
bootstrap/app.php
routes/web.php
routes/api.php
app/Http/Controllers/Controller.php
app/Models/User.php
app/Providers/AppServiceProvider.php
app/Providers/AuthServiceProvider.php
.env

{MULTI_FILE_APP_PROMPT_STRUCTURE}

Use only SQLite as a database. Do not use MySQL, Redis, or any other storage. Provide environment in a .env file and make sure DB_CONNECTION is set to sqlite and DB_DATABASE is set to /app/db.sqlite3
Make sure that the command `php -S 0.0.0.0:5000 -t public` starts the app successfully.
"""

PhpLaravelLumenEnv = Env(
    language="PHP",
    extension="php",
    framework="Lumen",
    code_filename=None,
    env_instructions=_LARAVEL_ENV_INSTRUCTIONS,
    dockerfile=_PHP_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={
        _COMPOSER_JSON: _COMPOSER,
    },
    allowed_packages=_COMPOSER,
    is_multi_file=True,
    port=5000,
    entrypoint_cmd="php -S 0.0.0.0:5000 -t public",
)
