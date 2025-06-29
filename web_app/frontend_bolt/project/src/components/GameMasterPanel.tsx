import React, { useState } from 'react';
import { Crown, Users, BookOpen, Scroll, Plus } from 'lucide-react';
import { Campaign, Session } from '../types/game';

interface GameMasterPanelProps {
  campaigns: Campaign[];
  onCreateCampaign: (campaign: Campaign) => void;
  onUpdateCampaign: (campaign: Campaign) => void;
}

export const GameMasterPanel: React.FC<GameMasterPanelProps> = ({ 
  campaigns, 
  onCreateCampaign, 
  onUpdateCampaign 
}) => {
  const [activeTab, setActiveTab] = useState<'campaigns' | 'session' | 'notes'>('campaigns');
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    description: '',
    gameMaster: 'Game Master'
  });

  const createCampaign = () => {
    if (!newCampaign.name.trim()) return;
    
    const campaign: Campaign = {
      id: Date.now().toString(),
      name: newCampaign.name.trim(),
      description: newCampaign.description.trim(),
      gameMaster: newCampaign.gameMaster,
      players: [],
      characters: [],
      sessions: [],
      notes: ''
    };
    
    onCreateCampaign(campaign);
    setNewCampaign({ name: '', description: '', gameMaster: 'Game Master' });
    setShowCreateForm(false);
  };

  const addSession = (campaignId: string) => {
    const campaign = campaigns.find(c => c.id === campaignId);
    if (!campaign) return;

    const newSession: Session = {
      id: Date.now().toString(),
      date: new Date().toISOString().split('T')[0],
      title: `Session ${campaign.sessions.length + 1}`,
      summary: '',
      experience: 0,
      treasure: []
    };

    const updatedCampaign = {
      ...campaign,
      sessions: [...campaign.sessions, newSession]
    };

    onUpdateCampaign(updatedCampaign);
    setSelectedCampaign(updatedCampaign);
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <Crown className="w-6 h-6 text-yellow-400" />
          Game Master Panel
        </h2>
        
        <div className="flex gap-4 mb-6">
          {[
            { id: 'campaigns', label: 'Campaigns', icon: BookOpen },
            { id: 'session', label: 'Session Tools', icon: Users },
            { id: 'notes', label: 'GM Notes', icon: Scroll }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                activeTab === id 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-black/20 text-purple-200 hover:bg-black/40'
              }`}
            >
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>

        {/* Campaigns Tab */}
        {activeTab === 'campaigns' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-white">Your Campaigns</h3>
              <button
                onClick={() => setShowCreateForm(true)}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-4 py-2 rounded-lg text-white font-semibold flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                New Campaign
              </button>
            </div>

            {showCreateForm && (
              <div className="bg-black/20 rounded-lg p-4 border border-purple-500/30">
                <h4 className="text-white font-semibold mb-3">Create New Campaign</h4>
                <div className="space-y-3">
                  <input
                    type="text"
                    placeholder="Campaign Name"
                    value={newCampaign.name}
                    onChange={(e) => setNewCampaign({ ...newCampaign, name: e.target.value })}
                    className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white placeholder-purple-300/50"
                  />
                  <textarea
                    placeholder="Campaign Description"
                    value={newCampaign.description}
                    onChange={(e) => setNewCampaign({ ...newCampaign, description: e.target.value })}
                    className="w-full bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white placeholder-purple-300/50 h-20 resize-none"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={createCampaign}
                      className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-white font-semibold"
                    >
                      Create
                    </button>
                    <button
                      onClick={() => setShowCreateForm(false)}
                      className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded text-white"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}

            <div className="grid gap-4">
              {campaigns.map(campaign => (
                <div key={campaign.id} className="bg-black/20 rounded-lg p-4 border border-purple-500/20">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="text-white font-semibold text-lg">{campaign.name}</h4>
                      <p className="text-purple-200 text-sm mb-2">{campaign.description}</p>
                      <div className="text-sm text-gray-400">
                        Sessions: {campaign.sessions.length} | Players: {campaign.players.length}
                      </div>
                    </div>
                    <button
                      onClick={() => setSelectedCampaign(campaign)}
                      className="bg-purple-600 hover:bg-purple-700 px-3 py-1 rounded text-white text-sm"
                    >
                      Manage
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Session Tools Tab */}
        {activeTab === 'session' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Session Management</h3>
            
            {selectedCampaign ? (
              <div className="space-y-4">
                <div className="bg-black/20 rounded-lg p-4">
                  <h4 className="text-white font-semibold mb-2">Current Campaign: {selectedCampaign.name}</h4>
                  <button
                    onClick={() => addSession(selectedCampaign.id)}
                    className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-white font-semibold flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    Add Session
                  </button>
                </div>

                <div className="space-y-2">
                  <h5 className="text-purple-200 font-semibold">Recent Sessions</h5>
                  {selectedCampaign.sessions.slice(-5).map(session => (
                    <div key={session.id} className="bg-black/20 rounded-lg p-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="text-white font-medium">{session.title}</span>
                          <span className="text-gray-400 text-sm ml-2">{session.date}</span>
                        </div>
                        <span className="text-yellow-400">{session.experience} XP</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center text-purple-300 py-8">
                <Users className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>Select a campaign to manage sessions</p>
              </div>
            )}
          </div>
        )}

        {/* GM Notes Tab */}
        {activeTab === 'notes' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Game Master Notes</h3>
            <div className="bg-black/20 rounded-lg p-4">
              <textarea
                placeholder="Keep track of plot hooks, NPC notes, world details, and more..."
                className="w-full h-64 bg-black/30 border border-purple-500/50 rounded-lg px-3 py-2 text-white placeholder-purple-300/50 resize-none"
              />
              <button className="mt-3 bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-white font-semibold">
                Save Notes
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};