<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { siteData } from '~/data/siteData'

const navData = siteData.nav
const navItemsByHref = Object.fromEntries((navData.items || []).map((item) => [item.href, item]))
const navItems = [
  navItemsByHref['#advantages'],
  {
    id: 'nav-integrations',
    slug: 'integrations',
    label: 'Интеграции',
    href: '#integrations',
    sortOrder: 0,
    isActive: true,
  },
  navItemsByHref['#pricing'],
  navItemsByHref['#steps'],
  navItemsByHref['#reviews'],
  navItemsByHref['#contacts'],
].filter(Boolean)
const mobileSocialItems = navData.meta.mobileSocials

const isMobileMenuOpen = ref(false)
const activeHash = ref('')
const scrollProgress = ref(0)
let previousBodyOverflow = ''
let pendingAnchorScrollTimeout = null

const syncHash = () => {
  if (typeof window === 'undefined') return
  activeHash.value = window.location.hash || ''
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const handleMenuItemClick = () => {
  closeMobileMenu()
}

const isAnchorHref = (href) => typeof href === 'string' && href.startsWith('#')

const scrollToAnchor = (href, options = {}) => {
  if (typeof window === 'undefined' || typeof document === 'undefined') return false
  if (!isAnchorHref(href)) return false

  const { behavior = 'smooth', updateHistory = true } = options
  const target = document.querySelector(href)

  if (updateHistory && window.location.hash !== href) {
    window.history.pushState(null, '', href)
  }

  if (!target) {
    syncHash()
    return false
  }

  target.scrollIntoView({ behavior, block: 'start' })
  activeHash.value = href
  return true
}

const clearPendingAnchorScroll = () => {
  if (pendingAnchorScrollTimeout !== null && typeof window !== 'undefined') {
    window.clearTimeout(pendingAnchorScrollTimeout)
    pendingAnchorScrollTimeout = null
  }
}

const scheduleAnchorScroll = async (href, closeMenuFirst = false, options = {}) => {
  if (!isAnchorHref(href)) return

  clearPendingAnchorScroll()

  if (closeMenuFirst && isMobileMenuOpen.value) {
    closeMobileMenu()
    await nextTick()

    pendingAnchorScrollTimeout = window.setTimeout(() => {
      pendingAnchorScrollTimeout = null
      scrollToAnchor(href, options)
    }, 180)
    return
  }

  scrollToAnchor(href, options)
}

const handleNavLinkClick = (event, href) => {
  if (!isAnchorHref(href)) return
  event.preventDefault()
  void scheduleAnchorScroll(href, false)
}

const handleMobileLinkClick = (event, href) => {
  if (!isAnchorHref(href)) {
    handleMenuItemClick()
    return
  }

  event.preventDefault()
  void scheduleAnchorScroll(href, true)
}

const isMobileItemActive = (href) => {
  if (!href.startsWith('#')) return false
  const current = activeHash.value || '#contacts'
  return current === href
}

const handleHashChange = () => {
  if (typeof window === 'undefined') return
  syncHash()

  if (window.location.hash) {
    void scheduleAnchorScroll(window.location.hash, false, {
      updateHistory: false,
    })
  }
}

const handleKeydown = (event) => {
  if (event.key === 'Escape' && isMobileMenuOpen.value) {
    closeMobileMenu()
  }
}

const handleResize = () => {
  if (typeof window === 'undefined') return
  if (window.innerWidth >= 1024 && isMobileMenuOpen.value) {
    closeMobileMenu()
  }
  syncHash()
  updateScrollProgress()
}

const updateScrollProgress = () => {
  if (typeof window === 'undefined' || typeof document === 'undefined') return

  const scrollTop = window.scrollY || document.documentElement.scrollTop || 0
  const documentHeight = document.documentElement.scrollHeight
  const viewportHeight = window.innerHeight
  const scrollableHeight = documentHeight - viewportHeight

  if (scrollableHeight <= 0) {
    scrollProgress.value = 0
    return
  }

  const rawProgress = (scrollTop / scrollableHeight) * 100
  scrollProgress.value = Math.min(100, Math.max(0, rawProgress))
}

watch(isMobileMenuOpen, (opened) => {
  if (typeof document === 'undefined') return

  if (opened) {
    previousBodyOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = previousBodyOverflow
  }
})

onMounted(() => {
  syncHash()
  updateScrollProgress()

  if (typeof window !== 'undefined') {
    window.addEventListener('keydown', handleKeydown)
    window.addEventListener('resize', handleResize)
    window.addEventListener('scroll', updateScrollProgress, { passive: true })
    window.addEventListener('hashchange', handleHashChange)

    if (window.location.hash) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          void scheduleAnchorScroll(window.location.hash, false, {
            updateHistory: false,
          })
        })
      })
    }
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', handleKeydown)
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('scroll', updateScrollProgress)
    window.removeEventListener('hashchange', handleHashChange)
    clearPendingAnchorScroll()
  }

  if (typeof document !== 'undefined') {
    document.body.style.overflow = previousBodyOverflow
  }
})
</script>

