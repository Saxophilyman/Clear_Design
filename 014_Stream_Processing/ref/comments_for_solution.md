Приблизительная схема

Простые Commands и Events.  
Events делятся на события-запросы и события-результаты/ 
EventStore делают "подписку", содержит историю состояний и запросов
"тупой" CommandHandler, превращает команду в событие-запрос.
Event Processors как модуль бизнес-логики

```
Command
    -> to_event()
    -> RequestedEvent

CommandHandler
    -> принимает Command
    -> вызывает command.to_event()
    -> сохраняет RequestedEvent в EventStore

EventStore
    -> сохраняет событие
    -> уведомляет подписанные EventProcessor'ы

EventProcessor
    -> получает RequestedEvent
    -> восстанавливает/читает состояние
    -> выполняет бизнес-логику
    -> порождает ResultEvent

ResultEvent
    -> apply(state)
```

`Command -> RequestedEvent -> Processor -> ResultEvent`
1. RequestedEvent — кто-то запросил действие.
2. ResultEvent — действие действительно произошло и может изменить состояние.

Протокол Event - не все события изменяют состояние напрямую.  
Протокол ResultEvent - событие, которое реально меняет или воспроизводит состояние.  
Протокол Command - команда to_event превращается в событие-запрос(при корректности).  
Сами Command имеют проверки по части валидности, но вся бизнес логика проверок - в процессорах.  

Requested-события(события-запросы) - **кто-то попросил робота что-то сделать**  
Result-события - **робот уже что-то сделал**  
EventStore - subscribe подписывает процессор на события, после этого каждый раз, 
когда в EventStore добавят событие, все процессоры его увидят(когда событие добавляется (append)).
Теперь EventStore.append() не просто сохраняет событие, но ещё и запускает процессоры. 
То есть делает 2 разных дела, что тое не совсем хорошо.


цепочка выполнения:
1. CommandHandler вызывает command.to_event()
2. Получает MoveRequestedEvent
3. EventStore.append(MoveRequestedEvent)
4. EventStore сохраняет MoveRequestedEvent
5. EventStore передаёт его всем процессорам
6. MoveProcessor узнаёт свой тип события
7. MoveProcessor добавляет RobotMovedEvent
8. EventStore сохраняет RobotMovedEvent
9. EventStore снова передаёт RobotMovedEvent всем процессорам
10. Все процессоры его игнорируют

Команда больше не решает всё сама.
Она только создаёт запрос.
Процессор решает, превратить ли запрос в реальный факт.

Процессоры не уходят в бесконечный цикл, потому что каждый процессор проверяет тип события, но это хрупко.
Но это ключевая разница между эталоном(к вопросу о RLock)


--------

Сила эталона

```
EventStore
    -> subscribers
        -> processors
            -> new events
                -> subscribers
```
Краткая разница:
``` 
CommandHandler
    -> append event
        -> processors react
```
vs
``` 
EventStore
    -> subscriber system
        -> processors independently react to stream
```
1. Процессоры становятся полноценными независимыми агрегаторами
   - сам восстанавливает состояние;
   - сам вычисляет новое;
   - сам генерирует result-events.

2. Появляется CQRS-мышление - а у нас этого не было?
``` 
Commands
    ->
RequestedEvents
    ->
ResultEvents
```
Разделение для чтения и записи

3. LoggingProcessor - как архитектурная мысль - у нас подобного разве не было?
4. StateProjector как отдельная архитектурная роль - снова пропустил - надо было брать с предыдущего задания. Строит только read model.
5. События, более информативные. Более полное отражение истории
6. RLock

``` 
append_events()
    внутри себя
        вызывает append_events()
```
reentrant call.

7. processors подписываются прямо внутри базового EventProcessor `self._event_store.subscribe(self._handle_event)`


Ещё раз отмечая:
 - добавление нового функционала можно осуществить почти без изменений основного кода.
 - происходит разделение потоков ответственности.
 - сама система начинает управлять собой через поток событий.
 - управление становится распределённым.
 - процессоры независимы
 - publish-subscribe модель
 - command и event
 - Projection / read model - не хранит истину, строит представление истины.
 - reentrant
``` 

```

``` 

```