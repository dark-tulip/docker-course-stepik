# docker-course-stepik
Курс управления вычислениями от Bioinformatics Institute

#### 1. Примонтировать текущую директорию в контейнер parseq/stepik-host-dir
```
echo 'CMkglgw38aTRhlQb+DrzKhrT5VHhG5ucraYD9pv6eHOXirXA8uLqzPOhmrObJV5FeAzu9/LIUqsHfUjAM7gLoANiNAuEyD6/FbNaJWvGjzjpVBt6BSux34ydlEEwsd6Xnlz5Gce+zoXZjcvmvl92ExwA7O4MykGuJb7GeixijW9fI8ev2BvpOP5MaXdX8nFv8y+XjNaI3SHPy60tZEZO0omJkYjnEkZrxOyYCekMsOha/COZ5FgcyBDQa3a4oCf/MwdxlT8RBXiJd1SnROlS63aD93W/YpB8pj8MwTVV0TSnVUueZeMaslSf7cWTMAUDtsQqiYcd3HGygyC2nMFjPg==' > message
docker run -it --rm -v $(pwd):/home/stepik parseq/stepik-host-dir
```
#### 2. Монтирование отдельного файла
```
docker run --rm -v $(pwd)/message:/dev/null parseq/stepik-mount-files
cat message
```
#### 3. Data volume containers
```
docker create -v /srv --name store2 ubuntu:14.04 bin/true
docker run -it --rm --volumes-from store2 ubuntu:14.04 
```
#### 4. Cписок осиротевших томов 
``` 
docker volume ls -qf dangling=true
```
#### 5.Docker никогда не удаляет data volumes, даже если контейнеры, которые их создали, удалены. Для удаления таких томов:
```
docker volume rm $(docker volume ls -qf dangling=true)
```
#### 6. Пробросить порты контейнера к внешнему порту хоста, ключ -р
```
docker run -d --name port-export -p <port_on_host_machine>:<port_inside_container> image
docker run -d --name ports-image -p 4200:80 parseq/stepik-ports-docker 
curl localhost:4200
```
Запустить в режиме демона
```
docker run -d parseq/stepik-exec-docker
docker exec -it 8633756b1eb2

psql -U postgres -c 'SELECT * FROM answers'
```

#### 7. Delete all docker containers 
```
docker rm -f $(docker ps -a -q)
```
#### 8. Взаимодействие контейнеров
* В Docker предустановлены три сети: `none, bridge, host`
* В сети Bridge - контейнеры обращаются по IP адресам (не по именам)
* По умолчанию все контейнеры в одной сети и попадают в сеть `bridge`


Для обращения к контейнеру по имени создаем персональную сеть
```
docker network create custom
docker inspect custom | more
docker run -it --rm --name one --network=custom ubuntu:14.04
docker run -it --rm --name two --network=custom ubuntu:14.04
```
из второго контейнера можем пинговать первый `ping one`

Simple-DNS task

```
docker network create simple-dns
docker run -d --name stepik-linking-docker --network=simple-dns parseq/stepik-linking-docker 
docker run -it --network=simple-dns parseq/stepik-linking-docker-client
```
#### 9. Создание образа из контейнера
```
docker commit img-from-container myimage
docker images
```
 -с / --change применяет инструкцию к создаваемому образу. В данном случе мы берем контейнер create-image-from-me, командой commit создаем из него образ newimage, опцией --change определяя команду (аналогичную таковой Dockerfile)
 ```
 docker commit --change='CMD ["python3"]' create-image-from-me myimage
 ```
 
 Dockerfile - описывает процесс создания образа
 `FROM` - из какого базового образа создем новый образ
 * C помощью образов
 * С помощью Dockerfile
 
 #### 10. First arg on cmd 
 ```
 При использовании режима exec для ENTRYPOINT аргументы CMD добавляются в конце.
 
 # Dockerfile
FROM ubuntu:14.04
ENTRYPOINT echo Hello $0!
CMD ["World"]
 ```
 
 #### 11. Dockerfile
```
# Базовый образ – ubuntu:16.04
FROM ubuntu:16.04

# Владельцем файла на хосте назначается пользователь с uid=1000, если при сборке не указываются дополнительные аргументы, или пользователь с uid, который был задан аргументом UID при сборке
ARG UID=1000

# Установлен текстовый редактор nano
RUN apt update && apt install nano && useradd --uid $UID stepik 

# Переменная окружения $EDITOR устанавливает nano в качестве редактора по умолчанию
ENV EDITOR=nano

# Именно этот пользователь (uid=1000/uid=UID) должен быть основным в контейнере.
USER stepik

# В качестве рабочей директории установлен каталог /home/stepik
WORKDIR /home/stepik

# При запуске контейнера открывается nano, файл автоматически сохраняется в файловую систему хоста, даже если при запуске опции монтирования не указаны (при отсутствии опции монтирования путь, по кторому сохраняется файл, не играет роли, важно, чтобы файл в конечном счете оказался на хосте)
VOLUME /home/stepik

ENTRYPOINT ["bin/bash", "-c", "nano"]
```

Удалить все образы не помеченные тегами
```
docker rmi $(docker images -f "dangling=true" -q)
```

#### Python virtualenv
```Python
virtualenv -p python3 virtualenv
cd virtualenv/bin
source activate
pip3 install wrapt==1.10.1
pip3 install 'requests<=1.9'
pip3 install 'snakemake<=3.13.3'
```
    
