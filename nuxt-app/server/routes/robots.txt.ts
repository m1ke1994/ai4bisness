const normalizeBaseUrl = (value: string) => value.replace(/\/+$/, '')

const resolveSiteBaseUrl = (event) => {
  const runtimeConfig = useRuntimeConfig()
  const configuredSiteUrl = String(runtimeConfig.public?.siteUrl || '').trim()
  if (configuredSiteUrl) {
    return normalizeBaseUrl(configuredSiteUrl)
  }

  const forwardedProto = getHeader(event, 'x-forwarded-proto')?.split(',')[0]?.trim()
  const proto = forwardedProto || 'https'
  const host =
    getHeader(event, 'x-forwarded-host')?.split(',')[0]?.trim() ||
    getHeader(event, 'host') ||
    'localhost:3000'

  return `${proto}://${host}`
}

export default defineEventHandler((event) => {
  const siteBaseUrl = resolveSiteBaseUrl(event)
  const robotsText = [
    'User-agent: *',
    'Allow: /',
    'Disallow: /admin/',
    'Disallow: /api/',
    `Sitemap: ${siteBaseUrl}/sitemap.xml`,
  ].join('\n')

  setHeader(event, 'Content-Type', 'text/plain; charset=utf-8')
<<<<<<< HEAD
  setHeader(event, 'Cache-Control', 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400')
=======
>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad
  return robotsText
})
