## Ansible

- подход infrastructure as a code
- Система управления конфигурациями
- не создан для того чтобы

### Плюсы:

- Over SSH - не нужно открывать доп порты (для работы нужен только доступ по ssh)
- Agengtless - не нужно доп ничего ставить (Python)
- Pyhtod-based - написан на Питоне, легко дописывать
- By RedHat - ready for enterprize

### Базовая схема
- `Control Node` - система с установленным Ansible (где происходит контроль)
- `Inventory` - список хостов для управления, разбитый по группам
- `Managed Node` - управляемая система

### Inventory
- Файл управляемых хостов
- формат `ini` (если мало) или `yaml` формат (если много - появился недавно)
- `ansible-inventory -i inventory.ini --list`
- хосты можно объединять в группу
- `ansible all -m ping -i inventory.ini`
- Группы хостов задают по правилу `What(db, web, cache), Where(datacenter, region, floot), When (dev, test, prod)` + осознанные названия


vim inventory.ini
```
[workers]
worker1 ansible_host=192.168.30.1
worker2 ansible_host=127.0.0.1

[workers:vars]
ansible_user=nick ansible_ssh_private_key_file=~/.ssh.infra
```

```
ansible workers -m ping -i inventory.ini
```

### Выолняемые единицы
- Module - 
- Task - 
- Play - уполрядоченный список task-oв который выполняется на указанной managed node
- Playbook - упорядоченный список play-eв, для достижения цели

### Roles


