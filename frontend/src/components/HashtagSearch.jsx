import { useState } from 'react'
import { API_URL } from '../config'

function HashtagSearch() {
  const [hashtag, setHashtag] = useState('')
  const [view, setView] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [historyData, setHistoryData] = useState(null)
  const [sentimentData, setSentimentData] = useState(null)
  const [popularData, setPopularData] = useState(null)
  const [correlatedData, setCorrelatedData] = useState(null)
  const [languageData, setLanguageData] = useState(null)

  const [buckets, setBuckets] = useState(6)
  const [bucketMinutes, setBucketMinutes] = useState(60)

  const [sentimentHours, setSentimentHours] = useState(24)

  const [popularHours, setPopularHours] = useState(1)
  const [popularLimit, setPopularLimit] = useState(5)

  const [correlatedHours, setCorrelatedHours] = useState(24)
  const [correlatedLimit, setCorrelatedLimit] = useState(5)

  const [languageHours, setLanguageHours] = useState(24)

  async function fetchHistory() {
    if (!hashtag.trim()) return
    setLoading(true)
    setError(null)
    setView('history')
    try {
      const res = await fetch(
        `${API_URL}/hashtags/${hashtag.trim()}/history?buckets=${buckets}&bucket_minutes=${bucketMinutes}`
      )
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setHistoryData(data)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  async function fetchSentiment() {
    if (!hashtag.trim()) return
    setLoading(true)
    setError(null)
    setView('sentiment')
    try {
      const res = await fetch(
        `${API_URL}/hashtags/${hashtag.trim()}/sentiment?hours=${sentimentHours}`
      )
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setSentimentData(data)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  async function fetchPopular() {
    if (!hashtag.trim()) return
    setLoading(true)
    setError(null)
    setView('popular')
    try {
      const res = await fetch(
        `${API_URL}/hashtags/${hashtag.trim()}/popular?hours=${popularHours}&limit=${popularLimit}`
      )
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setPopularData(data)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  async function fetchCorrelated() {
    if (!hashtag.trim()) return
    setLoading(true)
    setError(null)
    setView('correlated')
    try {
      const res = await fetch(
        `${API_URL}/hashtags/${hashtag.trim()}/correlated?hours=${correlatedHours}&limit=${correlatedLimit}`
      )
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setCorrelatedData(data)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  async function fetchLanguages() {
    if (!hashtag.trim()) return
    setLoading(true)
    setError(null)
    setView('languages')
    try {
      const res = await fetch(
        `${API_URL}/hashtags/${hashtag.trim()}/languages?hours=${languageHours}`
      )
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setLanguageData(data)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') fetchHistory()
  }

  const maxBarCount =
    historyData && historyData.data.length > 0
      ? Math.max(...historyData.data.map(b => b.count), 1)
      : 1

  return (
    <div>
      <h2>Search Hashtag</h2>

      <div className="search-bar">
        <input
          type="text"
          className="hashtag-input"
          placeholder="Enter hashtag (without #)"
          value={hashtag}
          onChange={e => setHashtag(e.target.value.toLowerCase())}
          onKeyDown={handleKeyDown}
        />
        <span style={{ fontSize: '12px', color: '#aaa', marginLeft: '8px' }}>
          press Enter for history
        </span>
      </div>

      <div className="action-buttons">
        <div className="action-group">
          <h4>History</h4>
          <div className="action-params">
            <label>
              Buckets
              <input
                type="number"
                value={buckets}
                onChange={e => setBuckets(Number(e.target.value))}
                min="2"
                max="48"
              />
            </label>
            <label>
              Min/bucket
              <input
                type="number"
                value={bucketMinutes}
                onChange={e => setBucketMinutes(Number(e.target.value))}
                min="1"
                max="1440"
              />
            </label>
          </div>
          <button onClick={fetchHistory} disabled={!hashtag.trim() || loading}>
            Show History
          </button>
        </div>

        <div className="action-group">
          <h4>Sentiment</h4>
          <div className="action-params">
            <label>
              Hours
              <input
                type="number"
                value={sentimentHours}
                onChange={e => setSentimentHours(Number(e.target.value))}
                min="1"
                max="720"
              />
            </label>
          </div>
          <button onClick={fetchSentiment} disabled={!hashtag.trim() || loading}>
            Show Sentiment
          </button>
        </div>

        <div className="action-group">
          <h4>Popular Posts</h4>
          <div className="action-params">
            <label>
              Hours
              <input
                type="number"
                value={popularHours}
                onChange={e => setPopularHours(Number(e.target.value))}
                min="1"
                max="168"
              />
            </label>
            <label>
              Limit
              <input
                type="number"
                value={popularLimit}
                onChange={e => setPopularLimit(Number(e.target.value))}
                min="1"
                max="50"
              />
            </label>
          </div>
          <button onClick={fetchPopular} disabled={!hashtag.trim() || loading}>
            Show Posts
          </button>
        </div>

        <div className="action-group">
          <h4>Correlated</h4>
          <div className="action-params">
            <label>
              Hours
              <input
                type="number"
                value={correlatedHours}
                onChange={e => setCorrelatedHours(Number(e.target.value))}
                min="1"
                max="720"
              />
            </label>
            <label>
              Limit
              <input
                type="number"
                value={correlatedLimit}
                onChange={e => setCorrelatedLimit(Number(e.target.value))}
                min="1"
                max="50"
              />
            </label>
          </div>
          <button onClick={fetchCorrelated} disabled={!hashtag.trim() || loading}>
            Show Correlated
          </button>
        </div>

        <div className="action-group">
          <h4>Languages</h4>
          <div className="action-params">
            <label>
              Hours
              <input
                type="number"
                value={languageHours}
                onChange={e => setLanguageHours(Number(e.target.value))}
                min="1"
                max="720"
              />
            </label>
          </div>
          <button onClick={fetchLanguages} disabled={!hashtag.trim() || loading}>
            Show Languages
          </button>
        </div>
      </div>

      {loading && <p style={{ fontSize: '14px', color: '#888' }}>Loading...</p>}
      {error && <p className="error">Error: {error}</p>}

      {/* history */}
      {view === 'history' && historyData && !loading && (
        <div className="result-section">
          <h3>History: #{historyData.tag}</h3>
          <p>
            {historyData.buckets} buckets &times; {historyData.bucket_minutes} min
          </p>

          <div className="chart-wrapper">
            <div className="bar-chart">
              {historyData.data.map((bucket, i) => (
                <div key={i} className="bar-col">
                  <span className="bar-value">{bucket.count}</span>
                  <div
                    className="bar"
                    style={{
                      height: `${Math.max((bucket.count / maxBarCount) * 130, bucket.count > 0 ? 3 : 0)}px`
                    }}
                  />
                </div>
              ))}
            </div>
            <div className="bar-labels">
              {historyData.data.map((bucket, i) => (
                <span key={i} className="bar-time">
                  {new Date(bucket.from_time).toLocaleTimeString('pl-PL', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* sentiment */}
      {view === 'sentiment' && sentimentData && !loading && (
        <div className="result-section">
          <h3>Sentiment: #{sentimentData.tag}</h3>
          <p>Last {sentimentData.period_hours} hours</p>

          <div className="sentiment-bars">
            <div className="sentiment-row">
              <span className="sentiment-label">Positive</span>
              <div className="sentiment-track">
                <div
                  className="sentiment-fill"
                  style={{
                    width: `${(sentimentData.positive * 100).toFixed(0)}%`,
                    background: '#4caf50'
                  }}
                />
              </div>
              <span className="sentiment-pct">
                {(sentimentData.positive * 100).toFixed(1)}%
              </span>
            </div>
            <div className="sentiment-row">
              <span className="sentiment-label">Neutral</span>
              <div className="sentiment-track">
                <div
                  className="sentiment-fill"
                  style={{
                    width: `${(sentimentData.neutral * 100).toFixed(0)}%`,
                    background: '#9e9e9e'
                  }}
                />
              </div>
              <span className="sentiment-pct">
                {(sentimentData.neutral * 100).toFixed(1)}%
              </span>
            </div>
            <div className="sentiment-row">
              <span className="sentiment-label">Negative</span>
              <div className="sentiment-track">
                <div
                  className="sentiment-fill"
                  style={{
                    width: `${(sentimentData.negative * 100).toFixed(0)}%`,
                    background: '#f44336'
                  }}
                />
              </div>
              <span className="sentiment-pct">
                {(sentimentData.negative * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      )}

      {/* popular posts */}
      {view === 'popular' && popularData && !loading && (
        <div className="result-section">
          <h3>Popular Posts: #{popularData.tag}</h3>
          <p>
            Last {popularData.period_hours}h, top {popularData.limit} posts
          </p>

          {popularData.posts.length === 0 && (
            <p style={{ color: '#888', fontSize: '14px', marginTop: '8px' }}>
              No posts found.
            </p>
          )}

          {popularData.posts.map(post => (
            <div key={post.id} className="post-card">
              <div className="post-header">
                <span className="post-account">@{post.account}</span>
                <span className="post-score: {post.score}">score: {post.score}</span>
              </div>
              <p className="post-content">
                {post.content.length > 300
                  ? post.content.slice(0, 300) + '...'
                  : post.content}
              </p>
              <div className="post-stats">
                <span>Fav: {post.favourites_count}</span>
                <span>Reblogs: {post.reblogs_count}</span>
                <span>Replies: {post.replies_count}</span>
                {post.url && (
                  <a href={post.url} target="_blank" rel="noreferrer">
                    View post
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* correlated hashtags */}
      {view === 'correlated' && correlatedData && !loading && (
        <div className="result-section">
          <h3>Correlated Hashtags for: #{correlatedData.tag}</h3>
          <p>Top {correlatedLimit} hashtags appearing together in the last {correlatedHours}h</p>
          
          {correlatedData.correlated_hashtags.length === 0 && (
            <p style={{ color: '#888', fontSize: '14px', marginTop: '8px' }}>
              No correlated hashtags found.
            </p>
          )}

          <ul style={{ listStyle: 'none', padding: 0 }}>
            {correlatedData.correlated_hashtags.map((item, idx) => (
              <li key={idx} style={{ 
                padding: '10px', 
                background: '#f9f9f9', 
                marginBottom: '5px', 
                borderRadius: '4px',
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '14px'
              }}>
                <span style={{ fontWeight: 'bold', color: '#1976d2' }}>#{item.tag}</span>
                <span style={{ color: '#666' }}>{item.count} occurrences</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* languages */}
      {view === 'languages' && languageData && !loading && (
        <div className="result-section">
          <h3>Language Statistics: #{languageData.tag}</h3>
          <p>Distribution in the last {languageHours}h</p>
          
          {languageData.languages.length === 0 && (
            <p style={{ color: '#888', fontSize: '14px', marginTop: '8px' }}>
              No language data found.
            </p>
          )}

          <div className="sentiment-bars">
            {languageData.languages.map((item, idx) => (
              <div key={idx} className="sentiment-row">
                <span className="sentiment-label" style={{ textTransform: 'uppercase' }}>{item.language}</span>
                <div className="sentiment-track">
                  <div
                    className="sentiment-fill"
                    style={{
                      width: `${(item.percentage * 100).toFixed(0)}%`,
                      background: '#1976d2'
                    }}
                  />
                </div>
                <span className="sentiment-pct">
                  {(item.percentage * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default HashtagSearch
