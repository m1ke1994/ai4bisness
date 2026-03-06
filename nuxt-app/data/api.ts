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

type HeroApiItem = {
  value?: string
  text?: string
}

type HeroApiResponse = {
  title?: string
  subtitle?: string
  description?: string
  image?: string | null
  stats_disclaimer?: string
  items?: HeroApiItem[]
}

export type HeroSectionData = {
  title: string
  subtitle: string
  description: string
  image: string
  statsDisclaimer: string
  items: Array<{
    value: string
    text: string
  }>
}

type ReviewsApiActions = {
  readMore?: string
  prevPageAria?: string
  nextPageAria?: string
  paginationAria?: string
  paginationGoTo?: string
  closeModalAria?: string
}

type ReviewsApiItem = {
  id?: number | string
  company?: string
  person?: string
  preview_text?: string
  preview_bullets?: unknown
  details_text?: string
  results?: unknown
}

type ReviewsApiResponse = {
  title?: string
  subtitle?: string
  meta?: {
    modal_results_title?: string
    actions?: ReviewsApiActions
  }
  items?: ReviewsApiItem[]
}

export type ReviewsSectionData = {
  title: string
  subtitle: string
  meta: {
    modalResultsTitle: string
    actions: ReviewsApiActions
  }
  items: Array<{
    id: string
    company: string
    person: string
    previewText: string
    previewBullets: string[]
    detailsText: string
    results: string[]
  }>
}

type ChannelsApiItem = {
  name?: string
  href?: string
  icon?: {
    src?: string | null
    alt?: string
  }
}

type ChannelsApiResponse = {
  title?: string
  subtitle?: string
  description?: string
  meta?: {
    itemAriaLabelPrefix?: string
  }
  media?: {
    background?: string | null
    image?: string | null
    secondaryImage?: string | null
  }
  items?: ChannelsApiItem[]
}

export type ChannelsSectionData = {
  title: string
  subtitle: string
  description: string
  meta: {
    itemAriaLabelPrefix: string
  }
  media: {
    background: {
      src: string
      alt: string
    }
    image: {
      src: string
      alt: string
    }
    secondaryImage: {
      src: string
      alt: string
    }
  }
  items: Array<{
    id: string
    name: string
    href: string
    icon: {
      src: string
      alt: string
    }
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

const normalizeTextList = (value: unknown): string[] => {
  if (!Array.isArray(value)) return []

  return value
    .map((item) => {
      if (typeof item === 'string') return item.trim()
      if (item && typeof item === 'object') {
        const text = (item as { text?: unknown }).text
        if (typeof text === 'string') return text.trim()
      }
      return ''
    })
    .filter(Boolean)
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

export const fetchHeroSection = async (): Promise<HeroSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<HeroApiResponse>('/api/hero/', {
      baseURL: baseUrl,
    })

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item) => ({
            value: (item?.value || '').trim(),
            text: (item?.text || '').trim(),
          }))
          .filter((item) => Boolean(item.value || item.text))
      : []

    return {
      title: (payload?.title || '').trim(),
      subtitle: (payload?.subtitle || '').trim(),
      description: (payload?.description || '').trim(),
      image: normalizeMediaUrl(payload?.image, baseUrl),
      statsDisclaimer: (payload?.stats_disclaimer || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchReviewsSection = async (): Promise<ReviewsSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<ReviewsApiResponse>('/api/reviews/', {
      baseURL: baseUrl,
    })

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: String(item?.id ?? `review-${index + 1}`),
            company: (item?.company || '').trim(),
            person: (item?.person || '').trim(),
            previewText: (item?.preview_text || '').trim(),
            previewBullets: normalizeTextList(item?.preview_bullets),
            detailsText: (item?.details_text || '').trim(),
            results: normalizeTextList(item?.results),
          }))
          .filter(
            (item) =>
              Boolean(item.company || item.person || item.previewText || item.detailsText) ||
              item.previewBullets.length > 0 ||
              item.results.length > 0,
          )
      : []

    return {
      title: (payload?.title || '').trim(),
      subtitle: (payload?.subtitle || '').trim(),
      meta: {
        modalResultsTitle: (payload?.meta?.modal_results_title || '').trim(),
        actions: payload?.meta?.actions || {},
      },
      items,
    }
  } catch {
    return null
  }
}

export const fetchChannelsSection = async (): Promise<ChannelsSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<ChannelsApiResponse>('/api/channels/', {
      baseURL: baseUrl,
    })

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `channel-${index + 1}`,
            name: (item?.name || '').trim(),
            href: (item?.href || '').trim(),
            icon: {
              src: normalizeMediaUrl(item?.icon?.src, baseUrl),
              alt: (item?.icon?.alt || item?.name || '').trim(),
            },
          }))
          .filter((item) => Boolean(item.name && item.href))
      : []

    return {
      title: (payload?.title || '').trim(),
      subtitle: (payload?.subtitle || '').trim(),
      description: (payload?.description || '').trim(),
      meta: {
        itemAriaLabelPrefix: (payload?.meta?.itemAriaLabelPrefix || '').trim(),
      },
      media: {
        background: {
          src: normalizeMediaUrl(payload?.media?.background, baseUrl),
          alt: '',
        },
        image: {
          src: normalizeMediaUrl(payload?.media?.image, baseUrl),
          alt: '',
        },
        secondaryImage: {
          src: normalizeMediaUrl(payload?.media?.secondaryImage, baseUrl),
          alt: '',
        },
      },
      items,
    }
  } catch {
    return null
  }
}
