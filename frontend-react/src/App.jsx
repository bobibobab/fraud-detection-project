import { useState } from 'react'
import './App.css'

const CATEGORIES = [
  { value: 'food',          label: '🍔 Food & Dining' },
  { value: 'shopping',      label: '🛍️ Shopping' },
  { value: 'travel',        label: '✈️ Travel' },
  { value: 'entertainment', label: '🎬 Entertainment' },
  { value: 'medical',       label: '🏥 Medical' },
  { value: 'other',         label: '📦 Other' },
]

function App() {
  const [form, setForm] = useState({
    amount: '',
    merchant_name: '',
    merchant_category: 'food',
    is_overseas: false,
    is_new_merchant: false,
    transaction_time: '14:00',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setForm(f => ({ ...f, [name]: type === 'checkbox' ? checked : value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.amount || isNaN(form.amount)) return
    setLoading(true)
    setResult(null)
    setError(null)
    try {
      const res = await fetch('http://127.0.0.1:8000/payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: parseFloat(form.amount),
          merchant_category: form.merchant_category,
          is_overseas: form.is_overseas,
          is_new_merchant: form.is_new_merchant,
          transaction_time: form.transaction_time,
        }),
      })
      if (!res.ok) throw new Error('Server error')
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError('Failed to connect to server. Make sure uvicorn is running.')
    } finally {
      setLoading(false)
    }
  }

  const riskPercent = result ? (result.risk_score * 100).toFixed(1) : 0
  const isApproved = result?.decision === 'approve'

  return (
    <div className="page">
      <div className="card">
        <h1 className="title">💳 Fraud Detection</h1>
        <p className="subtitle">Enter your payment details to check for fraud</p>

        <form onSubmit={handleSubmit} className="form">

          {/* Amount */}
          <div className="field">
            <label>Amount ($)</label>
            <input
              type="number"
              name="amount"
              value={form.amount}
              onChange={handleChange}
              placeholder="e.g. 150.00"
              min="0"
              step="0.01"
              required
            />
          </div>

          {/* Merchant Name */}
          <div className="field">
            <label>Merchant Name</label>
            <input
              type="text"
              name="merchant_name"
              value={form.merchant_name}
              onChange={handleChange}
              placeholder="e.g. Amazon, Starbucks"
            />
          </div>

          {/* Category */}
          <div className="field">
            <label>Merchant Category</label>
            <select name="merchant_category" value={form.merchant_category} onChange={handleChange}>
              {CATEGORIES.map(c => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>
          </div>

          {/* Time */}
          <div className="field">
            <label>Transaction Time</label>
            <input
              type="time"
              name="transaction_time"
              value={form.transaction_time}
              onChange={handleChange}
            />
          </div>

          {/* Toggles */}
          <div className="toggles">
            <label className="toggle">
              <input
                type="checkbox"
                name="is_overseas"
                checked={form.is_overseas}
                onChange={handleChange}
              />
              <span className="toggle-track" />
              <span>Overseas Transaction</span>
            </label>
            <label className="toggle">
              <input
                type="checkbox"
                name="is_new_merchant"
                checked={form.is_new_merchant}
                onChange={handleChange}
              />
              <span className="toggle-track" />
              <span>New / Unknown Merchant</span>
            </label>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Analyzing...' : 'Check Payment'}
          </button>
        </form>

        {/* Error */}
        {error && <div className="error-box">{error}</div>}

        {/* Result */}
        {result && (
          <div className={`result-box ${isApproved ? 'approve' : 'reject'}`}>
            <div className="result-icon">{isApproved ? '✅' : '🚨'}</div>
            <div className="result-status">
              {isApproved ? 'Payment Approved' : 'Payment Rejected'}
            </div>
            <div className="risk-bar-wrap">
              <div className="risk-bar-bg">
                <div
                  className="risk-bar-fill"
                  style={{ width: `${riskPercent}%`, background: isApproved ? '#10b981' : '#ef4444' }}
                />
              </div>
              <span className="risk-label">Risk Score: {riskPercent}%</span>
            </div>
            <div className="result-meta">
              <span>Merchant: <b>{form.merchant_name || '—'}</b></span>
              <span>Amount: <b>${parseFloat(form.amount).toFixed(2)}</b></span>
              <span>Time: <b>{form.transaction_time}</b></span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
