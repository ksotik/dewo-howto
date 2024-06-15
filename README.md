# Отключение уведомлений и наклеек в macOS с помощью AI

Я пробую использовать сервис https://memory.ai/dewo, который предоставляет инструмент для отслеживания активности работы в разных приложениях, и с помощью AI определяет начало сосредоточенной работы, после чего отключает уведомления.

Поддерживается Windows и macOS, мой опыт касается macOS.

Дополнительно от тех же разработчиков можно использовать сервис https://memory.ai/timely, который показывает активность в разных приложениях в виде удобного календаря и графиков. Но этот сервис платный, в отличие от Dewo.

Как же работает Dewo? На компьютер нужно установить специального демона - Memory. Этот демон связывается с учетной записью в Dewo и отправляет данные об используемых приложениях и активности. С помощью AI Dewo определяет момент продуктивности и инициирует отключение уведомлений на компьютере с помощью Memory. Отключение уведомлений производится с помощью стандартного режима "Не беспокоить" в центре уведомлений macOS.

Дополнительно есть мобильное приложение Dewo, которое позволяет управлять процессом с телефона, а также показывает Push уведомления, когда наступает режим продуктивности.

Звучит интересно - можно автоматически заглушать шум уведомлений и сосредоточенно работать. Однако в моём случае включения режима "Не беспокоить" недостаточно. У меня и так всегда отключены всплывающие уведомления, для просмотра непрочитанных сообщений или других событий я использую только наклейки (badges). К сожалению, реализация режима "Не беспокоить" в macOS отключает только уведомления и не отключает наклейки.

Но это можно исправить!

Инструкция, как настроить для себя Dewo+Memory+скрипт, автоматически отключающий наклейки - нижу. Инструкция справедлива для ОС Catalina.

## Регистрация в Dewo
Нужно зарегистрировать учетную запись на сайте https://memory.ai/dewo. Это понадобится для связки с приложением Memory.

## Установка приложения Memory
Скачать приложение можно на странице https://memory.ai/downloads.
После установки и запуска нужно связать его со своей учетной записью Dewo.

## Тест
На этом шаге уже можно потестировать сервис. Спустя какое-то время приложение уже начнет работать - будет автоматически включаться режим "Не беспокоить". Можно также установить мобильное приложение Dewo.

## Установка скрипта ncprefs и вспомогательных скриптов
Адрес: https://github.com/drewdiver/ncprefs.py (на всякий случай форк https://github.com/ksotik/ncprefs.py)

Этот скрипт на python позволяет управлять настройками уведомлений приложений с помощью терминала.
Установку будем производить в директорию `/opt/ncprefs` :
```
$ cd /opt/ncprefs
$ git clone https://github.com/ksotik/dewo-howto .
$ git clone https://github.com/drewdiver/ncprefs.py .
$ pip3 install pyobjc
```

## Список приложений, для которых нужно отключать наклейки
Список приложений и их идентификаторы можно получить с помощью скрипта ncprefs.py:
```
$ python3 ncprefs.py -l
```

Нас интересует вторая колонка, например для Telegram это `ru.keepcoder.Telegram`.

Список идентификаторов, которыми вы хотите управлтяь, нужно сохранить в файл appslist.txt.

## Настройка команды в crontab
Далее нужно только настроить запуск скрипта `badges_toggler.py`, который проверяет статус режима "Не беспокоить" и в зависимости от него отключает/включает наклейки приложений.

Для этого нужно создать файл `.crontab` в домашней директории:
```
$ touch ~/.crontab
$ nano ~/.crontab
```

со следующим содержимым:
```
*/1 * * * * /usr/local/bin/python3 /opt/ncprefs/badges_toggler.py
```

После чего сохранить файл и выполнить команду:
```
$ crontab ~/.crontab
```

Также на Catalina может возникать проблема с доступом для cron к файлам диска, решение здесь: https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/

Проверяем:
```
$ crontab -l
*/1 * * * * /usr/local/bin/python3 /opt/ncprefs/badges_toggler.py
```

Готово! Теперь каждую минуту будет запускаться скрипт, который будет отключать наклейки для нужных приложений, и возвращать их обратно, когда Dewo посчитает, что режим сосредоточенной работы завершен.

# Альтернативный способ

Вот такой командой можно отключить все наклейки на приложениях в Dock:
```
defaults write com.apple.systempreferences AttentionPrefBundleIDs 0 && killall Dock 
```

Для возвращения нужно просто перезапустить каждое приложение!
