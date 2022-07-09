# docker-course-stepik
Курс управления вычислениями от Bioinformatics Institute


## Data volume containers
```
docker create -v /srv --name store2 ubuntu:14.04 bin/true
docker run -it --rm --volumes-from store2 ubuntu:14.04```
