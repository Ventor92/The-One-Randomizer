export interface Character {
  id: string;
  name: string;
  class: CharacterClass;
  level: number;
  experience: number;
  attributes: Attributes;
  hitPoints: {
    current: number;
    maximum: number;
  };
  armorClass: number;
  skills: Skill[];
  equipment: Equipment[];
  spells: Spell[];
  background: string;
  notes: string;
}

export interface Attributes {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

export interface CharacterClass {
  name: string;
  description: string;
  hitDie: number;
  primaryAttributes: string[];
  skillProficiencies: string[];
}

export interface Skill {
  name: string;
  attribute: keyof Attributes;
  proficient: boolean;
  bonus: number;
}

export interface Equipment {
  id: string;
  name: string;
  type: 'weapon' | 'armor' | 'shield' | 'accessory' | 'consumable' | 'misc';
  description: string;
  quantity: number;
  weight: number;
  value: number;
  equipped: boolean;
  properties?: string[];
}

export interface Spell {
  id: string;
  name: string;
  level: number;
  school: string;
  castingTime: string;
  range: string;
  components: string;
  duration: string;
  description: string;
  prepared: boolean;
}

export interface Campaign {
  id: string;
  name: string;
  description: string;
  gameMaster: string;
  players: string[];
  characters: Character[];
  sessions: Session[];
  notes: string;
}

export interface Session {
  id: string;
  date: string;
  title: string;
  summary: string;
  experience: number;
  treasure: string[];
}

export interface DiceRoll {
  id: string;
  timestamp: number;
  dice: string;
  result: number;
  breakdown: number[];
  modifier: number;
  character?: string;
  purpose?: string;
}