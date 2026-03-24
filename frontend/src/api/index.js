const DEFAULT_INTERNAL_API_BASE = 'http://backend:8000'
const DEFAULT_PUBLIC_API_BASE = 'https://ai4businesss.com'

const normalizeBaseUrl = (value = '') => String(value || '').trim().replace(/\/+$/, '')

const configuredApiBase = normalizeBaseUrl(import.meta.env.VITE_API_BASE || '')
const configuredSiteUrl = normalizeBaseUrl(import.meta.env.VITE_PUBLIC_SITE_URL || DEFAULT_PUBLIC_API_BASE)

const pushUnique = (list, value) => {
  const normalized = normalizeBaseUrl(value)
  if (!normalized) return
  if (!list.includes(normalized)) {
    list.push(normalized)
  }
}

export const resolveApiBase = () => {
  if (typeof window === 'undefined') {
    return configuredApiBase || DEFAULT_INTERNAL_API_BASE
  }

  const host = window.location.hostname
  const origin = normalizeBaseUrl(window.location.origin)

  if (configuredApiBase && !/backend:8000/i.test(configuredApiBase)) {
    return configuredApiBase
  }

  if (host === 'localhost' || host === '127.0.0.1') {
    return 'http://localhost:8000'
  }

  if (origin) {
    return origin
  }

  return configuredSiteUrl || DEFAULT_PUBLIC_API_BASE
}

const getFooterPagesApiBaseUrls = () => {
  const candidates = []

  pushUnique(candidates, configuredApiBase)
  pushUnique(candidates, configuredSiteUrl)

  if (typeof window !== 'undefined') {
    pushUnique(candidates, window.location.origin)

    const host = window.location.hostname
    if ((host === 'localhost' || host === '127.0.0.1') && /backend:8000/i.test(configuredApiBase)) {
      pushUnique(candidates, 'http://localhost:8000')
    }
  }

  pushUnique(candidates, DEFAULT_INTERNAL_API_BASE)

  return candidates
}

const hasApiSuffix = (baseUrl) => {
  try {
    const path = new URL(baseUrl).pathname.replace(/\/+$/, '')
    return path.endsWith('/api')
  } catch {
    return /\/api\/?$/i.test(baseUrl)
  }
}

const buildFooterPageEndpoints = (slug, baseUrl) => {
  const encodedSlug = encodeURIComponent(slug)
  const apiPath = `/api/footer-pages/${encodedSlug}/`
  const plainPath = `/footer-pages/${encodedSlug}/`

  if (hasApiSuffix(baseUrl)) {
    return [plainPath, apiPath]
  }

  return [apiPath, plainPath]
}

const normalizeMediaUrl = (value, baseUrl) => {
  if (!value) return ''
  if (/^https?:\/\//i.test(value)) return value
  if (value.startsWith('/')) return `${baseUrl}${value}`
  return `${baseUrl}/${value}`
}

const normalizeTextList = (value) => {
  if (!Array.isArray(value)) return []

  return value
    .map((item) => {
      if (typeof item === 'string') return item.trim()
      if (item && typeof item === 'object' && typeof item.text === 'string') {
        return item.text.trim()
      }
      return ''
    })
    .filter(Boolean)
}

const fetchJson = async (path, baseUrl = resolveApiBase()) => {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl)
  const response = await fetch(`${normalizedBaseUrl}${path}`, {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error(`API request failed (${response.status}) for ${path}`)
  }

  return response.json()
}

const postJson = async (path, payload, baseUrl = resolveApiBase()) => {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl)
  const response = await fetch(`${normalizedBaseUrl}${path}`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  let responsePayload = null
  try {
    responsePayload = await response.json()
  } catch {
    responsePayload = null
  }

  if (!response.ok) {
    const error = new Error(
      String(responsePayload?.message || 'Не удалось отправить данные. Попробуйте еще раз.'),
    )
    error.status = response.status
    error.payload = responsePayload
    throw error
  }

  return responsePayload
}

export const submitCompanyBrief = async (payload) => {
  const baseUrl = resolveApiBase()
  return postJson('/api/company-briefs/', payload, baseUrl)
}

export const fetchHeaderSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/header/', baseUrl)

    const menuItems = Array.isArray(payload?.menu_items)
      ? payload.menu_items
          .map((item) => ({
            label: String(item?.title || '').trim(),
            href: String(item?.href || '').trim(),
          }))
          .filter((item) => item.label && item.href)
      : []

    return {
      brandName: String(payload?.brand_name || '').trim(),
      logo: normalizeMediaUrl(payload?.logo, normalizeBaseUrl(baseUrl)),
      logoLink: String(payload?.logo_link || '/').trim() || '/',
      menuItems,
    }
  } catch {
    return null
  }
}

