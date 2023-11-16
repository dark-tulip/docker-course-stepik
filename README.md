# docker-course-stepik
Курс управления вычислениями от Bioinformatics Institute

#### 1. Примонтировать текущую директорию в контейнер parseq/stepik-host-dir
```bash
echo 'CMkglgw38aTRhlQb+DrzKhrT5VHhG5ucraYD9pv6eHOXirXA8uLqzPOhmrObJV5FeAzu9/LIUqsHfUjAM7gLoANiNAuEyD6/FbNaJWvGjzjpVBt6BSux34ydlEEwsd6Xnlz5Gce+zoXZjcvmvl92ExwA7O4MykGuJb7GeixijW9fI8ev2BvpOP5MaXdX8nFv8y+XjNaI3SHPy60tZEZO0omJkYjnEkZrxOyYCekMsOha/COZ5FgcyBDQa3a4oCf/MwdxlT8RBXiJd1SnROlS63aD93W/YpB8pj8MwTVV0TSnVUueZeMaslSf7cWTMAUDtsQqiYcd3HGygyC2nMFjPg==' > message
docker run -it --rm -v $(pwd):/home/stepik parseq/stepik-host-dir
```
#### 2. Монтирование отдельного файла
```bash
docker run --rm -v $(pwd)/message:/dev/null parseq/stepik-mount-files
cat message
```
#### 3. Data volume containers
```bash
docker create -v /srv --name store2 ubuntu:14.04 bin/true
docker run -it --rm --volumes-from store2 ubuntu:14.04 
```
#### 4. Cписок осиротевших томов 
```bash
docker volume ls -qf dangling=true
```
#### 5.Docker никогда не удаляет data volumes, даже если контейнеры, которые их создали, удалены. Для удаления таких томов:
```bash
docker volume rm $(docker volume ls -qf dangling=true)
```
#### 6. Пробросить порты контейнера к внешнему порту хоста, ключ -р
```bash
docker run -d --name port-export -p <port_on_host_machine>:<port_inside_container> image
docker run -d --name ports-image -p 4200:80 parseq/stepik-ports-docker 
curl localhost:4200
```
Запустить в режиме демона
```bash
docker run -d parseq/stepik-exec-docker
docker exec -it 8633756b1eb2

psql -U postgres -c 'SELECT * FROM answers'
```

#### 7. Delete all docker containers 
```bash
docker rm -f $(docker ps -a -q)
```
#### 8. Взаимодействие контейнеров
* В Docker предустановлены три сети: `none, bridge, host`
* В сети Bridge - контейнеры обращаются по IP адресам (не по именам)
* По умолчанию все контейнеры в одной сети и попадают в сеть `bridge`


Для обращения к контейнеру по имени создаем персональную сеть
```bash
docker network create custom
docker inspect custom | more
docker run -it --rm --name one --network=custom ubuntu:14.04
docker run -it --rm --name two --network=custom ubuntu:14.04
```
из второго контейнера можем пинговать первый `ping one`

Simple-DNS task

```bash
docker network create simple-dns
docker run -d --name stepik-linking-docker --network=simple-dns parseq/stepik-linking-docker 
docker run -it --network=simple-dns parseq/stepik-linking-docker-client
```
#### 9. Создание образа из контейнера
```bash
docker commit img-from-container myimage
docker images
```

#### 10 Gitlab-runner in docker
```
Options:
--rm - Automatically remove the container when it exits
-d - Run container in background and print the ID
```
```bash
docker volume list
docker volume create gitlab-runner-config
docker volume inspect gitlab-runner-config

# create the volume for gitlab-runner
docker run -d --name gitlab-runner --restart always -v gitlab-runner-config:/etc/gitlab-runner -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner

# register GitlabRunner installed in docker
docker run --rm -it -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner register

sudo cat /var/lib/docker/volumes/gitlab-runner-config/_data/config.toml

# stop and remove container
docker stop gitlab-runner
docker rm gitlab-runner
```


 -с / --change применяет инструкцию к создаваемому образу. В данном случе мы берем контейнер create-image-from-me, командой commit создаем из него образ newimage, опцией --change определяя команду (аналогичную таковой Dockerfile)
 ```bash
 docker commit --change='CMD ["python3"]' create-image-from-me myimage
 ```
 
 Dockerfile - описывает процесс создания образа
 `FROM` - из какого базового образа создем новый образ
 * C помощью образов
 * С помощью Dockerfile
 
 #### 10. First arg on cmd 
 ```Dockerfile
 При использовании режима exec для ENTRYPOINT аргументы CMD добавляются в конце.
 
 # Dockerfile
FROM ubuntu:14.04
ENTRYPOINT echo Hello $0!
CMD ["World"]
 ```
 
 #### 11. Dockerfile
