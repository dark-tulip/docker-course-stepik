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
