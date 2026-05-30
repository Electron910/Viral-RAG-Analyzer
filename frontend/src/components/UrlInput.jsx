import React, { useState } from 'react';
import { Play } from 'lucide-react';

const UrlInput = ({ onIngest, loading }) => {
  const [mode, setMode] = useState('yt-ig');
  const [url1, setUrl1] = useState('');
  const [url2, setUrl2] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url1 && url2) {
      const p1 = mode.startsWith('yt') ? 'youtube' : 'instagram';
      const p2 = mode.endsWith('ig') ? 'instagram' : 'youtube';
      onIngest([{ platform: p1, url: url1 }, { platform: p2, url: url2 }]);
    }
  };

  const p1Label = mode.startsWith('yt') ? 'YouTube Video URL 1' : 'Instagram Reel URL 1';
  const p2Label = mode.endsWith('ig') ? 'Instagram Reel URL 2' : 'YouTube Video URL 2';

  return (
    <div className="url-input-container">
      <div className="mode-selector" style={{ marginBottom: '1rem', display: 'flex', gap: '1rem' }}>
        <label>
          <input type="radio" value="yt-ig" checked={mode === 'yt-ig'} onChange={(e) => setMode(e.target.value)} /> YouTube vs Instagram
        </label>
        <label>
          <input type="radio" value="yt-yt" checked={mode === 'yt-yt'} onChange={(e) => setMode(e.target.value)} /> YouTube vs YouTube
        </label>
        <label>
          <input type="radio" value="ig-ig" checked={mode === 'ig-ig'} onChange={(e) => setMode(e.target.value)} /> Instagram vs Instagram
        </label>
      </div>
      <form className="url-input-form" onSubmit={handleSubmit}>
        <input 
          type="url" 
          placeholder={p1Label} 
          value={url1} 
          onChange={e => setUrl1(e.target.value)}
          required 
        />
        <input 
          type="url" 
          placeholder={p2Label} 
          value={url2} 
          onChange={e => setUrl2(e.target.value)}
          required 
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : <><Play size={16} /> Analyze</>}
        </button>
      </form>
    </div>
  );
};

export default UrlInput;
