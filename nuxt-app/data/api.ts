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

type ContactsApiItem = {
  name?: string
  icon?: string | null
  href?: string
}

type ContactsApiResponse = {
  title?: string
  subtitle?: string
  description?: string
  meta?: {
    headingLine3?: string
  }
  media?: {
    sectionBackground?: string | null
    cardBackground?: string | null
  }
  channels_title?: string
  channels_subtitle?: string
  items?: ContactsApiItem[]
}

export type ContactsSectionData = {
  title: string
  subtitle: string
  description: string
  meta: {
    headingLine3: string
  }
  media: {
    sectionBackground: {
      src: string
      alt: string
    }
    cardBackground: {
      src: string
      alt: string
    }
  }
  channelsTitle: string
  channelsSubtitle: string
  items: Array<{
    id: string
    name: string
    href: string
    icon: string
  }>
}

type PricingApiFeature = {
  text?: string
}

type PricingApiItem = {
  title?: string
  subtitle?: string
  accent_badge?: string
  inherit_line?: string
  channels?: string
  cta_label?: string
  cta_link?: string
  is_featured?: boolean
  is_dark_card?: boolean
  features?: PricingApiFeature[]
}

type PricingApiResponse = {
  title?: string
  subtitle?: string
  channels_label?: string
  items?: PricingApiItem[]
}

export type PricingSectionData = {
  title: string
  subtitle: string
  channelsLabel: string
  items: Array<{
    id: string
    title: string
    subtitle: string
    channels: string
    accentBadge: string
    inheritLine: string
    meta: {
      featured: boolean
      darkCard: boolean
    }
    cta: {
      label: string
      href: string
    }
    features: Array<{
      id: string
      text: string
    }>
  }>
}

type IntegrationStepsApiItem = {
  day?: string
  title?: string
  description?: string
  image?: string | null
}

type IntegrationStepsApiResponse = {
  title?: string
  subtitle?: string
  items?: IntegrationStepsApiItem[]
  cta?: {
    titleLines?: string[]
    media?: {
      background?: string | null
      image?: string | null
    }
  }
}

export type IntegrationStepsSectionData = {
  title: string
  subtitle: string
  items: Array<{
    id: string
    day: string
    title: string
    description: string
    media: {
      image: {
        src: string
        alt: string
      }
    }
  }>
  cta: {
    titleLines: string[]
    media: {
      background: {
        src: string
        alt: string
      }
      image: {
        src: string
        alt: string
      }
    }
  }
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

export const fetchContactsSection = async (): Promise<ContactsSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<ContactsApiResponse>('/api/contacts/', {
      baseURL: baseUrl,
    })

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `contact-channel-${index + 1}`,
            name: (item?.name || '').trim(),
            href: (item?.href || '').trim(),
            icon: normalizeMediaUrl(item?.icon, baseUrl),
          }))
          .filter((item) => Boolean(item.name && item.href))
      : []

    return {
      title: (payload?.title || '').trim(),
      subtitle: (payload?.subtitle || '').trim(),
      description: (payload?.description || '').trim(),
      meta: {
        headingLine3: (payload?.meta?.headingLine3 || '').trim(),
      },
      media: {
        sectionBackground: {
          src: normalizeMediaUrl(payload?.media?.sectionBackground, baseUrl),
          alt: '',
        },
        cardBackground: {
          src: normalizeMediaUrl(payload?.media?.cardBackground, baseUrl),
          alt: '',
        },
      },
      channelsTitle: (payload?.channels_title || '').trim(),
      channelsSubtitle: (payload?.channels_subtitle || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchPricingSection = async (): Promise<PricingSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<PricingApiResponse>('/api/pricing/', {
      baseURL: baseUrl,
    })

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => {
            const features = Array.isArray(item?.features)
              ? item.features
                  .map((feature, featureIndex) => ({
                    id: `pricing-feature-${index + 1}-${featureIndex + 1}`,
                    text: (feature?.text || '').trim(),
                  }))
                  .filter((feature) => Boolean(feature.text))
              : []

            return {
              id: `pricing-plan-${index + 1}`,
              title: (item?.title || '').trim(),
              subtitle: (item?.subtitle || '').trim(),
              channels: (item?.channels || '').trim(),
              accentBadge: (item?.accent_badge || '').trim(),
              inheritLine: (item?.inherit_line || '').trim(),
              meta: {
                featured: Boolean(item?.is_featured),
                darkCard: Boolean(item?.is_dark_card),
              },
              cta: {
                label: (item?.cta_label || '').trim(),
                href: (item?.cta_link || '').trim(),
              },
              features,
            }
          })
          .filter((item) => Boolean(item.title || item.subtitle || item.features.length))
      : []

    return {
      title: (payload?.title || '').trim(),
      subtitle: (payload?.subtitle || '').trim(),
      channelsLabel: (payload?.channels_label || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchIntegrationStepsSection = async (): Promise<IntegrationStepsSectionData | null> => {
  const baseUrl = normalizeBaseUrl(getBackendBaseUrl())

  try {
    const payload = await $fetch<IntegrationStepsApiResponse>('/api/integration-steps/', {
      baseURL: baseUrl,
    })

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `step-${index + 1}`,
            day: (item?.day || '').trim(),
            title: (item?.title || '').trim(),
            description: (item?.description || '').trim(),
            media: {
              image: {
                src: normalizeMediaUrl(item?.image, baseUrl),
                alt: (item?.title || '').trim(),
              },
            },
          }))
          .filter((item) => Boolean(item.day || item.title || item.description || item.media.image.src))
      : []

    const titleLines = Array.isArray(payload?.cta?.titleLines)
      ? payload.cta.titleLines.map((line) => (line || '').trim()).slice(0, 2)
      : []

    return {
      title: (payload?.title || '').trim(),
      subtitle: (payload?.subtitle || '').trim(),
      items,
      cta: {
        titleLines,
        media: {
          background: {
            src: normalizeMediaUrl(payload?.cta?.media?.background, baseUrl),
            alt: '',
          },
          image: {
            src: normalizeMediaUrl(payload?.cta?.media?.image, baseUrl),
            alt: '',
          },
        },
      },
    }
  } catch {
    return null
  }
}
