type HeaderApiMenuItem = {
  title?: string
  href?: string
}

type HeaderApiResponse = {
  brand_name?: string
  logo?: string | null
  logo_link?: string
  menu_items?: HeaderApiMenuItem[]
}

export type HeaderSectionData = {
  brandName: string
  logo: string
  logoLink: string
  menuItems: Array<{
    label: string
    href: string
  }>
}

type FooterApiLinkItem = {
  title?: string
  href?: string
}

type FooterApiResponse = {
  brand_name?: string
  logo?: string | null
  logo_link?: string
  links?: FooterApiLinkItem[]
}

export type FooterSectionData = {
  brandName: string
  logo: string
  logoLink: string
  links: Array<{
    id: string
    label: string
    href: string
  }>
}

const normalizeBaseUrl = (value: string) => value.replace(/\/+$/, '')

const getBackendBaseUrl = () => {
  if (import.meta.client && typeof window !== 'undefined') {
    return `${window.location.protocol}//${window.location.hostname}:8000`
  }

  return 'http://backend:8000'
}

const normalizeMediaUrl = (value: string | null | undefined, baseUrl: string) => {
  if (!value) return ''
  if (/^https?:\/\//i.test(value)) return value
  if (value.startsWith('/')) return `${baseUrl}${value}`
  return `${baseUrl}/${value}`
}

export const fetchHeaderSection = async (): Promise<HeaderSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<HeaderApiResponse>('/api/header/', {
      baseURL: baseUrl,
    })

    const menuItems = Array.isArray(payload?.menu_items)
      ? payload.menu_items
          .map((item) => ({
            label: (item?.title || '').trim(),
            href: (item?.href || '').trim(),
          }))
          .filter((item) => Boolean(item.label && item.href))
      : []

    return {
      brandName: (payload?.brand_name || '').trim(),
      logo: normalizeMediaUrl(payload?.logo, baseUrl),
      logoLink: (payload?.logo_link || '/').trim() || '/',
      menuItems,
    }
  } catch {
    return null
  }
}

export const fetchFooterSection = async (): Promise<FooterSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<FooterApiResponse>('/api/footer/', {
      baseURL: baseUrl,
    })

    const links = Array.isArray(payload?.links)
      ? payload.links
          .map((item, index) => ({
            id: `footer-link-${index + 1}`,
            label: (item?.title || '').trim(),
            href: (item?.href || '').trim(),
          }))
          .filter((item) => Boolean(item.label && item.href))
      : []

    return {
      brandName: (payload?.brand_name || '').trim(),
      logo: normalizeMediaUrl(payload?.logo, baseUrl),
      logoLink: (payload?.logo_link || '/').trim() || '/',
      links,
    }
  } catch {
    return null
  }
}
