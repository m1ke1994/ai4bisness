export const initTracknodeTracker = () => {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return
  }

  const apiKey = String(import.meta.env.VITE_TRACKNODE_API_KEY || '').trim()
  const src =
    String(import.meta.env.VITE_TRACKNODE_TRACKER_SRC || '').trim() ||
    'https://tracknode.ru/tracker.js'

  if (!apiKey) {
    return
  }

  const scriptId = 'tracknode-tracker'
  if (document.getElementById(scriptId)) {
    return
  }

  const loadTracker = () => {
    if (document.getElementById(scriptId)) {
      return
    }

    const script = document.createElement('script')
    script.id = scriptId
    script.src = src
    script.async = true
    script.defer = true
    script.setAttribute('data-api-key', apiKey)

    document.head.appendChild(script)
  }

  const scheduleLoad = () => {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(loadTracker, { timeout: 2000 })
      return
    }

    window.setTimeout(loadTracker, 1200)
  }

  if (document.readyState === 'complete') {
    scheduleLoad()
    return
  }

  window.addEventListener('load', scheduleLoad, { once: true })
}
