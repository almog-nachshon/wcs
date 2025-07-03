NAMESPACE=wcs

install:
	helm upgrade --install wsc-devops-exam ./helmchart -n $(NAMESPACE) --create-namespace

uninstall:
	helm uninstall wsc-devops-exam -n $(NAMESPACE)
	kubectl delete ns $(NAMESPACE) --ignore-not-found

port-forward:
	kubectl port-forward svc/service-a 8080:8080 -n $(NAMESPACE)

logs:
	kubectl logs deploy/service-a -n $(NAMESPACE)

test:
	curl http://localhost:8080/service-b-info