```Dockerfile
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
```bash
docker rmi $(docker images -f "dangling=true" -q)
```

#### Python virtualenv
```bash
virtualenv -p python3 virtualenv
cd virtualenv/bin
source activate
pip3 install wrapt==1.10.1
pip3 install 'requests<=1.9'
pip3 install 'snakemake<=3.13.3'
``` 
для работы Snakemake требуется Python 3. Пример работы с virtualenv:
```bash
pip3 install snakemake

# Create virtual environment with name 'venv'
virtualenv venv
# Activate virtual environment
. venv/bin/activate
# Do whatever you want to, e.g. install dependencies 
# Exit from virtual environment
deactivate
```
#### Snakemake: words counter from file
```yaml
rule count:
  input: "input/input"
  output: "output/output"
  shell: "wc -w < {input} > {output}"

rule generate:
  output: "output/output"
  shell: "touch {output}"
```

#### Snakemake: copy files with editing
```yaml
# all files in current dir
FILES = [file for file in shell("ls input/", iterable=True)]

# for iterating through files
rule all:
  input: expand("output/{file}", file=FILES)

# for each file
rule copy_edited_files:
  input: "input/{file}"
  output: "output/{file}"
  shell: "echo Hello $(cat {input})! > {output}"
``` 
граф пайплайна, описанного в файле Snakefile, можно сохранить:
```bash
snakemake -s Snakefile --dag | dot -Tsvg > pipeline.svg
```
Или вывести на экран:
```bash
snakemake -s Snakefile --dag | dot -Tsvg | display
```
How to use python in Snakefile - for copy files from input directory to output dir
```yaml
def gen(wildcards):
  return ["out/{}".format(i) for i in range(1,6)]


rule all:
  input: gen
  output: touch(".status")


rule copy:
  input: "input/{file}"
  output: "out/{file}"
  shell: "cp {input} {output}"
```
Snakefile for task - characters counter
```yaml
FILES = [file for file in shell("ls input/", iterable=True)]

rule all:
  input: expand("output/{file}", file=FILES)
  output: touch(".status")

rule copy:
  input: "input/{file}"
  output: "output/{file}"
  run:
    print("Input::", input)
    print("Out:: ", output)    
    with open(str(input), "r") as f:
      txt = f.readline().strip()
      d = {key: txt.count(key) for key in set([ch for ch in txt])}
      result = str("\n".join(["{}: {}".format(key, d[key]) for key in sorted(d.keys())]))
      with open(str(output), "w") as outfile:
        outfile.write(result)   
```
#### CWL - common workflow language

##### Проверка 
```yaml
cwltool --outdir output word-count.cwl --input_file input/input
```
v1 Words counter
```yaml
cwlVersion: v1.0
class: CommandLineTool

requirements:
  InitialWorkDirRequirement:
    listing:
      - entryname: example.sh
        entry: |-
          #!/bin/bash
          filename=`echo $(inputs.input_file.location) | awk '{ split($0,array,"://")} END{print array[2]}'`
          cat $filename | wc -w
inputs:
  input_file:
    type: File
    inputBinding:
      position: 1

outputs:
  output_file:
    type: File
    outputBinding: 
      glob: output/output

baseCommand: ["sh", "example.sh"]
stdout: output/output
```
v2 Words counter
```yaml
cwlVersion: v1.0
class: CommandLineTool

baseCommand: wc
arguments: ["-w"]

stdout: output
inputs:
  input_file: stdin

outputs:
  output_file: stdout
