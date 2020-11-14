## Redis

Deploy with Kubectl
```bash
	kubectl create -f .\redis\redis.yaml
```

## Postgres
Build image for postgres
```bash
	cd apps/postgres
	docker build . -t postgres:safe
```
Deploy with Kubectl
```bash
	kubectl create -f .\postgres\postgres.yaml
```

## App
Build image for app
```bash
	cd apps/brounder
	docker build . -t brounder
```
Deploy with Kubectl
```bash
	kubectl create -f .\brounder\brounder.yaml
```


### Troubleshooting:

In case of needed migrations
```bash
	 kubectl exec -it <POD_ID> python manage.py migrate
```

