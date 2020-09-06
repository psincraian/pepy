<p align="center">
  <img width="100px" alt="pepy-logo"
    src="docs/logo.png"
  />
</p>
<p align="center">

<p align="center">

[![Build Status](https://travis-ci.com/psincraian/pepy.svg?branch=master)](https://travis-ci.com/psincraian/pepy)
<p align="center">

</p>
<h2 align="center"><code>PePy</code></h2>



## 📜 About
[pepy.tech](https://pepy.tech) is a site which aims to show statistics about Python packages.

This is the repository for the backend service, if you want to check the frontend check this repo https://github.com/psincraian/pepy-front

## ⚒️ Start contributing
I wanted to make the setup of the environment as easy as possible. To start the environment you need the 
following prerequisites:

### Prerequisites
  * bash (+4.3)
  * docker (+17.05)
  * docker-compose (+1.16.1)
  * docker-py (+2.2.1)
  * ansible (+2.3)
  
### Start environment
You only (_fingers crossed_) need to execute the following to start the environment:

```commandline
make start-containers
```

## Architecture and patterns
Principally I used some DDD concepts (like value objects, entities, and so on) and also CQS whose objective is to
separate commands from queries.

The structure of the code is the following:
  * `pepy/application`: here is where all the commands and the queries are located.
  * `pepy/domain`: domain objects like entities, exceptions, and value objects.
  * `pepy/infrastructure`: infrastructure components like the implementation of the repository
    class like DB or BigQuery, the Flask web application, the container, and so on.
    * `pepy/infrastructure/cli`: the command line programs.
    * `pepy/infrastructure/container`: config files and the dependency injection manager.
    * `pepy/infrastructure/api`: the api endpoints controller.
    
## FAQ
**Where the downloads come from?**

The data is retrieved from the official BigQuery repository: https://packaging.python.org/guides/analyzing-pypi-package-downloads/

**When the data is updated?**

There is a cron that runs every day at 5 pm UTC that retrieves all the new downloads from the previous day.

## 🚩 License
The code is available under the [MIT license](LICENSE.md).
