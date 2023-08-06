import json
import sys
import jinja2
import os
from os import path
import yaml
import requests
from  urllib.parse import urlencode
from kubernetes.client.rest import ApiException
from kubernetes import client, config
import abc
from abc import ABC, abstractmethod

class Cli(ABC):

    def __init__(self, namespace: str, username: str, password: str):
        self.namespace = namespace
        self.username = username
        self.password = password

    @abstractmethod
    def login(self):
        pass

    def get_deployments(self):
        try:
            config.load_kube_config()
            api_instance = client.AppsV1Api()
            api_response = api_instance.list_namespaced_deployment(namespace=self.namespace,_preload_content=False)
            return api_response.data 
        except Exception as e:
            print('Found exception in reading the logs')
            print(e)

    def get_deployment_names(self):
        try:
            deployment_names = []
            deployments = self.get_deployments()
            deployments =json.loads(deployments)
            for deployment in deployments['items']:
                deployment_names.append(deployment['metadata']['name'])
            print(deployment_names)
            return json.dumps(deployment_names)
        except Exception as e:
            print('Found exception in reading the logs')
            print(e)

    def get_deployment(self,deployment_name):
        try:
            deployment_names = []
            deployments = self.get_deployments()
            deployments =json.loads(deployments)
            for deployment in deployments['items']:
                if deployment_name in deployment['metadata']['name']:
                    return json.dumps(deployment)
        except Exception as e:
            print('Found exception in reading the logs')
            print(e)
 

    def create_deployment(self,deployment_file_path):
        config.load_kube_config()
        with open(path.join(path.dirname(__file__), deployment_file_path)) as f:
            dep = yaml.safe_load(f)
            api_instance = client.AppsV1Api()
            resp = api_instance.create_namespaced_deployment(body=dep, namespace=self.namespace)
            print("Deployment created. status='%s'" % resp.metadata.name)    

    def delete_deployment(self,deployment_name):
        config.load_kube_config()
        api_instance = client.AppsV1Api()
        resp = api_instance.delete_namespaced_deployment(name=deployment_name , namespace=self.namespace)
  

    def get_pods(self):
        try:
            config.load_kube_config()
            api_instance = client.CoreV1Api()
            api_response = api_instance.list_namespaced_pod(namespace=self.namespace,_preload_content=False)
            return api_response.data
        except Exception as e:
            print('Found exception in reading the logs')
            print(e)
        return   
    
    def get_pod(self,pod_name):
        try:
            config.load_kube_config()
            api_instance = client.CoreV1Api()
            api_response = api_instance.read_namespaced_pod(name=pod_name, namespace=self.namespace,_preload_content=False)
            return api_response.data
        except Exception as e:
            print('Found exception in reading the logs')
            print(e)
        return ''
    
    def get_logs(self,pod_name):
        config.load_kube_config()
        try:
            api_instance = client.CoreV1Api()
            api_response = api_instance.read_namespaced_pod_log(name=pod_name, namespace=self.namespace)
            print(api_response)
        except Exception as e:
            print(e)

    def follow_logs(self,pod_name):
        config.load_kube_config()
        try:
            api_instance = client.CoreV1Api()
            for line in api_instance.read_namespaced_pod_log(name=pod_name, namespace=self.namespace,follow =True,_preload_content=False).stream():
                print(line.decode('utf-8').strip())
        except Exception as e:
            print(e)