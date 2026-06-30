import { useLiveFeed } from '../context/LiveFeedContext'

function LiveFeed() {
  const {
    hashtag,
    setHashtag,
    posts,
    running,
    lastUpdated,
    error,
    tag,
    start,
    stop
  } = useLiveFeed()

  function handleStart() {
    if (!hashtag.trim() || running) return
    start(hashtag)
  }

  return (
    <div>
      <h2>Live Feed</h2>
      <p style={{ fontSize: '13px', color: '#888', marginBottom: '14px' }}>
        Polls Mastodon every 5 seconds for new posts with the given hashtag.
      </p>

      <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '16px' }}>
        <input
          type="text"
          className="hashtag-input"
          placeholder="Enter hashtag (without #)"
          value={hashtag}
          onChange={e => setHashtag(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !running && handleStart()}
          disabled={running}
        />
        {!running ? (
          <button onClick={handleStart} disabled={!hashtag.trim()}>Start</button>
        ) : (
          <button onClick={stop} style={{ background: '#c62828' }}>Stop</button>
        )}
      </div>

      {running && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <span style={{
            width: '8px', height: '8px', borderRadius: '50%',
            background: '#4caf50', display: 'inline-block',
            animation: 'pulse 1.5s infinite'
          }} />
          <span style={{ fontSize: '13px', color: '#2e7d32' }}>
            Watching #{tag}
          </span>
          {lastUpdated && (
            <span style={{ fontSize: '12px', color: '#aaa' }}>
              &middot; updated {lastUpdated.toLocaleTimeString('pl-PL')}
            </span>
          )}
          {posts.length > 0 && (
            <span style={{ fontSize: '12px', color: '#aaa' }}>
              &middot; {posts.length} posts
            </span>
          )}
        </div>
      )}

      {error && <p className="error">Error: {error}</p>}

      {running && posts.length === 0 && !error && (
        <p style={{ fontSize: '14px', color: '#aaa' }}>No posts yet...</p>
      )}

      {posts.map((post, i) => (
        <div key={post.id || i} className="post-card" style={{ borderLeft: '3px solid #4caf50' }}>
          <div className="post-header">
            <span className="post-account">@{post.account}</span>
            <span style={{ fontSize: '12px', color: '#aaa' }}>
              {new Date(post.created_at).toLocaleTimeString('pl-PL')}
            </span>
          </div>
          <p className="post-content">
            {post.content.length > 400 ? post.content.slice(0, 400) + '...' : post.content}
          </p>
          <div className="post-stats">
            {post.url && (
              <a href={post.url} target="_blank" rel="noreferrer">View post</a>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

export default LiveFeed