export const fetchFooterSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/footer/', baseUrl)

    const links = Array.isArray(payload?.links)
      ? payload.links
          .map((item, index) => ({
            id: `footer-link-${index + 1}`,
            label: String(item?.title || '').trim(),
            href: String(item?.href || '').trim(),
          }))
          .filter((item) => item.label && item.href)
      : []

    return {
      brandName: String(payload?.brand_name || '').trim(),
      logo: normalizeMediaUrl(payload?.logo, normalizeBaseUrl(baseUrl)),
      logoLink: String(payload?.logo_link || '/').trim() || '/',
      links,
    }
  } catch {
    return null
  }
}

export const fetchFooterPageBySlug = async (slug) => {
  const normalizedSlug = String(slug || '').trim()
  if (!normalizedSlug) {
    return null
  }

  const baseUrls = getFooterPagesApiBaseUrls()

  for (const baseUrl of baseUrls) {
    const endpoints = buildFooterPageEndpoints(normalizedSlug, baseUrl)

    for (const endpoint of endpoints) {
      try {
        const payload = await fetchJson(endpoint, baseUrl)

        const key = String(payload?.key || '').trim()
        const responseSlug = String(payload?.slug || '').trim()
        const title = String(payload?.title || '').trim()

        if (!key || !responseSlug || !title) {
          continue
        }

        return {
          key,
          slug: responseSlug,
          title,
          content: String(payload?.content || '').trim(),
        }
      } catch {
        // Try the next endpoint/base URL variant.
      }
    }
  }

  return null
}

export const fetchHeroSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/hero/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item) => ({
            value: String(item?.value || '').trim(),
            text: String(item?.text || '').trim(),
          }))
          .filter((item) => item.value || item.text)
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitle: String(payload?.subtitle || '').trim(),
      description: String(payload?.description || '').trim(),
      image: normalizeMediaUrl(payload?.image, normalizeBaseUrl(baseUrl)),
      statsDisclaimer: String(payload?.stats_disclaimer || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchReviewsSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/reviews/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: String(item?.id ?? `review-${index + 1}`),
            company: String(item?.company || '').trim(),
            person: String(item?.person || '').trim(),
            previewText: String(item?.preview_text || '').trim(),
            previewBullets: normalizeTextList(item?.preview_bullets),
            detailsText: String(item?.details_text || '').trim(),
            results: normalizeTextList(item?.results),
          }))
          .filter(
            (item) =>
              item.company ||
              item.person ||
              item.previewText ||
              item.detailsText ||
              item.previewBullets.length ||
              item.results.length,
          )
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitle: String(payload?.subtitle || '').trim(),
      meta: {
        modalResultsTitle: String(payload?.meta?.modal_results_title || '').trim(),
        actions: payload?.meta?.actions || {},
      },
      items,
    }
  } catch {
    return null
  }
}

