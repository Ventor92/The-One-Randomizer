import React from 'react';
import { Character } from '../types/game';
import { Sword, Shield, Heart, Star, User, Scroll } from 'lucide-react';

interface CharacterSheetProps {
  character: Character;
  onUpdateCharacter: (character: Character) => void;
}

export const CharacterSheet: React.FC<CharacterSheetProps> = ({ character, onUpdateCharacter }) => {
  const getAttributeModifier = (score: number): number => {
    return Math.floor((score - 10) / 2);
  };

  const formatModifier = (modifier: number): string => {
    return modifier >= 0 ? `+${modifier}` : `${modifier}`;
  };

  const updateAttribute = (attribute: keyof Character['attributes'], value: number) => {
    const updatedCharacter = {
      ...character,
      attributes: {
        ...character.attributes,
        [attribute]: Math.max(3, Math.min(20, value))
      }
    };
    onUpdateCharacter(updatedCharacter);
  };

  const updateHitPoints = (current: number) => {
    const updatedCharacter = {
      ...character,
      hitPoints: {
        ...character.hitPoints,
        current: Math.max(0, Math.min(character.hitPoints.maximum, current))
      }
    };
    onUpdateCharacter(updatedCharacter);
  };

  return (
    <div className="space-y-6">
      {/* Character Header */}
      <div className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
        <div className="flex items-center gap-4 mb-4">
          <User className="w-8 h-8 text-purple-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">{character.name}</h2>
            <p className="text-purple-200">Level {character.level} {character.class.name}</p>
          </div>
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-black/20 rounded-lg p-3 text-center">
            <Heart className="w-5 h-5 text-red-400 mx-auto mb-1" />
            <div className="text-sm text-gray-300">Hit Points</div>
            <div className="flex items-center justify-center gap-2">
              <input
                type="number"
                value={character.hitPoints.current}
                onChange={(e) => updateHitPoints(Number(e.target.value))}
                className="w-16 bg-black/50 border border-red-500/50 rounded px-2 py-1 text-white text-center"
              />
              <span className="text-gray-400">/</span>
              <span className="text-white font-bold">{character.hitPoints.maximum}</span>
            </div>
          </div>
          
          <div className="bg-black/20 rounded-lg p-3 text-center">
            <Shield className="w-5 h-5 text-blue-400 mx-auto mb-1" />
            <div className="text-sm text-gray-300">Armor Class</div>
            <div className="text-xl font-bold text-white">{character.armorClass}</div>
          </div>
          
          <div className="bg-black/20 rounded-lg p-3 text-center">
            <Star className="w-5 h-5 text-yellow-400 mx-auto mb-1" />
            <div className="text-sm text-gray-300">Experience</div>
            <div className="text-xl font-bold text-white">{character.experience}</div>
          </div>
        </div>
      </div>

      {/* Attributes */}
      <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Sword className="w-5 h-5 text-purple-400" />
          Attributes
        </h3>
        
        <div className="grid grid-cols-3 gap-4">
          {Object.entries(character.attributes).map(([attr, value]) => {
            const modifier = getAttributeModifier(value);
            return (
              <div key={attr} className="bg-black/20 rounded-lg p-4 text-center">
                <div className="text-sm text-purple-200 uppercase font-semibold mb-2">
                  {attr}
                </div>
                <div className="flex items-center justify-center gap-2 mb-2">
                  <button
                    onClick={() => updateAttribute(attr as keyof Character['attributes'], value - 1)}
                    className="w-6 h-6 bg-purple-600 hover:bg-purple-700 rounded text-white text-xs"
                  >
                    -
                  </button>
                  <span className="text-2xl font-bold text-white w-8">{value}</span>
                  <button
                    onClick={() => updateAttribute(attr as keyof Character['attributes'], value + 1)}
                    className="w-6 h-6 bg-purple-600 hover:bg-purple-700 rounded text-white text-xs"
                  >
                    +
                  </button>
                </div>
                <div className="text-lg text-yellow-400 font-semibold">
                  {formatModifier(modifier)}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Skills */}
      <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Scroll className="w-5 h-5 text-purple-400" />
          Skills
        </h3>
        
        <div className="grid grid-cols-2 gap-2">
          {character.skills.map((skill, index) => {
            const attributeValue = character.attributes[skill.attribute];
            const modifier = getAttributeModifier(attributeValue);
            const totalBonus = modifier + (skill.proficient ? 2 : 0) + skill.bonus;
            
            return (
              <div key={index} className="flex items-center justify-between bg-black/20 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={skill.proficient}
                    onChange={(e) => {
                      const updatedSkills = [...character.skills];
                      updatedSkills[index] = { ...skill, proficient: e.target.checked };
                      onUpdateCharacter({ ...character, skills: updatedSkills });
                    }}
                    className="w-4 h-4 text-purple-600 rounded"
                  />
                  <span className="text-white">{skill.name}</span>
                </div>
                <span className="text-yellow-400 font-semibold">
                  {formatModifier(totalBonus)}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};