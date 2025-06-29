import React, { useState } from 'react';
import { Character, Attributes } from '../types/game';
import { CHARACTER_CLASSES, BASE_SKILLS } from '../data/gameData';
import { User, Dices, Save } from 'lucide-react';

interface CharacterCreatorProps {
  onCreateCharacter: (character: Character) => void;
  onCancel: () => void;
}

export const CharacterCreator: React.FC<CharacterCreatorProps> = ({ onCreateCharacter, onCancel }) => {
  const [name, setName] = useState('');
  const [selectedClass, setSelectedClass] = useState(CHARACTER_CLASSES[0]);
  const [attributes, setAttributes] = useState<Attributes>({
    strength: 10,
    dexterity: 10,
    constitution: 10,
    intelligence: 10,
    wisdom: 10,
    charisma: 10
  });
  const [background, setBackground] = useState('');
  const [pointsRemaining, setPointsRemaining] = useState(27);

  const rollAttributes = () => {
    const newAttributes: Attributes = {
      strength: rollStat(),
      dexterity: rollStat(),
      constitution: rollStat(),
      intelligence: rollStat(),
      wisdom: rollStat(),
      charisma: rollStat()
    };
    setAttributes(newAttributes);
    calculatePointBuy(newAttributes);
  };

  const rollStat = (): number => {
    const rolls = Array.from({ length: 4 }, () => Math.floor(Math.random() * 6) + 1);
    rolls.sort((a, b) => b - a);
    return rolls.slice(0, 3).reduce((sum, roll) => sum + roll, 0);
  };

  const calculatePointBuy = (attrs: Attributes) => {
    const baseCost = Object.values(attrs).reduce((total, value) => {
      if (value <= 13) return total + (value - 8);
      if (value === 14) return total + 7;
      if (value === 15) return total + 9;
      return total + 12; // 16+ costs more in real point buy
    }, 0);
    setPointsRemaining(27 - baseCost);
  };

  const updateAttribute = (attr: keyof Attributes, value: number) => {
    const newAttributes = { ...attributes, [attr]: Math.max(8, Math.min(15, value)) };
    setAttributes(newAttributes);
    calculatePointBuy(newAttributes);
  };

  const createCharacter = () => {
    if (!name.trim()) return;

    const constitutionModifier = Math.floor((attributes.constitution - 10) / 2);
    const maxHitPoints = selectedClass.hitDie + constitutionModifier;

    const skills = BASE_SKILLS.map(baseSkill => ({
      ...baseSkill,
      proficient: selectedClass.skillProficiencies.includes(baseSkill.name),
      bonus: 0
    }));

    const character: Character = {
      id: Date.now().toString(),
      name: name.trim(),
      class: selectedClass,
      level: 1,
      experience: 0,
      attributes,
      hitPoints: {
        current: maxHitPoints,
        maximum: maxHitPoints
      },
      armorClass: 10 + Math.floor((attributes.dexterity - 10) / 2),
      skills,
      equipment: [],
      spells: [],
      background: background.trim(),
      notes: ''
    };

    onCreateCharacter(character);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-white mb-2">Create Your Character</h2>
        <p className="text-purple-200">Forge a legend in the New Origin</p>
      </div>

      {/* Basic Info */}
      <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <User className="w-5 h-5 text-purple-400" />
          Character Details
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter character name"
              className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-400"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">Class</label>
            <select
              value={selectedClass.name}
              onChange={(e) => setSelectedClass(CHARACTER_CLASSES.find(c => c.name === e.target.value)!)}
              className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-purple-400"
            >
              {CHARACTER_CLASSES.map(cls => (
                <option key={cls.name} value={cls.name} className="bg-gray-800">{cls.name}</option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="mt-4">
          <label className="block text-sm font-medium text-purple-200 mb-2">Background</label>
          <input
            type="text"
            value={background}
            onChange={(e) => setBackground(e.target.value)}
            placeholder="e.g., Noble, Soldier, Merchant"
            className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-400"
          />
        </div>
        
        <div className="mt-4 p-4 bg-black/20 rounded-lg">
          <h4 className="text-purple-200 font-semibold mb-2">{selectedClass.name}</h4>
          <p className="text-gray-300 text-sm mb-2">{selectedClass.description}</p>
          <div className="text-sm text-purple-200">
            <span className="font-semibold">Hit Die:</span> d{selectedClass.hitDie} | 
            <span className="font-semibold ml-2">Primary:</span> {selectedClass.primaryAttributes.join(', ')}
          </div>
        </div>
      </div>

      {/* Attributes */}
      <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Dices className="w-5 h-5 text-purple-400" />
            Attributes
          </h3>
          <button
            onClick={rollAttributes}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-4 py-2 rounded-lg text-white font-semibold transition-all"
          >
            Roll Stats
          </button>
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          {Object.entries(attributes).map(([attr, value]) => {
            const modifier = Math.floor((value - 10) / 2);
            const isPrimary = selectedClass.primaryAttributes.includes(attr);
            
            return (
              <div key={attr} className={`bg-black/20 rounded-lg p-4 text-center border-2 ${
                isPrimary ? 'border-yellow-500/50' : 'border-transparent'
              }`}>
                <div className="text-sm text-purple-200 uppercase font-semibold mb-2 flex items-center justify-center gap-1">
                  {attr}
                  {isPrimary && <span className="text-yellow-400">★</span>}
                </div>
                <div className="flex items-center justify-center gap-2 mb-2">
                  <button
                    onClick={() => updateAttribute(attr as keyof Attributes, value - 1)}
                    className="w-6 h-6 bg-purple-600 hover:bg-purple-700 rounded text-white text-xs"
                  >
                    -
                  </button>
                  <span className="text-2xl font-bold text-white w-8">{value}</span>
                  <button
                    onClick={() => updateAttribute(attr as keyof Attributes, value + 1)}
                    className="w-6 h-6 bg-purple-600 hover:bg-purple-700 rounded text-white text-xs"
                  >
                    +
                  </button>
                </div>
                <div className="text-lg text-yellow-400 font-semibold">
                  {modifier >= 0 ? `+${modifier}` : `${modifier}`}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-center gap-4">
        <button
          onClick={onCancel}
          className="px-6 py-3 bg-gray-600 hover:bg-gray-700 rounded-lg text-white font-semibold transition-colors"
        >
          Cancel
        </button>
        <button
          onClick={createCharacter}
          disabled={!name.trim()}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed rounded-lg text-white font-semibold transition-all flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          Create Character
        </button>
      </div>
    </div>
  );
};