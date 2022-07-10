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


