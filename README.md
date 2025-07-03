# WSC Sports - DevOps Exam Solution

This solution deploys two Kubernetes services using Helm:

- **Service A**: Python Flask web service exposing `/service-b-info`
- **Service B**: A resource-consuming dummy service for observable CPU and memory usage

Service A returns the following from Service B:
```json
{
  "nodeName": "minikube-m01",
  "cpu": "300",
  "memory": "50Mi"
}
