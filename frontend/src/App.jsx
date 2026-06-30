import { useState } from 'react'
import TopHashtags from './components/TopHashtags'
import HashtagSearch from './components/HashtagSearch'
import LiveFeed from './components/LiveFeed'
import { useLiveFeed } from './context/LiveFeedContext'
import { API_URL } from './config'

function App() {
  const [currentTab, setCurrentTab] = useState('top')
  const { running } = useLiveFeed()

  return (
    <div className="container">
      <h1 className="title">Trend Analyzer</h1>
      <p className="subtitle">Mastodon hashtag analytics</p>

      <div className="tabs">
        <button
          className={`tab-btn ${currentTab === 'top' ? 'active' : ''}`}
          onClick={() => setCurrentTab('top')}
        >
          Top Hashtags
        </button>
        <button
          className={`tab-btn ${currentTab === 'search' ? 'active' : ''}`}
          onClick={() => setCurrentTab('search')}
        >
          Search Hashtag
        </button>
        <button
          className={`tab-btn ${currentTab === 'live' ? 'active' : ''}`}
          onClick={() => setCurrentTab('live')}
          style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          Live Feed
          {running && (
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: '#4caf50',
              animation: 'pulse 1.5s infinite'
            }} />
          )}
        </button>
      </div>

      <div className="tab-content">
        {currentTab === 'top' && <TopHashtags />}
        {currentTab === 'search' && <HashtagSearch />}
        {currentTab === 'live' && <LiveFeed />}
      </div>
    </div>
  )
}

export default App
