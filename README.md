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
