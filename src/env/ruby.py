from env.base import MULTI_FILE_APP_PROMPT_STRUCTURE, Env

_WORKDIR = "/app"
_GEMFILE_NAME = "Gemfile"

_RUBY_DOCKERFILE = f"""
# setup base
FROM ruby:3.4.1-alpine
{{additional_commands}}

# install deps and copy generated code
RUN mkdir -p {_WORKDIR}
WORKDIR {_WORKDIR}
RUN apk --update add build-base nodejs tzdata postgresql-dev postgresql-client libxslt-dev libxml2-dev git
RUN gem install rails
ENV APP_SECRET=supers3cret
RUN rails new . --api
COPY / {_WORKDIR}/
RUN sed -i 's/config.assets/# config.assets/' config/environments/development.rb
RUN bundler install
RUN bin/rails db:create || echo "db:create failed"
RUN bin/rails db:migrate || echo "db:migrate failed"
RUN echo "bin/rails server --binding 0.0.0.0 --port 5000" > entrypoint.sh
ENTRYPOINT {{entrypoint_cmd}}
"""

_GEMFILE = """
source "https://rubygems.org"

# Bundle edge Rails instead: gem "rails", github: "rails/rails", branch: "main"
gem "rails", "~> 8.0.1"
# Use sqlite3 as the database for Active Record
gem "sqlite3", ">= 2.1"
# Use the Puma web server [https://github.com/puma/puma]
gem "puma", ">= 5.0"
# Build JSON APIs with ease [https://github.com/rails/jbuilder]
# gem "jbuilder"

# Use Active Model has_secure_password [https://guides.rubyonrails.org/active_model_basics.html#securepassword]
gem "bcrypt", "~> 3.1.7"

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem "tzinfo-data", platforms: %i[ windows jruby ]

# Use the database-backed adapters for Rails.cache, Active Job, and Action Cable
gem "solid_cache"
gem "solid_queue"
gem "solid_cable"

# Reduces boot times through caching; required in config/boot.rb
gem "bootsnap", require: false

# Deploy this application anywhere as a Docker container [https://kamal-deploy.org]
gem "kamal", require: false

# Add HTTP asset caching/compression and X-Sendfile acceleration to Puma [https://github.com/basecamp/thruster/]
gem "thruster", require: false

gem "image_processing", "~> 1.2"

# Use Rack CORS for handling Cross-Origin Resource Sharing (CORS), making cross-origin Ajax possible
gem "rack-cors"

gem 'activestorage', '~> 8.0.1'

group :development, :test do
  # See https://guides.rubyonrails.org/debugging_rails_applications.html#debugging-with-the-debug-gem
  gem "debug", platforms: %i[ mri windows ], require: "debug/prelude"

  # Static analysis for security vulnerabilities [https://brakemanscanner.org/]
  gem "brakeman", require: false

  # Omakase Ruby styling [https://github.com/rails/rubocop-rails-omakase/]
  gem "rubocop-rails-omakase", require: false
end
"""

_RAILS_ENV_INSTRUCTIONS = f"""
You need to create the Ruby on Rails project from scratch, after the command `rails new . --api` was run.

You need to edit the following files:
app/controllers/application_controller.rb
app/models/application_record.rb
config/application.rb
config/environments/development.rb
config/routes.rb

{MULTI_FILE_APP_PROMPT_STRUCTURE}

Use only SQLite as a database. Do not use MySQL, Redis, or any other storage.
Configure SQLite to use database file `db.sqlite3` in config/database.yml
Do NOT provide Gemfile or Gemfile.lock file. Make sure to include the right frameworks in config/application.rb - e.g. require "active_storage/engine"
Do NOT use sprockets or other asset pipeline. Do NOT use config.assets in config/environments/development.rb.
The command `bin/rails server --binding 0.0.0.0 --port 5000` will start the app.
"""

RubyOnRailsEnv = Env(
    language="Ruby",
    extension="rb",
    framework="Rails",
    code_filename=None,
    env_instructions=_RAILS_ENV_INSTRUCTIONS,
    dockerfile=_RUBY_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_GEMFILE_NAME: _GEMFILE},
    allowed_packages=_GEMFILE,
    is_multi_file=True,
    port=5000,
    entrypoint_cmd="/bin/sh entrypoint.sh",
)
