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

const escapeXml = (value: string) =>
  value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')

export default defineEventHandler((event) => {
  const siteBaseUrl = resolveSiteBaseUrl(event)
<<<<<<< HEAD
=======
  const lastmod = new Date().toISOString()
>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad
  const pages = ['/', '/privacy-policy', '/public-offer', '/user-agreement']

  const urlNodes = pages
    .map((path) => {
      const loc = `${siteBaseUrl}${path}`
      return [
        '<url>',
        `<loc>${escapeXml(loc)}</loc>`,
<<<<<<< HEAD
=======
        `<lastmod>${lastmod}</lastmod>`,
>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad
        '</url>',
      ].join('')
    })
    .join('')

  const sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    urlNodes,
    '</urlset>',
  ].join('')

  setHeader(event, 'Content-Type', 'application/xml; charset=utf-8')
<<<<<<< HEAD
  setHeader(event, 'Cache-Control', 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400')
  return sitemap
})
=======
  return sitemap
})

>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad
