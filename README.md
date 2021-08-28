# Quark :]

Reference-style: 
![alt text][quark-cowsay]

[quark-cowsay]: https://github.com/gonzaloacosta/quark-server/raw/master/images/quark-cowsay.png "Quark Cowsay"

Quark is a simple server writing in python flask to use in linux containers world :]

### Build

```bash
docker build --no-cache -t quark-server .
```

### Run

```bash
docker run --rm -d --name quark-server -p 8080:8080 gonzaloacosta/quark-server 
```

## Context Path

- **Home** `/`

Welcome home paga have all the amazing *remember notes!*

- **Hello World** `/hello`

```bash
curl http://<address>:<port>/hello
```
- **Version** `/version`

Version number of this awesome quark server ;)

```bash
curl http://<simple-webserver>/version
```

- **Date** `/date`

Return date time

```
curl http://<address>:<port>/date
```
- **Health Check** `/healthz`

Health check usefull to readiness and liveness probes. Return `ok` is everythings it's ok and `no` there is a problem.

```bash
curl http://<address>:<port>/healthz
```

- **Sleep** `/sleep/<num>`

Return `num` seconds to response.

```bash
curl http://<simple-webserver>/sleep/5
```

- **Inject error** `/error`

Return an 503 error

```bash
curl http://<simple-webserver>/error
```

- **Test TCP** `/tcp/?host=<hostname|address>&port=<port>`

Usefull to reach a tcp layer 4 services.

```bash
curl http://localhost:8080/testconn?type=pass&host=google.com&port=80
```

- **Forward** `/forward?type=pass&host=<hostname|address>&port=<port>`

Usefull tool to reach a http services in chain.

* `type=pass`: try to reach another services defined in parameters `host` and `port`
* `type=end`: finalize the chain services.

```
curl http://localhost:8080/forward?type=<passs|end>&host=<another_services>&port=8080
```

- **URL** `/url?host=<hostname|address>&port=<port>`

Similar to another scenario but in this case use the [Zipkins headers](https://github.com/openzipkin/b3-propagation) to propagation headers.

```bash
curl http://localhost:8080/url?host=<another_services>&port=8080
```

- **Logger** `/logger/<num>

Logger in stander output the amount of second that you define in `num`.


```bash
curl http://localhost:8080/logger/<num>
```

- **Logging** `/logging?iteration=<number>&file=</path/to/file.log>`

TODO: Logging in a file some of text or iteration. The job will be create the path and write the secuence in a indicated file

```bash
curl http://localhost:8080/logging?iteration=<number>&file=</path/to/file.log>
```

- **Metrics** `/metrics`

TODO: Enable prometheus metrics and defined counter, gauges and histograms to monitor the application.

- **Load Average** `/load/<cpu|mem>`

TODO: Start a Job to consume a lot of cpu or memory to reach limits and request

```bash
curl http://localhost:8080/load/<cpu|mem>
```

## Contact

- **Gonzalo Acosta** <gonzaloacostapeiro@gmail.com>