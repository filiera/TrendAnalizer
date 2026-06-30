import React, { createContext, useContext, useState, useRef, useEffect } from 'react';
import { API_URL } from '../config';

const POLL_INTERVAL = 5000;

const LiveFeedContext = createContext();

export function LiveFeedProvider({ children }) {
  const [hashtag, setHashtag] = useState('');
  const [posts, setPosts] = useState([]);
  const [running, setRunning] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [error, setError] = useState(null);

  const sinceIdRef = useRef(null);
  const tagRef = useRef('');

  async function fetchNew() {
    const tag = tagRef.current;
    if (!tag) return;

    const params = new URLSearchParams({ limit: 20 });
    if (sinceIdRef.current) {
      params.set('since_id', sinceIdRef.current);
    }

    try {
      const res = await fetch(`${API_URL}/hashtags/${tag}/poll?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (data.length > 0) {
        sinceIdRef.current = data[0].id;
        setPosts(prev => [...data, ...prev].slice(0, 100));
      }

      setLastUpdated(new Date());
      setError(null);
    } catch (e) {
      setError(e.message);
    }
  }

  function start(tagToWatch) {
    const cleanedTag = tagToWatch.trim().replace('#', '').toLowerCase();
    if (!cleanedTag) return;
    
    tagRef.current = cleanedTag;
    sinceIdRef.current = null;
    setPosts([]);
    setError(null);
    setRunning(true);
  }

  function stop() {
    setRunning(false);
  }

  useEffect(() => {
    if (!running) return;
    fetchNew();
    const interval = setInterval(fetchNew, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [running]);

  const value = {
    hashtag,
    setHashtag,
    posts,
    running,
    lastUpdated,
    error,
    tag: tagRef.current,
    start,
    stop
  };

  return (
    <LiveFeedContext.Provider value={value}>
      {children}
    </LiveFeedContext.Provider>
  );
}

export function useLiveFeed() {
  return useContext(LiveFeedContext);
}
