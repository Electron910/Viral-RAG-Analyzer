import React from 'react';
import { Eye, Heart, MessageCircle, Users } from 'lucide-react';

const VideoCard = ({ platform, data }) => {
  if (!data) return null;

  return (
    <div className="video-card">
      <div className="video-thumb">
        {data.thumbnail_url && (
          <img src={data.thumbnail_url} alt="Thumbnail" style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        )}
      </div>
      <div className="video-info">
        <div style={{ textTransform: 'uppercase', fontSize: '0.8rem', color: '#888', marginBottom: '0.5rem' }}>
          {platform} Video
        </div>
        <h3 className="video-title">{data.title}</h3>
        
        <div className="meta-grid">
          <div className="meta-item">
            <Users size={14} /> {data.creator} ({(data.follower_count || 0).toLocaleString()} followers)
          </div>
          <div className="meta-item">
            <Eye size={14} /> {(data.views || 0).toLocaleString()}
          </div>
          <div className="meta-item">
            <Heart size={14} /> {(data.likes || 0).toLocaleString()}
          </div>
          <div className="meta-item">
            <MessageCircle size={14} /> {(data.comments || 0).toLocaleString()}
          </div>
        </div>
        
        <div className="engagement-badge">
          Engagement Rate: {data.engagement_rate}%
        </div>
      </div>
    </div>
  );
};

export default VideoCard;
