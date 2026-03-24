const scriptId = 'b24u-script'

export const initB24U = () => {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return
  }

  const existingScript = document.getElementById(scriptId)

  const initWidget = () => {
    const win = window
    if (win.B24U && typeof win.B24U.init === 'function') {
      win.B24U.init()
      return
    }
    console.warn('[B24U] script loaded, but window.B24U.init is unavailable')
  }

  const loadScript = () => {
    if (existingScript) {
      if (window.B24U) {
        initWidget()
      } else {
        existingScript.addEventListener('load', initWidget, { once: true })
      }
      return
    }

    const script = document.createElement('script')
    script.id = scriptId
    script.src = 'https://i.b24u.ru/ai4businesss.com'
    script.defer = true
    script.async = true

    script.onload = initWidget
    script.onerror = () => {
      console.error('[B24U] failed to load script:', script.src)
    }

    document.head.appendChild(script)
  }

  const scheduleLoad = () => {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(loadScript, { timeout: 2500 })
      return
    }

    window.setTimeout(loadScript, 1500)
  }

  if (document.readyState === 'complete') {
    scheduleLoad()
    return
  }

  window.addEventListener('load', scheduleLoad, { once: true })
}
