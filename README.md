# Example Grafana use
  
Simple example of api monitoring via Grafana

Based on the [webinar by Sergey Bukharov](https://www.youtube.com/watch?v=Q_fKb0nrfCg)
  
  
## Used technologies
  
* [Python 3.10](https://docs.python.org/3.10/),
* [FastAPI](https://fastapi.tiangolo.com/), 
* [aioprometheus](https://aioprometheus.readthedocs.io/en/stable/),
* [Prometheus](https://prometheus.io/), 
* [Grafana](https://grafana.com/), 
* [docker](https://docs.docker.com/)
  
  
## Interfaces

- API documentation - http://127.0.0.1:8000/docs
- API metrics - http://127.0.0.1:8000/metrics
- Prometheus is available at - http://127.0.0.1:9090  
- Grafana - http://127.0.0.1:3000 (admin:admin)   
  
  
## Launching in Docker

Create and start container:
```bash
$ docker-compose --env-file ./configs/.env up 
```
Stop lifted containers:
```bash
$ docker-compose --env-file ./configs/.env stop
```
Start stopped containers:
```bash
$ docker-compose --env-file ./configs/.env start
```
Stop and delete containers and network:
```bash
$ docker-compose --env-file ./configs/.env down
```