## Создание загрузочного носителя

Скачать образ с [официального сайта](https://archlinux.org/download/)

Скачать средство создания образа, например [Rufus](https://rufus.ie/ru/)

Записать образ на флешку, выбрав схему раздела ***GPT***

## Загрузка с образа

Зайти в BIOS при перезагрузке компьютера
Клавиши: <kbd>Del</kbd> / <kbd>Esc</kbd> / <kbd>F2</kbd> / <kbd>F8</kbd> / <kbd>F10</kbd>

Выбрать первый вариант: "Arch Linux install medium"

В случае возникновения ошибок в BIOS отключить Secure Boot

## Подключение к интернету

Проверить подключение к интернету командой `ip addr show`
Если у "wlan0", где 0 - номер адаптера, присутствует IPv4, подключение к интернету выполнено успешно.

### Подключение по Wi-Fi

Ввести команды:
1. `iwctl`
2. `station wlan0 scan`
3. `station wlan0 get-networks`
4. `station wlan0 connect SSID` - ввести пароль
5. `exit

Повторно проверить подключение командой `ip addr show`

## Разметка диска

Получить список дисков командой `lsblk`

Открыть нужный диск командой `cfdisk /dev/диск`

Из свободного пространства создать разделы:
- EFI (при необходимости)
- Основной
- Swap (при желании)

Записать таблицу разделов кнопкой `write`

Отформатировать EFI (если создавали!) командой
`mkfs.vfat /dev/раздел_efi`

Отформатировать основной раздел командой
`mkfs.ext4 /dev/основной_раздел`

Инициализировать раздел swap (если создавали) командой
`mkswap /dev/раздел_swap`

## Монтирование разделов

Выполнить команды:
1. `mount /dev/основной_раздел /mnt`
2. `mount --mkdir /dev/раздел_efi /mnt/boot`
3. `swapon /dev/раздел_swap`

## Установка базовых компонентов

Выполнить команду `pacstrap -K /mnt base linux linux-firmware`

## Генерация файла fstab

Выполните команду `genfstab -U /mnt >> /mnt/etc/fstab`

Проверьте файл *`/mnt/etc/fstab`*

## Настройка системы

Перейдите к корневому каталогу новой системы: `arch-chroot /mnt`
### Установка пакетов

Установите пакеты командой:
```bash
pacman -S base-devel linux-headers helix grub efibootmgr os-prober bash-completion iwd sudo pacman-contrib ufw pipewire pipewire-pulse wireplumber
```

Для процессоров intel / amd установите соответствующие микрокоды:
`intel-ucode / amd-ucode`

Для видеокарт intel установите: `mesa intel-media-driver`

Для видеокарт amd установите: `mesa libva-mesa-driver`

Для видеокарт nvidia установите: `nvidia nvidia-utils`

### Создание пользователей и выдача прав

Установка пароля root: `passwd`

Создание пользователя: `useradd -m -g users -G wheel user`

Установка пароля пользователя: `passwd user`

Откройте файл командой `sudo helix /etc/sudoers`
и раскомментировать строчку `%WHEEL ALL=(ALL:ALL) ALL`

### Локали и язык

Открыть файл командой `helix /etc/locale.gen`
И раскомментировать локали:
en_US.UTF-8 UTF-8
ru_RU.UTF-8 UTF-8

Открыть файл `helix /etc/locale.conf`
И написать:
`LANG=en_US.UTF-8`

Выполнить команду `locale-gen`

### Настройка загрузчика

Открыть файл `helix /etc/default/grub`
Убрать `quiet` из параметра `GRUB_CMDLINE_LINUX_DEFAULT`
Раскомментировать строку:
`GRUB_DISABLE_OS_PROBER="false"`

Выполнить команду установки:
`grub-install --efi-directory=/boot --boot-directory=/boot`

Выполнить команду генерации настроек:
`grub-mkconfig -o /boot/grub/grub.cfg`

### Перезагрузка

1. Выйти из системы командой `exit`
2. Размонтировать все разделы `umount -R /mnt`
3. Перезагрузиться `reboot`

## В установленной системе

### Настройка интернет соединения

Открыть файл `helix /etc/iwd/main.conf`
Написать:
```
[General]
EnableNetworkConfiguration=true
```

Включить службы DNS:
1. `systemctl enable --now systemd-resolved`
2. `systemctl enable --now iwd`

Подключиться к интернету (см пункт "Подключение к интернету")

Установить фаервол `ufw`

Активировать службу: `systemctl enable --now ufw.service`

Выполнить следующие команды конфигурации:
```
# ufw default deny
# ufw allow from 192.168.0.0/24
# ufw allow Deluge
# ufw limit ssh
```

Активировать фаервол: `ufw enable`

### Обслуживание SSD (ВАЖНО!!!)

Если в вашей системе используются ssd диски, необходимо настроить для них периодический trim.

Установить пакет `util-linux`

Включить службу-таймер: `systemctl enable fstrim.timer`
