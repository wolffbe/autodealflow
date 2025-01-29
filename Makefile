COMPOSE_FILE = docker-compose.yaml

c:
	docker-compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	docker system prune -f

b:
	docker-compose -f $(COMPOSE_FILE) build --no-cache

r:
	docker-compose -f $(COMPOSE_FILE) up -d

l:
	docker-compose -f $(COMPOSE_FILE) logs -f

cb:
	$(MAKE) c
	$(MAKE) b

cbr:
	$(MAKE) c
	$(MAKE) b
	$(MAKE) r

cbrl:
	$(MAKE) cbr
	$(MAKE) l

brl:
	$(MAKE) b
	$(MAKE) r
	$(MAKE) l