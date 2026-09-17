## Симптом

Обновление не завершалось, новый Pod получил ImagePullBackOff


Пытался обновиться на несуществующий образ.

## Диагностика

С помощью команды

 `sudo k3s kubectl -n homelab get pods` 
 
 выяснил какой Pod не работает и с помощью команды 
 
 `sudo k3s kubectl -n homelab describe pod homelab-api-67ddf95598-6hgzr` 

 посмотрел Events в чём была проблема. Проблема `Not found`, значит, что образ с неправильным тегом не нашёлся.

## Причина

Тег `training-missing` отсутствовал в Docker Hub

## Исправление

Выполнил откат к предыдущей версии. 
Командами: 

`sudo k3s kubectl -n homelab rollout undo deployment/homelab-api`

`sudo k3s kubectl -n homelab rollout status deployment/homelab-api`

## Проверка

После отката выполнил проверку, что всё работает как раньше. 

Командами:

`sudo k3s kubectl -n homelab get deployment homelab-api`

`sudo k3s kubectl -n homelab get pods`
