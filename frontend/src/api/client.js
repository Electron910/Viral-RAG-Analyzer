import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ingestVideos = async (videos) => {
  const response = await axios.post(`${API_URL}/ingest`, {
    videos: videos,
  });
  return response.data;
};

// We will use native EventSource for streaming, so we don't necessarily need a wrapper here for chat,
// but fetch API is better for POST with bodies for SSE.
export const chatStream = async (sessionId, message, onToken, onCitation, onError, onDone) => {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split(/\r?\n\r?\n/);
      buffer = lines.pop() || ''; // Keep the last incomplete part

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === 'token') {
              onToken(data.content);
            } else if (data.type === 'citation') {
              onCitation(data);
            } else if (data.type === 'error') {
              console.error("Backend error:", data.content);
              onError(data.content);
            } else if (data.type === 'done') {
              onDone();
            }
          } catch (e) {
            console.error('Parse error on line:', line, e);
          }
        }
      }
    }
  } catch (err) {
    onError(err.message);
  }
};
