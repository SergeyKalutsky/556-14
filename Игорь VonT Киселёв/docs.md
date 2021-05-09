# **\*Название игры\***

- **Жанр**: Top-down shooter(Перспектива свеху)/Battle Royale
- **Враги**: Будут
- **Цель**: Уничтожить других игроков/открывать новых персоонажей и оружие
- __Однопользовательская__(_В преспективе_ ___многопользовательская___)

## Классы:
```
    Player:
        attributes:
            x
            y
            move_direction
            ammo
            sprite
            weapon
            healt_points
            stamina
            in_shadow
            run
            speed
        methods:
            __init__()
            move()
            run()
            pick_item()
            use_item()

    Weapon:
        attributes:
            bullets
            sprite
            shoot_per_second
            reload_speed
            automatic_shooting
            angle
        methods:
            __init__()
            shoot()

    Bullet:
        attributes:
            x
            y
            sprite
            move_direction
        methods:
            __init__()
            move()
    
    Tile:
        attributes:
            x
            y
            sprite
            bg_or_fg
            fake
        methods:
            __init__()
    
    Camera:
        attributes:
            x
            y
        methods:
            __init__()
            follow_the_object()
```
