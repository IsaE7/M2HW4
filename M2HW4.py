from enum import Enum
from random import randint, choice


class SuperAbility(Enum):
    CRITICAL_DAMAGE = 1
    BOOST = 2
    BLOCK_DAMAGE_AND_REVERT = 3
    HEAL = 4


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.stunned = False

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if (hero.ability == SuperAbility.BLOCK_DAMAGE_AND_REVERT and
                        self.__defence != SuperAbility.BLOCK_DAMAGE_AND_REVERT):
                    block = choice([5, 10])
                    hero.health -= (self.damage - block)
                    hero.blocked_damage = block
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss, heroes):
        coefficient = randint(2, 5)
        boss.health -= self.damage * coefficient
        print(f'Warrior {self.name} hits critically {self.damage * coefficient}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOOST)

    def apply_super_power(self, boss, heroes):
        boost_amount = randint(5, 10)
        print(f'Magic {self.name} boosts heroes attack by {boost_amount}')
        for hero in heroes:
            if hero.health > 0:
                hero.damage += boost_amount


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BLOCK_DAMAGE_AND_REVERT)
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.blocked_damage}')


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.has_revived = False

    def apply_super_power(self, boss, heroes):
        if not self.has_revived:
            for hero in heroes:
                if hero.health <= 0:
                    print(f'Witcher {self.name} sacrifices himself to revive {hero.name}')
                    hero.health = self.health
                    self.health = 0
                    self.has_revived = True
                    return


class Hacker(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.steal_round = True

    def apply_super_power(self, boss, heroes):
        if self.steal_round:
            steal_amount = randint(10, 30)
            target_hero = choice([hero for hero in heroes if hero.health > 0])
            boss.health -= steal_amount
            target_hero.health += steal_amount
            print(f'Hacker {self.name} steals {steal_amount} health from Boss and gives it to {target_hero.name}')
        self.steal_round = not self.steal_round


class Golem(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOOST)

    def apply_super_power(self, boss, heroes):
        shared_damage = boss.damage // 5
        print(f'Golem {self.name} takes {shared_damage} damage from each hero')
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += shared_damage
                self.health -= shared_damage


class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss, heroes):
        if randint(1, 4) == 1:
            print(f'Thor {self.name} stunned the Boss!')
            boss.stunned = True


class TrickyBastard(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)
        self.fake_dead = False

    def apply_super_power(self, boss, heroes):
        if not self.fake_dead and randint(1, 4) == 1:
            print(f'TrickyBastard {self.name} pretends to be dead')
            self.fake_dead = True
        elif self.fake_dead:
            print(f'TrickyBastard {self.name} is back in the fight')
            self.fake_dead = False


round_number = 0


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def show_statistics(boss, heroes):
    print(f'ROUND {round_number} ----------------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    if not boss.stunned:
        boss.attack(heroes)
    else:
        print("Boss is stunned and skips his turn")
        boss.stunned = False

    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and hero.ability != boss.defence:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def start_game():
    boss = Boss('Serega', 4000, 50)
    warrior_1 = Warrior('Aron', 290, 10)
    warrior_2 = Warrior('Hektor', 280, 15)
    magic = Magic('Hendolf', 270, 10)
    doc = Medic('Leonard', 250, 5, 15)
    assistant = Medic('Sacura', 300, 5, 5)
    berserk = Berserk('Gatz', 260, 20)
    witcher = Witcher('Geralt', 300, 0)
    hacker = Hacker('Neo', 280, 10)
    golem = Golem('Rocky', 500, 5)
    thor = Thor('Thor', 300, 20)
    tricky_bastard = TrickyBastard('Loki', 250, 15)

    heroes_list = [warrior_1, warrior_2, doc, magic, berserk, assistant, witcher, hacker, golem, thor, tricky_bastard]

    show_statistics(boss, heroes_list)

    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()

