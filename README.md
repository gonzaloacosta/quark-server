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

### Build & Run & Status

```bash
# Build
make dev-up

# Status
make dev-status

# Destroy
make dev-down
```

## Quark :] blog post!

- [x] *Home* `/`
- [x] *New Post* `/create`
- [x] *View Post* `/<post_id>`
- [x] *Edit Post* `/<post_id>/edit`
- [x] *Delete Post* `/<post_id>/delete`
- [ ] *External DB Mongo*, for users.
- [ ] *External Redis* for sessions
- [ ] *Login*, add login web page
- [X] *Slim Image*, change the images and add nginx, wsgi and flask.
- [X] *Make files*
- [ ] *Unit and Integration Test*

## Another funtionalities

- [x] *Healthz* `/healthz`, Usefull for readiness and liveness probe.
- [x] *Sleep* `/sleep/<num>`, Introduce and sleep `<num>` time in secods in the request.
- [x] *Inject error* `/error`, Inject an error 503.
- [x] *Check TCP* `/tcp/`, Complete field with `<host>` and `<port>` to test.
- [ ] *Forward* `/forward?type=pass&host=<hostname|address>&port=<port>`. Refactor the function. Usefull to forward a request, TODO build the web page with form.
  - `type=pass`: try to reach another services defined in parameters `host` and `port`
  - `type=end`: finalize the chain services.
- [ ] *URL* `/url?host=<hostname|address>&port=<port>`, Similar to another scenario but in this case use the [Zipkins headers](https://github.com/openzipkin/b3-propagation) to propagation headers.
- [x] *Logger* `/logger/<num>`, Print a secuence of number until `<num>` in stdout.
- [ ] *Logging* `/logging?iteration=<number>&file=</path/to/file.log>`, TODO the idea is write in a file some of logs.
- [ ] *Prometheus Metrics* `/metrics`, Todo complete defining counter, histograms, summaries, gauges to defined SLI, SLO and SLA 
- [ ] *CPU/Mem Generator**`/load/<cpu|mem>`, simulate cpu and memory generator.

## Contact

- **Gonzalo Acosta** <br>
  e-mail: <gonzaloacostapeiro@gmail.com> <br>
  Twitter: @_gonzalo_acosta

