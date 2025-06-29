import React, { useState } from 'react';
import { Dices, Plus, Minus } from 'lucide-react';
import { DiceRoll } from '../types/game';

interface DiceRollerProps {
  onRoll: (roll: DiceRoll) => void;
  characterName?: string;
}

export const DiceRoller: React.FC<DiceRollerProps> = ({ onRoll, characterName }) => {
  const [diceType, setDiceType] = useState(20);
  const [diceCount, setDiceCount] = useState(1);
  const [modifier, setModifier] = useState(0);
  const [purpose, setPurpose] = useState('');
  const [isRolling, setIsRolling] = useState(false);

  const diceTypes = [4, 6, 8, 10, 12, 20, 100];

  const rollDice = () => {
    setIsRolling(true);
    
    setTimeout(() => {
      const breakdown: number[] = [];
      let total = 0;
      
      for (let i = 0; i < diceCount; i++) {
        const roll = Math.floor(Math.random() * diceType) + 1;
        breakdown.push(roll);
        total += roll;
      }
      
      const finalTotal = total + modifier;
      
      const diceRoll: DiceRoll = {
        id: Date.now().toString(),
        timestamp: Date.now(),
        dice: `${diceCount}d${diceType}${modifier !== 0 ? (modifier > 0 ? `+${modifier}` : modifier) : ''}`,
        result: finalTotal,
        breakdown,
        modifier,
        character: characterName,
        purpose: purpose || undefined
      };
      
      onRoll(diceRoll);
      setIsRolling(false);
    }, 1000);
  };

  return (
    <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
      <div className="flex items-center gap-3 mb-6">
        <Dices className="w-6 h-6 text-purple-400" />
        <h3 className="text-xl font-bold text-white">Dice Roller</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-purple-200 mb-2">Purpose (optional)</label>
          <input
            type="text"
            value={purpose}
            onChange={(e) => setPurpose(e.target.value)}
            placeholder="e.g., Attack roll, Saving throw"
            className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-400"
          />
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">Count</label>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setDiceCount(Math.max(1, diceCount - 1))}
                className="bg-purple-600 hover:bg-purple-700 p-2 rounded-lg transition-colors"
              >
                <Minus className="w-4 h-4 text-white" />
              </button>
              <span className="text-white font-bold text-lg w-8 text-center">{diceCount}</span>
              <button
                onClick={() => setDiceCount(Math.min(10, diceCount + 1))}
                className="bg-purple-600 hover:bg-purple-700 p-2 rounded-lg transition-colors"
              >
                <Plus className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">Die Type</label>
            <select
              value={diceType}
              onChange={(e) => setDiceType(Number(e.target.value))}
              className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-purple-400"
            >
              {diceTypes.map(die => (
                <option key={die} value={die} className="bg-gray-800">d{die}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">Modifier</label>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setModifier(modifier - 1)}
                className="bg-purple-600 hover:bg-purple-700 p-2 rounded-lg transition-colors"
              >
                <Minus className="w-4 h-4 text-white" />
              </button>
              <span className="text-white font-bold text-lg w-8 text-center">{modifier}</span>
              <button
                onClick={() => setModifier(modifier + 1)}
                className="bg-purple-600 hover:bg-purple-700 p-2 rounded-lg transition-colors"
              >
                <Plus className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>
        </div>
        
        <div className="text-center">
          <div className="text-purple-200 mb-4">
            Rolling: <span className="text-yellow-400 font-bold">
              {diceCount}d{diceType}{modifier !== 0 ? (modifier > 0 ? `+${modifier}` : modifier) : ''}
            </span>
          </div>
          
          <button
            onClick={rollDice}
            disabled={isRolling}
            className={`px-8 py-3 rounded-lg font-bold text-white transition-all transform hover:scale-105 ${
              isRolling 
                ? 'bg-gray-600 cursor-not-allowed animate-pulse' 
                : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700'
            }`}
          >
            {isRolling ? 'Rolling...' : 'Roll Dice'}
          </button>
        </div>
      </div>
    </div>
  );
};