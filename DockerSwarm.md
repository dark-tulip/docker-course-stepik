docker play labs

1) создаем три инстанса 


```bash
docker swarm init --advertise-addr 192.168.0.16
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/03024ca0-7751-463b-a314-74020eeea6ac)

### чтобы добавить еще одну ноду в кластер надо внести команду с выведенным токеном

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/78282e8f-71a3-4a05-ae95-db35d95e7856)

### Список нод

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/6fbe69e5-682d-46dd-8005-d347caacdabe)

### Удалить ноду из кластера

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
                "TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUWflM0yNKip3breJK4gMy/fVpiUowCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMjQwMTI1MDUzMDAwWhcNNDQwMTIwMDUz\nMDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABNbb04jMKupd+PuMqdC8OAE3j7IM0Zk5DJpa46bqeBY1Mits9Tno7HYHJqRN\nMvunYiDVRm0bKf/pXf7w7vfgCCujQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRaaD1PVUl/wJ1C1OEiA2RbJFBKPTAKBggqhkjO\nPQQDAgNIADBFAiBayTG3Zu4VTr/pGTM6Uri3L+oWX+i+TA4eInHDVABy+gIhAMHr\np/1I4TZv4IYjL7WJ19hTnDKnqMg1ebaDBy2Jvv+C\n-----END CERTIFICATE-----\n",
                "CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
                "CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE1tvTiMwq6l34+4yp0Lw4ATePsgzRmTkMmlrjpup4FjUyK2z1OejsdgcmpE0y+6diINVGbRsp/+ld/vDu9+AIKw=="
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