<template>
  <!-- HEADER (С„РёРєСЃРёСЂРѕРІР°РЅРЅР°СЏ, РІРїРµСЂРµРґРё РІСЃРµРіРѕ) -->
  <header class="fixed left-0 top-0 z-[1000] w-full bg-[#02030A] shadow-[0_8px_28px_rgba(0,0,0,0.24)]">
    <div class="mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">
      <div class="relative flex h-[74px] items-center justify-between lg:h-[88px]">
        <a :href="navData.meta.brandHref" class="flex shrink-0 items-center gap-3 text-white" :aria-label="siteData.meta.brandName">
          <img
            :src="siteData.assets.media.logo.src"
            :alt="siteData.meta.brandName"
            class="h-[100px] w-auto rounded-full sm:h-[100px] lg:h-[120px] xl:h-[128px]"
            draggable="false"
          />
          <span class="text-[20px] font-semibold leading-none tracking-[-0.02em] sm:text-[24px] lg:text-[26px]">
            {{ siteData.meta.brandName }}
          </span>
        </a>

        <!-- Desktop nav -->
        <nav
          class="absolute left-1/2 top-1/2 hidden -translate-x-1/2 -translate-y-1/2 items-center gap-4 lg:flex xl:gap-8 2xl:gap-14"
          :aria-label="navData.meta.aria.desktopNav"
        >
          <a
            v-for="item in navItems"
            :key="item.href"
            :href="item.href"
            class="text-[15px] font-medium text-[#A8ABC3] transition-colors duration-200 hover:text-[#736CFF] xl:text-[17px] 2xl:text-[20px]"
            @click="handleNavLinkClick($event, item.href)"
          >
            {{ item.label }}
          </a>
        </nav>

        <!-- Mobile burger -->
        <button
          type="button"
          class="relative z-[1001] inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/15 bg-white/[0.03] text-white transition hover:bg-white/5 active:scale-[0.98] lg:hidden"
          :aria-label="isMobileMenuOpen ? navData.meta.aria.closeMenu : navData.meta.aria.openMenu"
          :aria-expanded="isMobileMenuOpen"
          aria-controls="mobile-menu"
          @click="toggleMobileMenu"
        >
          <svg
            v-if="!isMobileMenuOpen"
            viewBox="0 0 24 24"
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            stroke-width="1.9"
            stroke-linecap="round"
          >
            <path d="M4 7h16" />
            <path d="M4 12h16" />
            <path d="M4 17h16" />
          </svg>

          <svg
            v-else
            viewBox="0 0 24 24"
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
          >
            <path d="M5 5l14 14" />
            <path d="M19 5 5 19" />
          </svg>
        </button>
      </div>
    </div>

    <div class="pointer-events-none absolute inset-x-0 bottom-0 h-[4px] bg-white/10">
      <div
        class="h-full bg-[linear-gradient(90deg,#7A6EFF_0%,#9D96FF_100%)] transition-[width] duration-150 ease-out"
        :style="{ width: `${scrollProgress}%` }"
      />
    </div>
  </header>

  <!-- MOBILE FULLSCREEN MENU (РєР°Рє РЅР° СЃРєСЂРёРЅРµ) -->
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isMobileMenuOpen"
        id="mobile-menu"
        class="fixed inset-0 z-[1100] bg-black lg:hidden"
        role="dialog"
        aria-modal="true"
        :aria-label="navData.meta.aria.mobileDialog"
      >
        <!-- Р’РµСЂС…РЅСЏСЏ РїР°РЅРµР»СЊ (Р»РѕРіРѕС‚РёРї + РєСЂРµСЃС‚РёРє), РєР°Рє РЅР° РёР·РѕР±СЂР°Р¶РµРЅРёРё -->
        <div class="mx-auto w-full max-w-[1720px] px-4 sm:px-6">
          <div class="flex h-[74px] items-center justify-between">
            <a
              :href="navData.meta.brandHref"
              class="flex shrink-0 items-center gap-3 text-white"
              :aria-label="siteData.meta.brandName"
              @click="handleMenuItemClick"
            >
              <img
                :src="siteData.assets.media.logo.src"
                :alt="siteData.meta.brandName"
                class="h-14 w-auto rounded-full"
                draggable="false"
              />
              <span class="text-[20px] font-semibold leading-none tracking-[-0.02em]">
                {{ siteData.meta.brandName }}
              </span>
            </a>

            <button
              type="button"
              class="inline-flex h-11 w-11 items-center justify-center text-white"
              :aria-label="navData.meta.aria.closeMenu"
              @click="closeMobileMenu"
            >
              <svg viewBox="0 0 24 24" class="h-8 w-8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
                <path d="M5 5l14 14" />
                <path d="M19 5 5 19" />
              </svg>
            </button>
          </div>
        </div>

        <!-- РњРµРЅСЋ РїРѕ С†РµРЅС‚СЂСѓ -->
        <div class="flex h-[calc(100vh-74px)] flex-col">
          <div class="flex flex-1 items-center justify-center px-6">
            <nav class="-mt-6 flex flex-col items-center gap-5 text-center" :aria-label="navData.meta.aria.mobileNav">
              <a
                v-for="item in navItems"
                :key="item.href"
                :href="item.href"
                class="text-[18px] leading-[1.2] tracking-[-0.02em] transition-colors"
                :class="
                  isMobileItemActive(item.href)
                    ? 'font-semibold text-white'
                    : 'font-medium text-white/60 hover:text-white'
                "
                @click="handleMobileLinkClick($event, item.href)"
              >
                {{ item.label }}
              </a>
            </nav>
          </div>

          <!-- Иконки снизу по центру -->
          <div class="pb-10">
            <div class="flex items-center justify-center gap-4">
              <a
                v-for="item in mobileSocialItems"
                :key="item.id"
                :href="item.href"
                :aria-label="item.ariaLabel"
                class="inline-flex h-11 w-11 items-center justify-center rounded-full bg-[#6A5EFD] text-black shadow-[0_10px_24px_rgba(106,94,253,0.35)]"
                @click.prevent
              >
                <img :src="item.icon.src" :alt="item.icon.alt" class="h-[18px] w-[18px] object-contain" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

