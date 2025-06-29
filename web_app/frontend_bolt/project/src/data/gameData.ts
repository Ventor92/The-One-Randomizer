import { CharacterClass, Skill } from '../types/game';

export const CHARACTER_CLASSES: CharacterClass[] = [
  {
    name: 'Warrior',
    description: 'Masters of combat, wielding sword and shield with unmatched prowess.',
    hitDie: 10,
    primaryAttributes: ['strength', 'constitution'],
    skillProficiencies: ['Athletics', 'Intimidation', 'Survival', 'Perception']
  },
  {
    name: 'Rogue',
    description: 'Stealthy infiltrators and masters of precision strikes.',
    hitDie: 8,
    primaryAttributes: ['dexterity', 'intelligence'],
    skillProficiencies: ['Stealth', 'Sleight of Hand', 'Investigation', 'Deception']
  },
  {
    name: 'Mage',
    description: 'Wielders of arcane magic, bending reality to their will.',
    hitDie: 6,
    primaryAttributes: ['intelligence', 'wisdom'],
    skillProficiencies: ['Arcana', 'History', 'Investigation', 'Medicine']
  },
  {
    name: 'Cleric',
    description: 'Divine servants who channel holy power to heal and protect.',
    hitDie: 8,
    primaryAttributes: ['wisdom', 'charisma'],
    skillProficiencies: ['Medicine', 'Religion', 'Insight', 'Persuasion']
  },
  {
    name: 'Ranger',
    description: 'Guardians of the wilderness, tracking foes and protecting nature.',
    hitDie: 10,
    primaryAttributes: ['dexterity', 'wisdom'],
    skillProficiencies: ['Survival', 'Animal Handling', 'Athletics', 'Perception']
  },
  {
    name: 'Bard',
    description: 'Charismatic performers who weave magic through music and story.',
    hitDie: 8,
    primaryAttributes: ['charisma', 'dexterity'],
    skillProficiencies: ['Performance', 'Persuasion', 'Deception', 'History']
  }
];

export const BASE_SKILLS: Omit<Skill, 'proficient' | 'bonus'>[] = [
  { name: 'Athletics', attribute: 'strength' },
  { name: 'Acrobatics', attribute: 'dexterity' },
  { name: 'Sleight of Hand', attribute: 'dexterity' },
  { name: 'Stealth', attribute: 'dexterity' },
  { name: 'Arcana', attribute: 'intelligence' },
  { name: 'History', attribute: 'intelligence' },
  { name: 'Investigation', attribute: 'intelligence' },
  { name: 'Nature', attribute: 'intelligence' },
  { name: 'Religion', attribute: 'intelligence' },
  { name: 'Animal Handling', attribute: 'wisdom' },
  { name: 'Insight', attribute: 'wisdom' },
  { name: 'Medicine', attribute: 'wisdom' },
  { name: 'Perception', attribute: 'wisdom' },
  { name: 'Survival', attribute: 'wisdom' },
  { name: 'Deception', attribute: 'charisma' },
  { name: 'Intimidation', attribute: 'charisma' },
  { name: 'Performance', attribute: 'charisma' },
  { name: 'Persuasion', attribute: 'charisma' }
];

export const SAMPLE_SPELLS = [
  {
    id: '1',
    name: 'Magic Missile',
    level: 1,
    school: 'Evocation',
    castingTime: '1 action',
    range: '120 feet',
    components: 'V, S',
    duration: 'Instantaneous',
    description: 'Three darts of magical force strike unerringly at targets within range.',
    prepared: false
  },
  {
    id: '2',
    name: 'Shield',
    level: 1,
    school: 'Abjuration',
    castingTime: '1 reaction',
    range: 'Self',
    components: 'V, S',
    duration: '1 round',
    description: 'An invisible barrier of magical force protects you, granting +5 AC.',
    prepared: false
  },
  {
    id: '3',
    name: 'Fireball',
    level: 3,
    school: 'Evocation',
    castingTime: '1 action',
    range: '150 feet',
    components: 'V, S, M',
    duration: 'Instantaneous',
    description: 'A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame.',
    prepared: false
  }
];