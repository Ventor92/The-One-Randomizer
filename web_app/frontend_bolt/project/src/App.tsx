import React, { useState } from 'react';
import { Sword, Users, Dices, Crown, Plus, Menu, X } from 'lucide-react';
import { Character, DiceRoll, Campaign } from './types/game';
import { CharacterCreator } from './components/CharacterCreator';
import { CharacterSheet } from './components/CharacterSheet';
import { DiceRoller } from './components/DiceRoller';
import { DiceHistory } from './components/DiceHistory';
import { GameMasterPanel } from './components/GameMasterPanel';

function App() {
  const [activeView, setActiveView] = useState<'dashboard' | 'characters' | 'dice' | 'gm'>('dashboard');
  const [characters, setCharacters] = useState<Character[]>([]);
  const [selectedCharacter, setSelectedCharacter] = useState<Character | null>(null);
  const [showCharacterCreator, setShowCharacterCreator] = useState(false);
  const [diceRolls, setDiceRolls] = useState<DiceRoll[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleCreateCharacter = (character: Character) => {
    setCharacters([...characters, character]);
    setSelectedCharacter(character);
    setShowCharacterCreator(false);
    setActiveView('characters');
  };

  const handleUpdateCharacter = (updatedCharacter: Character) => {
    setCharacters(characters.map(char => 
      char.id === updatedCharacter.id ? updatedCharacter : char
    ));
    setSelectedCharacter(updatedCharacter);
  };

  const handleDiceRoll = (roll: DiceRoll) => {
    setDiceRolls([...diceRolls, roll]);
  };

  const clearDiceHistory = () => {
    setDiceRolls([]);
  };

  const handleCreateCampaign = (campaign: Campaign) => {
    setCampaigns([...campaigns, campaign]);
  };

  const handleUpdateCampaign = (updatedCampaign: Campaign) => {
    setCampaigns(campaigns.map(camp => 
      camp.id === updatedCampaign.id ? updatedCampaign : camp
    ));
  };

  const sidebarItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Sword },
    { id: 'characters', label: 'Characters', icon: Users },
    { id: 'dice', label: 'Dice Roller', icon: Dices },
    { id: 'gm', label: 'Game Master', icon: Crown }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-600 via-slate-900 to-stone-500">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Mobile menu button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 bg-purple-600 hover:bg-purple-700 p-2 rounded-lg text-white"
      >
        {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-40 w-64 bg-black/20 backdrop-blur-sm border-r border-purple-500/30 transform transition-transform duration-300 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0`}>
        <div className="p-6">
          <div className="flex items-center gap-3 mb-8">
            <Sword className="w-8 h-8 text-purple-400" />
            <div>
              <h1 className="text-xl font-bold text-white">New Origin</h1>
              <p className="text-purple-300 text-sm">Original ttRPG System</p>
            </div>
          </div>

          <nav className="space-y-2">
            {sidebarItems.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => {
                  setActiveView(id as any);
                  setSidebarOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  activeView === id
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                    : 'text-purple-200 hover:bg-purple-600/20 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                {label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64 p-4 lg:p-8 relative z-10">
        {/* Dashboard */}
        {activeView === 'dashboard' && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-4xl font-bold text-white mb-4">Welcome to the New Origin</h2>
              <p className="text-purple-200 text-lg">An original tabletop RPG system for epic adventures</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6 hover:scale-105 transition-transform cursor-pointer"
                   onClick={() => setActiveView('characters')}>
                <Users className="w-12 h-12 text-purple-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Characters</h3>
                <p className="text-purple-200 mb-4">Create and manage your heroes</p>
                <div className="text-2xl font-bold text-yellow-400">{characters.length}</div>
              </div>

              <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6 hover:scale-105 transition-transform cursor-pointer"
                   onClick={() => setActiveView('dice')}>
                <Dices className="w-12 h-12 text-purple-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Dice Roller</h3>
                <p className="text-purple-200 mb-4">Roll dice for your adventures</p>
                <div className="text-2xl font-bold text-yellow-400">{diceRolls.length}</div>
              </div>

              <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6 hover:scale-105 transition-transform cursor-pointer"
                   onClick={() => setActiveView('gm')}>
                <Crown className="w-12 h-12 text-yellow-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Campaigns</h3>
                <p className="text-purple-200 mb-4">Manage your game sessions</p>
                <div className="text-2xl font-bold text-yellow-400">{campaigns.length}</div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">Quick Actions</h3>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => setShowCharacterCreator(true)}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-6 py-3 rounded-lg text-white font-semibold transition-all flex items-center gap-2"
                >
                  <Plus className="w-4 h-4" />
                  Create Character
                </button>
                <button
                  onClick={() => setActiveView('dice')}
                  className="bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 px-6 py-3 rounded-lg text-white font-semibold transition-all flex items-center gap-2"
                >
                  <Dices className="w-4 h-4" />
                  Roll Dice
                </button>
              </div>
            </div>

            {/* Game Rules Preview */}
            <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">Game System Overview</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-purple-200 font-semibold mb-2">Core Mechanics</h4>
                  <ul className="text-gray-300 space-y-1">
                    <li>• Six core attributes: STR, DEX, CON, INT, WIS, CHA</li>
                    <li>• d20 + attribute modifier + proficiency for checks</li>
                    <li>• Level-based progression system</li>
                    <li>• Armor Class and Hit Points combat system</li>
                  </ul>
                </div>
                <div>
                  <h4 className="text-purple-200 font-semibold mb-2">Character Classes</h4>
                  <ul className="text-gray-300 space-y-1">
                    <li>• Warrior - Masters of combat</li>
                    <li>• Rogue - Stealth and precision</li>
                    <li>• Mage - Arcane spellcasters</li>
                    <li>• Cleric - Divine magic wielders</li>
                    <li>• Ranger - Wilderness guardians</li>
                    <li>• Bard - Charismatic performers</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Characters */}
        {activeView === 'characters' && (
          <div className="space-y-6">
            {showCharacterCreator ? (
              <CharacterCreator
                onCreateCharacter={handleCreateCharacter}
                onCancel={() => setShowCharacterCreator(false)}
              />
            ) : selectedCharacter ? (
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => setSelectedCharacter(null)}
                    className="text-purple-300 hover:text-white"
                  >
                    ← Back to Characters
                  </button>
                </div>
                <CharacterSheet
                  character={selectedCharacter}
                  onUpdateCharacter={handleUpdateCharacter}
                />
              </div>
            ) : (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-3xl font-bold text-white">Your Characters</h2>
                  <button
                    onClick={() => setShowCharacterCreator(true)}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-6 py-3 rounded-lg text-white font-semibold transition-all flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    Create Character
                  </button>
                </div>

                {characters.length === 0 ? (
                  <div className="text-center py-12">
                    <Users className="w-16 h-16 text-purple-400 mx-auto mb-4 opacity-50" />
                    <p className="text-purple-200 text-lg mb-4">No characters created yet</p>
                    <button
                      onClick={() => setShowCharacterCreator(true)}
                      className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-6 py-3 rounded-lg text-white font-semibold transition-all"
                    >
                      Create Your First Character
                    </button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {characters.map(character => (
                      <div
                        key={character.id}
                        onClick={() => setSelectedCharacter(character)}
                        className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6 hover:scale-105 transition-transform cursor-pointer"
                      >
                        <div className="flex items-center gap-3 mb-4">
                          <Users className="w-8 h-8 text-purple-400" />
                          <div>
                            <h3 className="text-xl font-bold text-white">{character.name}</h3>
                            <p className="text-purple-200">Level {character.level} {character.class.name}</p>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-400">HP:</span>
                            <span className="text-white ml-1">
                              {character.hitPoints.current}/{character.hitPoints.maximum}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-400">AC:</span>
                            <span className="text-white ml-1">{character.armorClass}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">XP:</span>
                            <span className="text-white ml-1">{character.experience}</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Class:</span>
                            <span className="text-white ml-1">{character.class.name}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Dice Roller */}
        {activeView === 'dice' && (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-white">Dice Roller</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <DiceRoller
                onRoll={handleDiceRoll}
                characterName={selectedCharacter?.name}
              />
              <DiceHistory
                rolls={diceRolls}
                onClear={clearDiceHistory}
              />
            </div>
          </div>
        )}

        {/* Game Master */}
        {activeView === 'gm' && (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-white">Game Master Tools</h2>
            <GameMasterPanel
              campaigns={campaigns}
              onCreateCampaign={handleCreateCampaign}
              onUpdateCampaign={handleUpdateCampaign}
            />
          </div>
        )}
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}

export default App;