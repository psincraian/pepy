<p align="center">
  <img width="100px" alt="pepy-logo"
    src="pepy/infrastructure/web/static/logo.png"
  />
</p>
<p align="center">
<a href="https://travis-ci.com/psincraian/pepy.svg?branch=master"><img src="https://travis-ci.com/psincraian/pepy.svg?branch=master" alt="Build status" height="18"></a>
</p>
<h2 align="center"><code>pepy</code></h2>

## 📜 About

[pepy.tech](http://pepy.tech) is a site which aim is to show
statistics information about the Python packages.

## ⚒️ Start contributing
I wanted to make the setup of the environment as easy as possible. To
start the environment you will need to have the following
prerequisites:

### Prerequisites

* bash (+4.3)
* docker (+17.05)
* docker-compose (+1.16.1)
* docker-py (+2.2.1)
* ansible (+2.3)

### Start environment

You only (_fingers crossed_) need to execute the following to start
the environment:

```sh
make start-containers
```

## Architecture and patterns

Principally I used some of DDD concepts (like value objects, entities,
and so on) and also CQS which objective is to separate commands from
queries.

The structure of the code is the following:

* `pepy/application`: here is where all the commands and the queries
  are located.
* `pepy/domain`: domain objects like entities, exceptions, and value
  objects.
* `pepy/infrastructure`: infrastructure components like the
  implementation of the repository class like db or BigQuery, the
  Flask web application, the container, and so on.
* `pepy/infrastructure/cli`: the command line programs
* `pepy/infrastructure/container`: config files and the dependency
  injection manager.
* `pepy/infrastructure/web`: the Flask application with all the
  routes.

## 🚩 License

The code is available under the [MIT license](LICENSE.md).
