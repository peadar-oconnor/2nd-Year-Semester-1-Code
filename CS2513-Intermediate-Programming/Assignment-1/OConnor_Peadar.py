class Character:

    # constructor
    def __init__(self, name, strength):
        if type(name) != str:
            print("type ERROR")
        else:
            self._name = name

        if type(strength) == float:
            if strength <= 0.0:
                self._strength = 0.0
            elif strength >= 5.0:
                self._strength = 5.0
            else:
                self._strength = strength
        else:
            print("type ERROR")

    # declare property
    @property
    # getter
    def name(self):
        return self._name

    # setter
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, strength):
        self._strength = strength

    # string representation
    def __str__(self):
        return "%s %.1f" % (self._name, self._strength)

    # overload of operator
    def __gt__(self, comp):
        #if they're an archer/knight they will always have a weapon
        if isinstance(self, Archer) is True:
            firstWeapon = True
        else:
            firstWeapon = self._weapon

        if isinstance(comp, Archer) is True:
            secondWeapon = True
        else:
            secondWeapon = comp._weapon

        if firstWeapon is True and secondWeapon is False:
            return True
        elif firstWeapon is False and secondWeapon is True:
            return False
        else:
            if self._strength > comp._strength:
                return True
            return False

    def fight(self, char):
        #archers/knights cant fight other archers/knights
        if isinstance(self, Archer) is True and isinstance(char, Archer) is True:
            print("fight ERROR")
        else:
            if self == char:
                return "An Orc cannot fight itself!"
            elif self > char:
                self._strength += 1
                if self._strength > 5:
                    self._strength = 5
                return self.__str__()
            elif char > self:
                char._strength += 1
                if char._strength > 5:
                    char._strength = 5
                return char.__str__()
            else:
                self._strength -= 0.5
                if self._strength < 0:
                    self._strength = 0
                char._strength -= 0.5
                if char._strength < 0:
                    char._strength = 0


class Orc(Character):
    def __init__(self, name, strength, weapon):
        Character.__init__(self, name, strength)

        if weapon is True or weapon is False:
            self._weapon = weapon
        else:
            print("type ERROR")

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, weapon):
        self._weapon = weapon

    def __str__(self):
        return "%s %s" % (Character.__str__(self), self._weapon)


class Archer(Character):
    def __init__(self, name, strength, kingdom):
        Character.__init__(self, name, strength)

        if type(kingdom) != str:
            print("type ERROR")
        else:
            self._kingdom = kingdom

    @property
    def kingdom(self):
        return self._kingdom

    @kingdom.setter
    def kingdom(self, kingdom):
        self._kingdom = kingdom

    def __str__(self):
        return "%s %s" % (Character.__str__(self), self._kingdom)


class Knight(Archer):
    def __init__(self, name, strength, kingdom, archers_list):
        Archer.__init__(self, name, strength, kingdom)

        if type(archers_list) != list:
            print("type ERROR")
        else:
            fixed_list = []
            notArcherError = 0
            for item in archers_list:
                if isinstance(item, Archer) is False:
                    notArcherError += 1
                elif self._kingdom == item._kingdom:
                    fixed_list.append(item)
            if notArcherError > 0:
                print("archers list ERROR")
            self._archers_list = fixed_list

    @property
    def archers_list(self):
        return self._archers_list

    @archers_list.setter
    def archers_list(self, archers_list):
        self._archers_list = archers_list

    def __str__(self):
        fullStrList = "["
        for item in self._archers_list:
            fullStrList += item.__str__()
            fullStrList += ", "
        fullStrList = fullStrList[:-2]
        fullStrList += "]"
        return "%s %s" % (Archer.__str__(self), fullStrList)