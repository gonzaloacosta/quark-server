# Quark :]

```
 ________  ___  ___  ________  ________  ___  __       
|\   __  \|\  \|\  \|\   __  \|\   __  \|\  \|\  \     
\ \  \|\  \ \  \\\  \ \  \|\  \ \  \|\  \ \  \/  /|_   
 \ \  \\\  \ \  \\\  \ \   __  \ \   _  _\ \   ___  \  
  \ \  \\\  \ \  \\\  \ \  \ \  \ \  \\  \\ \  \\ \  \ 
   \ \_____  \ \_______\ \__\ \__\ \__\\ _\\ \__\\ \__\
    \|___| \__\|_______|\|__|\|__|\|__|\|__|\|__| \|__|
          \|__|                                        
                
```

Quark is a simple server writing in python using flask, thinking to use in linux containers world

### Build

```bash
docker build --no-cache -t gonzaloacosta/quark-server:0.0.2 .
```

### Run

```bash
docker run --rm -d --name quark-server -p 8080:8080 gonzaloacosta/quark-server:v0.0.2
```

## Quark :] short post!

- [x] **Home** `/`
- [x] **New Post** `/create`
- [x] **View Post** `/<post_id>`
- [x] **Edit Post** `/<post_id>/edit`
- [x] **Delete Post** `/<post_id>/delete`
- [ ] **External DB Mongo**, for users.
- [ ] **External Redis** for sessions
- [ ] **Login**, add login web page

## Another funtionalities

- [x] **Healthz** `/healthz`, Usefull for readiness and liveness probe.
- [x] **Sleep** `/sleep/<num>`, Introduce and sleep `<num>` time in secods in the request.
- [x] **Inject error** `/error`, Inject an error 503.
- [x] **Check TCP** `/tcp/`, Complete field with `<host>` and `<port>` to test.
- [/] **Forward** `/forward?type=pass&host=<hostname|address>&port=<port>`. Usefull to forward a request, TODO build the web page with form.
  - `type=pass`: try to reach another services defined in parameters `host` and `port`
  - `type=end`: finalize the chain services.
- [/] **URL** `/url?host=<hostname|address>&port=<port>`, Similar to another scenario but in this case use the [Zipkins headers](https://github.com/openzipkin/b3-propagation) to propagation headers.
- [x] **Logger** `/logger/<num>`, Print a secuence of number until `<num>` in stdout.
- [ ] **Logging** `/logging?iteration=<number>&file=</path/to/file.log>`, TODO the idea is write in a file some of logs.
- [/] **Prometheus Metrics** `/metrics`, Define counter, histograms, summarys, gauges to defined SLI, SLO and SLA 
- [ ] **CPU/Mem Generator** `/load/<cpu|mem>`, simulate cpu and memory generator.

### Run application without containers

- **UWS**

```bash
uwsgi --http localhost:8080 --wsgi-file server.py --callable app
```

- **Flask**

```bash
export FLASK_APP=server
export FLASK_ENVIRONMENT=development
flask run -p 8080
```

## Contact

- **Gonzalo Acosta** <gonzaloacostapeiro@gmail.com>
