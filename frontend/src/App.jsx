import React, { useState } from 'react';
import UrlInput from './components/UrlInput';
import VideoCard from './components/VideoCard';
import ChatPanel from './components/ChatPanel';
import { ingestVideos, chatStream } from './api/client';
import './App.css';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [videoData1, setVideoData1] = useState(null);
  const [videoData2, setVideoData2] = useState(null);
  const [platform1, setPlatform1] = useState('');
  const [platform2, setPlatform2] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [chatting, setChatting] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleIngest = async (videos) => {
    setIngesting(true);
    setPlatform1(videos[0].platform === 'youtube' ? 'YouTube' : 'Instagram Reel');
    setPlatform2(videos[1].platform === 'youtube' ? 'YouTube' : 'Instagram Reel');
    
    try {
      const data = await ingestVideos(videos);
      setSessionId(data.session_id);
      setVideoData1(data.metadata_list[0]);
      setVideoData2(data.metadata_list[1]);
      setMessages([{ role: 'assistant', content: 'Videos ingested successfully! Ask me anything.' }]);
    } catch (err) {
      console.error(err);
      alert('Failed to analyze videos. Check console for details.');
    } finally {
      setIngesting(false);
    }
  };

  const handleSendMessage = async (text) => {
    if (!sessionId) return;
    
    setChatting(true);
    const newMessages = [...messages, { role: 'user', content: text }];
    setMessages(newMessages);
    
    let assistantMsg = { role: 'assistant', content: '', citations: [] };
    setMessages([...newMessages, assistantMsg]);

    const onToken = (token) => {
      assistantMsg.content += token;
      setMessages(msgs => {
        const updated = [...msgs];
        updated[updated.length - 1] = { ...assistantMsg };
        return updated;
      });
    };

    const onCitation = (citation) => {
      assistantMsg.citations.push(citation);
      setMessages(msgs => {
        const updated = [...msgs];
        updated[updated.length - 1] = { ...assistantMsg };
        return updated;
      });
    };

    const onError = (err) => {
      console.error(err);
      setChatting(false);
    };

    const onDone = () => {
      setChatting(false);
    };

    await chatStream(sessionId, text, onToken, onCitation, onError, onDone);
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1 style={{ margin: '0 0 1rem 0' }}>Viral RAG Chatbot</h1>
        <UrlInput onIngest={handleIngest} loading={ingesting} />
      </div>
      
      <div className="main-content">
        <div className="videos-section">
          {videoData1 && <VideoCard platform={platform1} data={videoData1} />}
          {videoData2 && <VideoCard platform={platform2} data={videoData2} />}
          {!videoData1 && !videoData2 && !ingesting && (
            <div style={{ color: '#888', textAlign: 'center', marginTop: '2rem' }}>
              Select comparison mode and enter URLs above to analyze videos
            </div>
          )}
        </div>
        
        <ChatPanel 
          messages={messages} 
          onSendMessage={handleSendMessage} 
          loading={chatting} 
          platform1={platform1}
          platform2={platform2}
        />
      </div>
    </div>
  );
}

export default App;
