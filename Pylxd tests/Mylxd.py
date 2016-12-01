#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pylxd import Client
import pylxd
import StringIO
from pylxd import image
import hashlib


class Cluster():
    def __init__(self):
        self._servers = []

    def add(self, server):
        names = [s.name for s in self._servers]
        if server.name in names:
            raise Exception(
                'The server already exists in cluster')
        self._servers.append(server)

    def search(self, container_name):
        state = False
        for server in self._servers:
            for cont in server.containers:
                if cont.name == container_name:
                    state = True
                    return server.name
        if not state:
            print(
                'Error the container do not exists')


class Server():
    def __init__(self, name, host, port, crt, key, password=None):
        self.containers = []
        self.name = name
        self.key = key
        self.ip = host
        self.port = port
        self.crt = crt
        self.endpoint = "https://" + self.ip + ":" + str(self.port)
        self.client = Client(
            endpoint=self.endpoint,
            cert=(self.crt, self.key),
            verify=False)
        if not (self.client.trusted):
            try:
                self.client.authenticate(password)
            except pylxd.exceptions.LXDAPIException:
                print("Introduces the trust password to Client.autheticate")

    def scan(self):
        self.containers = self.client.containers.all()

    @property
    def containers(self):
        return self.client.containers


if __name__ == '__main__':
    cluster = Cluster()
    text_crt = open('/home/joseaa/.config/lxc/client.crt', 'r')
    text_key = open('/home/joseaa/.config/lxc/client.key', 'r')

    file_crt = StringIO.StringIO()
    file_key = StringIO.StringIO()
    file_crt.write(text_crt)
    file_key.write(text_key)

    local = Server(
        'local', '127.0.0.1', '8443',
        '/home/joseaa/.config/lxc/client.crt',
        '/home/joseaa/.config/lxc/client.key')

    cluster.add(local)
    local.scan()
    ##################################################
    # Pruebas networks
    ##################################################
    network = local.client.networks.all()
    for net in network:
        print ("name:" + net.name)
        print ("tipo:" + net.type)

    red = local.client.networks.get("veth6MX54V")
    print red.name

    ##################################################
    # Pruebas profile
    ##################################################
    profile = local.client.profiles.all()
    print ("profiles")
    for pro in profile:
        print ("name:" + pro.name)
    docker = local.client.profiles.get("docker")
    print docker.config
    print docker.devices
    print docker.description
    ##################################################
    # Pruebas images
    ##################################################
    fingerprint = hashlib.sha256(b'').hexdigest()
    a_images = image.Image.all(local.client)
    for img in a_images:
        print img.fingerprint
        # print img.filename
    contain = local.client.containers.get("odoo")
    profil = contain.profiles[0]
    print profil
    profil = local.client.profiles.get(profil)
    print profil.name
    print profil.config
    print profil.devices
    print profil.description
    print contain.config
    print(contain.profiles)
    print(contain.config)
    print(contain.expanded_config)
    print(type(contain.config))
    print (contain.config[u'volatile.base_image'])
    cluster.search('odoo')
    for cont in local.containers:
        print cont.name
    password = "nueva"
    rober = Server(
        'rober', '192.168.2.132', '8443',
        '/home/joseaa/Escritorio/pruebas_pylxd/client.crt',
        '/home/joseaa/Escritorio/pruebas_pylxd/client.key',
        password)
    print(15 * "*")
    print (rober.client.trusted)
    print(15 * "*")
    cluster.add(rober)
    rober.scan()
    for cont in rober.containers:
        print cont.name
    print (30 * "*")

