Ferris K8s
=====================
[![Downloads](https://pepy.tech/badge/ferris-k8s)](https://pepy.tech/project/ferris-k8s)

The following library simplifies the process of 
* accessing Kubernetes API.
* managing deployments

# Pre-Requisites
The core engine is KubernetesEngine and is an abstract class. You need to implement the login method in order to enable the login to your specific Kubernetes environment.


# Dependencies
* You need to have kubectl installed


# To Build
* git clone this repo
* cd to root directory of repo
* python setup.py sdist
* cd to dist directory
* pip install the tar file
* import ferris_k8s_cli.ferris_k8s_cli.KubernetesEnige


# Sample Code

```python

from ferris_k8s.cli import Cli
import json

cli = Cli('namespace','username','password')
cli.login()
pod_list = json.loads(cli.get_pods())

for pod in pod_list["items"]:
    print(pod['metadata']['name'])
    print("specs")
    print(pod['spec'])
    print("status")
    print(pod['status'])
    print("*********************************")    
#cli.get_deployments()
#cli.create_deployment('/home/jovyan/work/ferri-data-cli-samples/metabase.yaml')
#cli.delete_deployment('metabase')
#cli.get_logs('metabase-55dd49bdf8-whz78')
## Streams Logs
#cli.follow_logs('bcm-baszh-8-executionreport-5bbc99dbc-s4xm9')

```

