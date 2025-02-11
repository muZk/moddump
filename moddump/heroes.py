import i18n
from utils import camelcase
from abilities import Ability

attribute_constants = {
    'DOTA_ATTRIBUTE_STRENGTH': 'str',
    'DOTA_ATTRIBUTE_AGILITY': 'agi',
    'DOTA_ATTRIBUTE_INTELLECT': 'int'
}


class Hero(object):
    def __init__(self, heroes, abilities, language_file, addon, include=[]):
        self.heroes = heroes['DOTAHeroes']
        self.abilities = abilities['DOTAAbilities']
        self.language_file = language_file
        self.language = language_file['lang']['Language']
        self.include = include
        self.addon = addon

    def default(self, key, attr):
        return self.heroes[key].get(attr)

    def parse_hero(self, key):
        hero = {
            'name': i18n.t(key, self.language, self.language_file),
            'lore': i18n.t('%s_lore' % key, self.language, self.language_file),
            'primary_attribute': attribute_constants.get(self.default(key, 'AttributePrimary')),
            'str': self.default(key, 'AttributeBaseStrength'),
            'agi': self.default(key, 'AttributeBaseAgility'),
            'int': self.default(key, 'AttributeBaseIntelligence'),
            'str_gain': self.default(key, 'AttributeStrengthGain'),
            'agi_gain': self.default(key, 'AttributeAgilityGain'),
            'int_gain': self.default(key, 'AttributeIntelligenceGain'),
            'movement_speed': self.default(key, 'MovementSpeed'),
            'attack_range': self.default(key, 'AttackRange'),
            'damage_max': self.default(key, 'AttackDamageMax'),
            'damage_min': self.default(key, 'AttackDamageMin')
        }
        if len(self.include) > 0:
            for attr in self.include:
                hero[camelcase(attr)] = self.default(key, attr)
        # Include abilities
        hero['abilities'] = {}
        ability = Ability(self.abilities, self.language, self.language_file)
        index = 1
        while 'Ability%s' % index in self.heroes[key]:
            hero['abilities'][str(index)] = ability.parse_ability(self.default(key, 'Ability%s' % index))
            index += 1
        return hero

    def parse(self):
        parsed = {}
        parsed['Heroes'] = {}
        parsed['Language'] = self.language
        for hero_key, value in self.heroes.iteritems():
            if hero_key in self.addon.available_heroes:
                parsed['Heroes'][hero_key] = self.parse_hero(hero_key)
        return parsed
