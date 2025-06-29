import React from 'react';
import { DiceRoll } from '../types/game';
import { Clock, Dices } from 'lucide-react';

interface DiceHistoryProps {
  rolls: DiceRoll[];
  onClear: () => void;
}

export const DiceHistory: React.FC<DiceHistoryProps> = ({ rolls, onClear }) => {
  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Clock className="w-5 h-5 text-purple-400" />
          Roll History
        </h3>
        <button
          onClick={onClear}
          className="text-purple-300 hover:text-white text-sm transition-colors"
        >
          Clear All
        </button>
      </div>
      
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {rolls.length === 0 ? (
          <div className="text-center text-purple-300 py-8">
            <Dices className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No rolls yet. Start rolling some dice!</p>
          </div>
        ) : (
          rolls.slice().reverse().map((roll) => (
            <div key={roll.id} className="bg-black/20 rounded-lg p-3 border border-purple-500/20">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="text-yellow-400 font-bold text-lg">
                    {roll.result}
                  </div>
                  <div className="text-purple-200">
                    {roll.dice}
                  </div>
                  {roll.purpose && (
                    <div className="text-sm text-gray-400">
                      ({roll.purpose})
                    </div>
                  )}
                </div>
                <div className="text-right text-sm text-gray-400">
                  {roll.character && <div>{roll.character}</div>}
                  <div>{formatTime(roll.timestamp)}</div>
                </div>
              </div>
              
              {roll.breakdown.length > 1 && (
                <div className="mt-2 text-sm text-purple-300">
                  Individual: [{roll.breakdown.join(', ')}]
                  {roll.modifier !== 0 && (
                    <span> {roll.modifier > 0 ? '+' : ''}{roll.modifier}</span>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};