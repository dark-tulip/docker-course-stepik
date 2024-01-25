## docker play labs

1) создаем три инстанса 

```bash
docker swarm init --advertise-addr 192.168.0.16
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/03024ca0-7751-463b-a314-74020eeea6ac)

### Add node to cluster

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/78282e8f-71a3-4a05-ae95-db35d95e7856)

### Список нод

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/6fbe69e5-682d-46dd-8005-d347caacdabe)

### Покинуть рой из кластера

```bash
docker swarm leave
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/3af19cd0-5602-48c1-ada1-e608587485a1)


![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/d513649b-b799-4f04-86e4-a04d01155a9a)


### docker inspect nodeName

```bash
[node3] (local) root@192.168.0.16 ~
$ docker inspect node1
```
```json
[
    {
        "ID": "pkdo85iflgjsd0y8btfyl2g41",
        "Version": {
            "Index": 21
        },
        "CreatedAt": "2024-01-25T05:42:09.855347244Z",
        "UpdatedAt": "2024-01-25T05:45:20.213507149Z",
        "Spec": {
            "Labels": {},
            "Role": "worker",
            "Availability": "active"
        },
        "Description": {
            "Hostname": "node1",
            "Platform": {
                "Architecture": "x86_64",
                "OS": "linux"
            },
            "Resources": {
                "NanoCPUs": 8000000000,
                "MemoryBytes": 33737699328
            },
            "Engine": {
                "EngineVersion": "24.0.7",
                "Plugins": [
                    {
                        "Type": "Log",
                        "Name": "awslogs"
                    },
                    {
                        "Type": "Log",
                        "Name": "fluentd"
                    },
                    {
                        "Type": "Log",
                        "Name": "gcplogs"
                    },
                    {
                        "Type": "Log",
                        "Name": "gelf"
                    },
                    {
                        "Type": "Log",
                        "Name": "journald"
                    },
                    {
                        "Type": "Log",
                        "Name": "json-file"
                    },
                    {
                        "Type": "Log",
                        "Name": "local"
                    },
                    {
                        "Type": "Log",
                        "Name": "logentries"
                    },
                    {
                        "Type": "Log",
                        "Name": "splunk"
                    },
                    {
                        "Type": "Log",
                        "Name": "syslog"
                    },
                    {
                        "Type": "Network",
                        "Name": "bridge"
                    },
                    {
                        "Type": "Network",
                        "Name": "host"
                    },
                    {
                        "Type": "Network",
                        "Name": "ipvlan"
                    },
                    {
                        "Type": "Network",
                        "Name": "macvlan"
                    },
                    {
                        "Type": "Network",
                        "Name": "null"
                    },
                    {
                        "Type": "Network",
                        "Name": "overlay"
                    },
                    {
                        "Type": "Volume",
                        "Name": "local"
                    }
                ]
            },
            "TLSInfo": {
                "TrustRoot": "**",
                "CertIssuerSubject": "**",
                "CertIssuerPublicKey": "**"
            }
        },
        "Status": {
            "State": "down",
            "Message": "heartbeat failure",
            "Addr": "192.168.0.18"
        }
    }
]
```

### Удалить ноду из кластера

```bash
docker node rm hostname
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/ba1263e2-811a-43d3-bddd-6ad29a29ae44)

### Посмотреть токен воркера

```bash
docker swarm join-token worker
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/b8677cca-3391-479c-9e9e-b07e662f9378)


### docker stack deploy

```
docker stack deploy -c ./stack.yml wp
```

```stack.yml
version: "3"

services:
    wordpress:
        image: wordpress
        ports:
            -   80:80
        environment:
            WORDPRESS_DB_HOST: mysql
            WORDPRESS_DB_NAME: wp
            WORDPRESS_DB_USER: wp
            WORDPRESS_DB_PASSWORD: wp_pass

    mysql:
        image: mysql:5.7
        environment:
            MYSQL_USER: wp
            MYSQL_DATABASE: wp
            MYSQL_PASSWORD: wp_pass
            MYSQL_ROOT_PASSWORD: root

    phpmyadmin:
        image: phpmyadmin
        ports:
            - 8080:80
        environment:
            PMA_HOST: mysql
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/7cc5b88a-2f28-4329-b304-591c2f23cca6)


теперь по портам 80 и 8080 можно открыть phpMyadmin and wordpress

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/f64ca931-b918-41a4-acfb-43440a7ca24b)
