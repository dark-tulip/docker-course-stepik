# docker-course-stepik
Курс управления вычислениями от Bioinformatics Institute

#### Примонтировать текущую директорию в контейнер parseq/stepik-host-dir
```
echo 'CMkglgw38aTRhlQb+DrzKhrT5VHhG5ucraYD9pv6eHOXirXA8uLqzPOhmrObJV5FeAzu9/LIUqsHfUjAM7gLoANiNAuEyD6/FbNaJWvGjzjpVBt6BSux34ydlEEwsd6Xnlz5Gce+zoXZjcvmvl92ExwA7O4MykGuJb7GeixijW9fI8ev2BvpOP5MaXdX8nFv8y+XjNaI3SHPy60tZEZO0omJkYjnEkZrxOyYCekMsOha/COZ5FgcyBDQa3a4oCf/MwdxlT8RBXiJd1SnROlS63aD93W/YpB8pj8MwTVV0TSnVUueZeMaslSf7cWTMAUDtsQqiYcd3HGygyC2nMFjPg==' > message
docker run -it --rm -v $(pwd):/home/stepik parseq/stepik-host-dir
```
#### Монтирование отдельного файла
```
docker run --rm -v $(pwd)/message:/dev/null parseq/stepik-mount-files
cat message
```
#### Data volume containers
```
docker create -v /srv --name store2 ubuntu:14.04 bin/true
docker run -it --rm --volumes-from store2 ubuntu:14.04 
```
#### Cписок осиротевших томов 
``` 
docker volume ls -qf dangling=true
```
#### Docker никогда не удаляет data volumes, даже если контейнеры, которые их создали, удалены. Для удаления таких томов:
```
docker volume rm $(docker volume ls -qf dangling=true)
```



