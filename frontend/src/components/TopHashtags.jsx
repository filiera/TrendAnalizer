import { useState, useEffect } from 'react'
import { API_URL } from '../config'

function TopHashtags() {
  const [hashtags, setHashtags] = useState([])
  const [totalPosts, setTotalPosts] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [limit, setLimit] = useState(10)
  const [hours, setHours] = useState(1)

  async function fetchData() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_URL}/hashtags/top?limit=${limit}&hours=${hours}`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setHashtags(data.hashtags)
      setTotalPosts(data.total_posts)
    } catch (e) {
      setError('Failed to load: ' + e.message)
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchData()
  }, [])

  const maxCount = hashtags.length > 0 ? hashtags[0].count : 1

  return (
    <div>
      <h2>Top Hashtags</h2>

      <div className="filters">
        <label>
          Limit:
          <input
            type="number"
            value={limit}
            onChange={e => setLimit(Number(e.target.value))}
            min="1"
            max="100"
            style={{ width: '60px' }}
          />
        </label>
        <label>
          Last (hours):
          <input
            type="number"
            value={hours}
            onChange={e => setHours(Number(e.target.value))}
            min="1"
            max="720"
            style={{ width: '65px' }}
          />
        </label>
        <button onClick={fetchData} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {!loading && hashtags.length === 0 && !error && (
        <p style={{ color: '#888', fontSize: '14px' }}>No data yet.</p>
      )}

      {hashtags.length > 0 && (
        <>
          <p style={{ fontSize: '13px', color: '#666', marginBottom: '10px' }}>
            Total posts in window: {totalPosts}
          </p>
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Hashtag</th>
                <th>Count</th>
                <th style={{ width: '200px' }}>Bar</th>
              </tr>
            </thead>
            <tbody>
              {hashtags.map((item, i) => (
                <tr key={i}>
                  <td>{item.rank}</td>
                  <td>#{item.tag}</td>
                  <td>{item.count}</td>
                  <td>
                    <div style={{
                      width: `${(item.count / maxCount) * 100}%`,
                      minWidth: '4px',
                      height: '12px',
                      background: '#1976d2',
                      borderRadius: '2px'
                    }} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  )
}

export default TopHashtags