```


# Docker and containers
- **independent, standartized application package**
- used in different development environments
- **Environment is your lamguage, framework and runtimes**
- to be sure that your application is used this exact version

### When и когда?
- когда среды теста и прода могут быть различны
- когда вы работаете над несколькими проектами
- когда версии и зависимости одного проекта не совместимы с вашей локальной системой
- lower impact on OS, faster, minimal disk usage
- encapsulates environment instead of whole machine

### Difference with operating system
- your operating system Virtual OS
- another machine
- general overhead, like a standalone machie and a lot of resource consumption
- default setup process
- bigger imppact on OS, slower, higher disk space usage
- sharing and rebuilding can be challenging
- encapculates "whole machine" instead of environment

`Docker is just most common used tool for creating and managing containers`

## Why Docker Toolbox? (for old unsupported versions of OS)
- Docker toolbox эмулирует виртуальную машину линукса, на системах где нельзя установить docker desktop
- Docker engine Deamon uses Linux specific kernel features - so you cannot install directly on Windows
- you can use docker-machine to install small Linux VM on your machine
- last versions of windows does not require it

## Docker tools and building blocks
- Docker Engine Deamon installs always -> Docker Desktop (incl CLI)
- Docker Hub
- Docker Compose
- > Kubernetes

## Images 
- everything on the **image IS READONLY**
- container is runnning unit of application
- `COPY . .`
- первая точка значит - текущая директория вне контейнера (Где расположен сам докерфайл) - HOST FILE SYSTEM
- вторая точка означает текущий IMAGE/CONTAINER FILE SYSTEM
- COPY `./` означает в текущий `WORKDIR`
- `RUN npm install` тоже запуститься в заданном `WOKRDIR`
- `EXPOSE` со внутренним портом контейнера поделиться с хост машиной
- `docker run -p` option в каком локальном порту запустить контейнер? 3000:80 (host:container)
- `docker build .` - near the dockerfile
- `docker run IMAGE_ID`
- фишка - можно не полностью вводить ID запускаемого образа*, он найдет по началу уникальной строки
- **LAYER BASED ARCHITECTURE** - докер кэширует каждый исполняемый слой, обратно исполняются только измененные сценарии либо ресурсы - поэтому последующая сборка проходит быстрее
- каждая инструкция это новый слой в докер контейнере

#### Опция `-d` при запуске контейнера -detached mode - не показывать логи в консоли, запускать on background (по умолчанию attached)
#### Начать читать логи контейнера `docker logs -f some_container` или с командой `docker attach container_name` - for STDOUR/STDERR signals
#### Interactive mode `docker run -it ID` - STDIN - to provide input
- option `-rm` helps to automatically remove running container
- Команда `docker cp local/file container_name:/test` позволяет скопировать файл в контейнер или из него в хостовую ОС `docker cp container_name:/test local/file`
```bash
# From host to container
tansh@tansh:~$ docker cp AAAAAA.txt clever_newton:/new_AAAAA.txt
Successfully copied 2.05kB to clever_newton:/new_AAAAA.txt

# From container to host 
tansh@tansh:~$ docker cp clever_newton:/BBBB.txt host_BBBB.txt
Successfully copied 2.05kB to /home/tansh/host_BBBB.txt
```
docker image prune -a
- образы с одним именем можно тегировать '-t' option when you're building an image - это как метка или версия образа
- ставить на прод latest опасно и чревато нагрузкой на сеть

## Харнение данных в docker образе и контейнерах
1) readonly, inside image (built-in) mode
2) read+write containers, temporary - dynamic and changable **stored in memory**
3) read+write containers+volumes permanent - must not be lost if container stop / restarts **stored in a file or database**

каждый слой в докер контейнере кэшиурется и при последу№щей сборке будет использован кэш этого слоя. 
### Увеличить кол-во виртуальной памяти  
```bash
sudo sysctl -w vm.max_map_count=262144
```
### Why alpine is not preferred?
- alpine сборки могут увеличивать время билда - содержать некоторые ошибки в либах или снижение в производительности
- использование alpine версии для питона плохая идея!
why?
- стандартная библиотека debian линукса принимает уже скомпилированные бинарные `.whl` пакеты
- для alpine версий скачиваются исходники в сжатом формате `.tar.gz`. Для alpine linux используется musl который переводит source код в С код. Это доп расходы по сравнению со стандратной gclib (C library) который используется в том числе и для питона
- некоторые пакеты питона PyPl используют готовый wheel который значительно ускоряет процесс сборки
- при использовании Alpine Linux каждый используемый пакет нужно изначально скомпилировать в С код

# Dockerfile
- очень полезная универсальная статья
- https://habr.com/ru/companies/wunderfund/articles/586778/
### ADD and COPY
```Dockerfile
# Копирование локальных файлов с хоста в целевую директорию
COPY /source/path  /destination/path
ADD /source/path  /destination/path

# Загрузка внешнего файла и копирование его в целевую директорию
ADD http://external.file/url  /destination/path

# Копирование и распаковка локального сжатого файла
ADD source.file.tar.gz /destination/path
```
### CMD and Entrypoint
cmd можно без никаких параметров передать при запуске контейнера
для entrypoint нужно явно переопределить аргументы
- есть два способа задать аргументы командной строки
1) с помощью массивов **array form** - рекомендуется - мы работаем с самим PID запущенного приложения
2) с помощью строковой команды **bash srting form** - не рекомендуется  - идет работа напрямую с bash - SIGTERM может ожидать до 10 сек
shell format не всегда быстро реагирует на Ctrl + C 
используйте инструкцию HEALTHCHECK - покажет нездоровый запуск контейнера

есть специальный линтер для проверки написанного докерфайла - HADOLINT

### HEALTHCHECK
- в докерфайте есть отдельная инструкция которая на момент запуска контейнера покажет некорректно поднятый сервер, хотя состояние контейнера будет выглядеть как запущенное
