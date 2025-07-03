from flask import Flask, jsonify
from kubernetes import client, config

app = Flask(__name__)
config.load_incluster_config()

@app.route("/service-b-info")
def get_service_b_info():
    v1 = client.CoreV1Api()
    metrics = client.CustomObjectsApi()

    namespace = "wcs"

    pods = v1.list_namespaced_pod(namespace=namespace, label_selector="app=service-b")
    if not pods.items:
        return jsonify({"error": "No service-b pod found"}), 404

    pod = pods.items[0]
    pod_name = pod.metadata.name
    node_name = pod.spec.node_name

    try:
        usage = metrics.get_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods",
            name=pod_name
        )
        container_metrics = usage["containers"][0]["usage"]
        cpu_raw = container_metrics["cpu"]
        memory_raw = container_metrics["memory"]

        if cpu_raw.endswith("n"):
            cpu = str(int(cpu_raw.rstrip("n")) // 1000000)
        else:
            cpu = cpu_raw

        if memory_raw.endswith("Ki"):
            memory = str(round(int(memory_raw.rstrip("Ki")) / 1024, 1))
        else:
            memory = memory_raw
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    return jsonify({
        "nodeName": node_name,
        "cpu": cpu,
        "memory": memory
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
