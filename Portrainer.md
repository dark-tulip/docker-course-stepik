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


### Настройки стека через UI

можно изменить стек на котором был поднят контейнер 

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/1613f0e9-1965-4fb8-be84-f2bc0ece3795)


можно обновить параметры сервиса, например для БД перемещать каждый раз volumes не ризон, лучше задать constraints

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/572a8c8a-a8af-4829-9e59-ceebaba6e793)


![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/e3ba361e-881c-4d2f-b39b-c5380c3a7824)

или можно обновить стэк файл
```yaml
version: "3"

services:
    wordpress:
        image: wordpress
        ports:
            -   82:80
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
        deploy:
            replicas: 2

    phpmyadmin:
        image: phpmyadmin
        ports:
            - 8081:80
        environment:
            PMA_HOST: mysql
```

## Макс кол-во реплик на ноду
если нод меньше, остальные реплики будут в состоянии ожидания pending
чтобы изменнеия вступили в силу, стек нужно пересоздать
```yaml
    mysql:
        image: mysql:5.7
        environment:
            MYSQL_USER: wp
            MYSQL_DATABASE: wp
            MYSQL_PASSWORD: wp_pass
            MYSQL_ROOT_PASSWORD: root
        deploy:
            replicas: 2
            max_replicas_per_node: 1
```

## Режимы реплицирования сервисов
есть два режима реплицирования сервисов
- **replicated**; Number of replicas and Replication rules, запуск на ноде соответсвующей правилам (defaults)
- **global**; размещение на всех нодах кластера, for example portainer agent serice is located on each node

```yaml
    mysql:
        image: mysql:5.7
        environment:
            MYSQL_USER: wp
            MYSQL_DATABASE: wp
            MYSQL_PASSWORD: wp_pass
            MYSQL_ROOT_PASSWORD: root
        deploy:
            mode: global  # режим реплицирования глобавльный
            constraints: 
              - "node.labels.nginx!=1"  # разместится только на первой ноде
```

## Secrets