export const fetchChannelsSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/channels/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `channel-${index + 1}`,
            name: String(item?.name || '').trim(),
            href: String(item?.href || '').trim(),
            icon: {
              src: normalizeMediaUrl(item?.icon?.src, normalizeBaseUrl(baseUrl)),
              alt: String(item?.icon?.alt || item?.name || '').trim(),
            },
          }))
          .filter((item) => item.name && item.href)
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitle: String(payload?.subtitle || '').trim(),
      description: String(payload?.description || '').trim(),
      meta: {
        itemAriaLabelPrefix: String(payload?.meta?.itemAriaLabelPrefix || '').trim(),
      },
      media: {
        background: {
          src: normalizeMediaUrl(payload?.media?.background, normalizeBaseUrl(baseUrl)),
          alt: '',
        },
        image: {
          src: normalizeMediaUrl(payload?.media?.image, normalizeBaseUrl(baseUrl)),
          alt: '',
        },
        secondaryImage: {
          src: normalizeMediaUrl(payload?.media?.secondaryImage, normalizeBaseUrl(baseUrl)),
          alt: '',
        },
      },
      items,
    }
  } catch {
    return null
  }
}

export const fetchContactsSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/contacts/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `contact-channel-${index + 1}`,
            name: String(item?.name || '').trim(),
            href: String(item?.href || '').trim(),
            icon: normalizeMediaUrl(item?.icon, normalizeBaseUrl(baseUrl)),
          }))
          .filter((item) => item.name && item.href)
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitle: String(payload?.subtitle || '').trim(),
      description: String(payload?.description || '').trim(),
      meta: {
        headingLine3: String(payload?.meta?.headingLine3 || '').trim(),
      },
      media: {
        sectionBackground: {
          src: normalizeMediaUrl(payload?.media?.sectionBackground, normalizeBaseUrl(baseUrl)),
          alt: '',
        },
        cardBackground: {
          src: normalizeMediaUrl(payload?.media?.cardBackground, normalizeBaseUrl(baseUrl)),
          alt: '',
        },
      },
      channelsTitle: String(payload?.channels_title || '').trim(),
      channelsSubtitle: String(payload?.channels_subtitle || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchPricingSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/pricing/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => {
            const features = Array.isArray(item?.features)
              ? item.features
                  .map((feature, featureIndex) => ({
                    id: `pricing-feature-${index + 1}-${featureIndex + 1}`,
                    text: String(feature?.text || '').trim(),
                  }))
                  .filter((feature) => feature.text)
              : []

            return {
              id: `pricing-plan-${index + 1}`,
              title: String(item?.title || '').trim(),
              subtitle: String(item?.subtitle || '').trim(),
              channels: String(item?.channels || '').trim(),
              accentBadge: String(item?.accent_badge || '').trim(),
              inheritLine: String(item?.inherit_line || '').trim(),
              meta: {
                featured: Boolean(item?.is_featured),
                darkCard: Boolean(item?.is_dark_card),
              },
              cta: {
                label: String(item?.cta_label || '').trim(),
                href: String(item?.cta_link || '').trim(),
              },
              features,
            }
          })
          .filter((item) => item.title || item.subtitle || item.features.length)
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitle: String(payload?.subtitle || '').trim(),
      channelsLabel: String(payload?.channels_label || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchIntegrationStepsSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/integration-steps/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `step-${index + 1}`,
            day: String(item?.day || '').trim(),
            title: String(item?.title || '').trim(),
            description: String(item?.description || '').trim(),
            media: {
              image: {
                src: normalizeMediaUrl(item?.image, normalizeBaseUrl(baseUrl)),
                alt: String(item?.title || '').trim(),
              },
            },
          }))
          .filter((item) => item.day || item.title || item.description || item.media.image.src)
      : []

    const titleLines = Array.isArray(payload?.cta?.titleLines)
      ? payload.cta.titleLines.map((line) => String(line || '').trim()).slice(0, 2)
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitle: String(payload?.subtitle || '').trim(),
      items,
      cta: {
        titleLines,
        media: {
          background: {
            src: normalizeMediaUrl(payload?.cta?.media?.background, normalizeBaseUrl(baseUrl)),
            alt: '',
          },
          image: {
            src: normalizeMediaUrl(payload?.cta?.media?.image, normalizeBaseUrl(baseUrl)),
            alt: '',
          },
        },
      },
    }
  } catch {
    return null
  }
}

export const fetchSystemIntegrationsSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/system-integrations/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `integration-row-${index + 1}`,
            title: String(item?.title || '').trim(),
            description: String(item?.description || '').trim(),
            media: {
              image: {
                src: normalizeMediaUrl(item?.image, normalizeBaseUrl(baseUrl)),
                alt: String(item?.title || '').trim(),
              },
            },
          }))
          .filter((item) => item.title || item.description || item.media.image.src)
      : []

    return {
      title: String(payload?.title || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchSubscriptionsSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/subscriptions/', baseUrl)

    const items = Array.isArray(payload?.items)
      ? payload.items
          .map((item, index) => ({
            id: `ai-value-point-${index + 1}`,
            text: String(item?.text || '').trim(),
          }))
          .filter((item) => item.text)
      : []

    return {
      title: String(payload?.title || '').trim(),
      subtitlePrefix: String(payload?.subtitle_prefix || '').trim(),
      subtitleHighlight: String(payload?.subtitle_highlight || '').trim(),
      badgePrimary: String(payload?.badge_primary || '').trim(),
      badgeSecondary: String(payload?.badge_secondary || '').trim(),
      description: String(payload?.description || '').trim(),
      leftLabel: String(payload?.left_label || '').trim(),
      rightLabel: String(payload?.right_label || '').trim(),
      paidTitle: String(payload?.paid_title || '').trim(),
      paidDescription: String(payload?.paid_description || '').trim(),
      noteDescription: String(payload?.note_description || '').trim(),
      items,
    }
  } catch {
    return null
  }
}

export const fetchEffectivenessSection = async () => {
  const baseUrl = resolveApiBase()

  try {
    const payload = await fetchJson('/api/effectiveness/', baseUrl)

    const trainingItems = Array.isArray(payload?.training?.items)
      ? payload.training.items
          .map((item, index) => ({
            id: `training-source-${index + 1}`,
            title: String(item?.title || '').trim(),
          }))
          .filter((item) => item.title)
      : []

    const compareItems = Array.isArray(payload?.summary?.items)
      ? payload.summary.items
          .map((item, index) => ({
            id: `advantage-row-${index + 1}`,
            title: String(item?.title || '').trim(),
            aiDescription: String(item?.ai_description || '').trim(),
            humanDescription: String(item?.human_description || '').trim(),
          }))
          .filter((item) => item.title || item.aiDescription || item.humanDescription)
      : []

    return {
      training: {
        title: String(payload?.training?.title || '').trim(),
        rightPill: String(payload?.training?.right_pill || '').trim(),
        rightTitle: String(payload?.training?.right_title || '').trim(),
        items: trainingItems,
      },
      summary: {
        subtitle: String(payload?.summary?.subtitle || '').trim(),
        title: String(payload?.summary?.title || '').trim(),
        desktopStageLabel: String(payload?.summary?.desktop_stage_label || '').trim(),
        desktopAiLabel: String(payload?.summary?.desktop_ai_label || '').trim(),
        desktopHumanLabel: String(payload?.summary?.desktop_human_label || '').trim(),
        mobileAiLabel: String(payload?.summary?.mobile_ai_label || '').trim(),
        mobileHumanLabel: String(payload?.summary?.mobile_human_label || '').trim(),
        stageDescriptionLabel: String(payload?.summary?.stage_description_label || '').trim(),
        desktopFooter: String(payload?.summary?.desktop_footer || '').trim(),
        items: compareItems,
      },
    }
  } catch {
    return null
  }
}
