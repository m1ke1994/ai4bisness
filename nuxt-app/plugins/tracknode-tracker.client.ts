export default defineNuxtPlugin(() => {
  if (process.server) return

  const cfg = useRuntimeConfig()

  // public: можно отдавать в клиент (это не секрет, это "public key")
  const apiKey = cfg.public.tracknodeApiKey
  const src = cfg.public.tracknodeTrackerSrc || 'https://tracknode.ru/tracker.js'

  if (!apiKey) return

  const SCRIPT_ID = 'tracknode-tracker'
  if (document.getElementById(SCRIPT_ID)) return

  const loadTracker = () => {
    if (document.getElementById(SCRIPT_ID)) return

    const s = document.createElement('script')
    s.id = SCRIPT_ID
    s.src = src
    s.async = true
    s.defer = true
    s.setAttribute('data-api-key', apiKey)

    document.head.appendChild(s)
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
})
