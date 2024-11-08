import yaml

diccionario_conf = {"Configuración preagarre": [0,0,0,0,0,0]}

with open("fichero_pruebas_yaml", "+a") as f:
    yaml.dump(diccionario_conf)
with open("fichero_pruebas_yaml", "+r") as f:
    conf = yaml.load(f, yaml.Loader)