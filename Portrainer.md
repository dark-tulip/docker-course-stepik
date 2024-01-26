Portrainer consist from
- Portrainer Server
- Portrainer Agent

## Install

```bash
curl -L https://downloads.portainer.io/ee2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml
```

## Run stack
```bash
docker stack deploy -c portainer-agent-stack.yml portainer
```

портрейнер стартует на порту 9000 тут есть список кластеров которые находятся под нашим управлением

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/53228bb3-f88e-4943-9b77-d41c1bf45956)

визуалайзер кластера

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/e775ecef-f0f5-4eaa-8328-90e049c835a9)
