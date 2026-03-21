export default defineNuxtPlugin(() => {
  if (import.meta.server) return

  const scriptId = 'b24u-script'

  const existingScript = document.getElementById(scriptId) as HTMLScriptElement | null

  const initB24U = () => {
    const win = window as typeof window & {
      B24U?: {
        init?: () => void
      }
    }

    if (win.B24U && typeof win.B24U.init === 'function') {
      win.B24U.init()
      console.log('[B24U] init() called')
    } else {
      console.warn('[B24U] script loaded, but window.B24U.init is unavailable')
    }
  }

  if (existingScript) {
    if ((window as any).B24U) {
      initB24U()
    } else {
      existingScript.addEventListener('load', initB24U, { once: true })
    }
    return
  }

  const script = document.createElement('script')
  script.id = scriptId
  script.src = 'https://i.b24u.ru/ai4businesss.com'
  script.defer = true
  script.async = false

  script.onload = () => {
    initB24U()
  }

  script.onerror = () => {
    console.error('[B24U] failed to load script:', script.src)
  }

  document.head.appendChild(script)
})