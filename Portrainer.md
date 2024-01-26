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

Секреты монтируются в контейнер как монтирование файлов или папок

Данный секрет нельзя прочитать или изменить, его можно только удалить


![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/b052f114-68d4-4345-9fdf-4378d6c26789)


Эти секреты доступны во всех нодах кластера, тут пароль читается из файла

```
version: "3.5"

services:
  mysql:
    image: mysql
    environment: 
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/mysql_root_password
      MYSQL_DATABASE: test
    secrets:
      - mysql_root_password

  pma:
    image: phpmyadmin
    ports:
      - 8080:80
    environment:
      PMA_HOST: mysql

secrets:
  mysql_root_password:
    external: true
```

это скроет значение из публичного доступа или конфиг файла


![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/8f50ab03-f4ac-411f-9c33-26aabcf34144)

Через портрейнер можно зайти в терминал и увидеть расшифрованный секрет

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/193ccbe8-6a88-4fd8-a66e-c251d9b44bb4)


## Configs

- виртуальные файлы которые монтируются в контейнеры
- конфиги монтируются внутри кластера докер и доступны на всех нодах

1) создаем новый стек
```yaml
version: "3"

services:
  nginx:
    image: nginx
    ports:
      - 81:80
```

2) create new config, после создания нельзя редактировать, можно только удалить

```config
server {
  listen 80;
  server_name _;
  location = / {
    add_header Content-Type text/plain;
    return 200 'Portainer config';
  }
}
```

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/41177aa6-8198-4ab7-88f9-6a7d13ed52b7)

3) Монтирование конфига внутри контейнера, modify stack

```yaml
version: "3.5"

services:
  nginx:
    image: nginx
    ports:
      - 81:80
    configs:  # примонтировать конфиг по данному пути
      - source: nginxConfig
        target: /etc/nginx/conf.d/default.conf

configs:
  nginxConfig:
    external: true
```

4) config accepted by nginx

![image](https://github.com/dark-tulip/docker-course-stepik/assets/89765480/f81a0b10-fcb8-4693-aa7f-0d52952b4fbc)
