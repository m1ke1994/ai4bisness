<script setup>
import { siteData } from '~/data/siteData'

const heroData = siteData.hero
const hiroMobileImageVars = heroData.meta.imageVars.mobile
const hiroDesktopImageVars = heroData.meta.imageVars.desktop
const stats = heroData.items
</script>

<template>
  <section class="relative isolate overflow-hidden">
    <!-- С„РѕРЅ -->
    <div
      class="absolute inset-0 z-0 bg-[linear-gradient(180deg,#02030D_0%,#04061A_24%,#0B0F34_58%,#1C225A_100%)]"
      aria-hidden="true"
    />
    <div
      class="absolute inset-0 z-[2] opacity-90"
      style="
        background:
          radial-gradient(38rem 28rem at 34% 36%, rgba(34, 42, 136, 0.22), transparent 70%),
          radial-gradient(34rem 26rem at 63% 49%, rgba(44, 53, 160, 0.22), transparent 72%),
          radial-gradient(28rem 22rem at 100% 88%, rgba(92, 95, 178, 0.2), transparent 72%);
      "
      aria-hidden="true"
    />

    <img
      :src="siteData.assets.media.heroTexture.src"
      alt=""
      aria-hidden="true"
      class="pointer-events-none absolute bottom-[-250px] left-1/2 z-[1] w-[88%] min-w-[620px] -translate-x-1/2 select-none opacity-5 sm:min-w-[760px]"
      draggable="false"
    />

    <!-- desktop phone -->
    <img
      :src="heroData.media.image.src"
      :alt="heroData.media.image.alt"
      :style="hiroDesktopImageVars"
      class="pointer-events-none absolute right-[var(--hiro-desktop-right)] bottom-[var(--hiro-desktop-bottom)] z-[5] hidden w-[var(--hiro-desktop-w)] max-w-full object-contain select-none lg:block xl:w-[var(--hiro-desktop-w-xl)] xl:max-w-none 2xl:w-[var(--hiro-desktop-w-2xl)]"
      draggable="false"
    />

    <!-- РљРѕРЅС‚РµРЅС‚ -->
    <div class="relative z-10 mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">
      <!-- РњРћР‘РР›РљРђ -->
      <div class="relative flex flex-col items-center pt-12 pb-6 text-center lg:hidden">
        <h1
          class="max-w-[360px] text-[30px] font-semibold leading-[1.15] tracking-[-0.03em] text-white sm:max-w-[440px] sm:text-[34px]"
        >
          <span class="block">{{ heroData.title }}</span>
          <span class="block">{{ heroData.subtitle }}</span>
        </h1>

        <p class="mt-5 max-w-[360px] text-[14px] leading-[1.5] text-[#A9AEC8] sm:max-w-[460px] sm:text-[15px]">
          {{ heroData.description }}
        </p>

        <!-- STATS (РєР°Рє РЅР° СЃРєСЂРёРЅРµ) вЂ” СЃСЂР°Р·Сѓ РїРѕРґ РѕРїРёСЃР°РЅРёРµРј -->
        <div class="mt-6 w-full max-w-[640px]">
          <div
            class="stats-panel rounded-[22px] border border-white/12 bg-white/6 p-3 shadow-[0_18px_60px_rgba(0,0,0,0.35)] backdrop-blur-md sm:rounded-[26px] sm:p-4"
          >
            <div
              class="grid gap-2 [grid-template-columns:repeat(auto-fit,minmax(150px,1fr))] sm:gap-3"
            >
              <div
                v-for="s in stats"
                :key="s.id"
                class="stats-card rounded-[18px] border border-white/10 bg-white/5 px-3 py-3 text-center sm:rounded-[20px] sm:px-4 sm:py-4"
              >
                <div class="text-[20px] font-semibold leading-[1] tracking-[-0.03em] text-white sm:text-[22px]">
                  {{ s.value }}
                </div>
                <div class="mt-2 text-[11px] leading-[1.25] tracking-[-0.01em] text-white/75 sm:text-[12px]">
                  {{ s.text }}
                </div>
              </div>
            </div>

            <div class="mt-3 text-center text-[11px] leading-[1.35] text-white/60 sm:mt-4 sm:text-[12px]">
              {{ heroData.meta.statsDisclaimer }}
            </div>
          </div>
        </div>

        <!-- С‚РµР»РµС„РѕРЅ РїРѕ С†РµРЅС‚СЂСѓ -->
        <div class="mt-7 w-full">
          <img
            :src="heroData.media.image.src"
            :alt="heroData.media.image.alt"
            :style="hiroMobileImageVars"
            class="mx-auto w-[var(--hiro-mobile-w)] max-w-[var(--hiro-mobile-max-w)] object-contain sm:w-[var(--hiro-mobile-w-sm)] sm:max-w-[var(--hiro-mobile-max-w-sm)]"
            draggable="false"
          />
        </div>
      </div>

      <!-- Р”Р•РЎРљРўРћРџ -->
      <div
        class="hidden lg:grid lg:min-h-[680px] lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)] lg:items-start lg:gap-6 xl:min-h-[730px] xl:gap-8"
      >
        <!-- Р»РµРІС‹Р№ Р±Р»РѕРє -->
        <div class="relative pt-14 pb-12 xl:pt-20 xl:pb-14 2xl:pt-24 2xl:pb-16">
          <h1
            class="max-w-[640px] text-[48px] font-semibold leading-[1.12] tracking-[-0.03em] text-white xl:max-w-[820px] xl:text-[64px] 2xl:text-[72px]"
          >
            <span class="block">{{ heroData.title }}</span>
            <span class="mt-3 block">{{ heroData.subtitle }}</span>
          </h1>

          <p class="mt-6 max-w-[560px] text-[18px] leading-[1.42] text-[#A9AEC8] xl:mt-8 xl:max-w-[680px] xl:text-[22px]">
            {{ heroData.description }}
          </p>

          <!-- STATS (РєР°Рє РЅР° СЃРєСЂРёРЅРµ) вЂ” РїРѕРґ РѕРїРёСЃР°РЅРёРµРј, Р°РґР°РїС‚РёРІРЅРѕ -->
          <div class="mt-8 max-w-[760px] xl:mt-10">
            <div
              class="stats-panel rounded-[26px] border border-white/12 bg-white/6 p-4 shadow-[0_22px_70px_rgba(0,0,0,0.40)] backdrop-blur-md xl:p-5"
            >
              <div class="grid grid-cols-3 gap-3 xl:gap-4">
                <div
                  v-for="s in stats"
                  :key="s.id"
                  class="stats-card rounded-[20px] border border-white/10 bg-white/5 px-4 py-4 text-center xl:px-5 xl:py-5"
                >
                  <div class="text-[24px] font-semibold leading-[1] tracking-[-0.03em] text-white xl:text-[26px]">
                    {{ s.value }}
                  </div>
                  <div class="mt-2 text-[12px] leading-[1.25] tracking-[-0.01em] text-white/75 xl:text-[13px]">
                    {{ s.text }}
                  </div>
                </div>
              </div>

              <div class="mt-4 text-center text-[12px] leading-[1.35] text-white/60 xl:text-[13px]">
                {{ heroData.meta.statsDisclaimer }}
              </div>
            </div>
          </div>
        </div>

        <!-- РїСЂР°РІС‹Р№ Р±Р»РѕРє -->
        
      </div>

    </div>
  </section>
</template>

<style scoped>
/* subtle premium edge + inner glow like on the screenshot */
.stats-panel {
  position: relative;
}
.stats-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.06));
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
.stats-card {
  position: relative;
}
.stats-card::after {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  background: radial-gradient(280px 120px at 50% 0%, rgba(142, 132, 255, 0.14), transparent 65%);
  pointer-events: none;
}

/* floating badges animation РѕСЃС‚Р°РІР»СЏРµРј РєР°Рє Р±С‹Р»Рѕ */
.hero-float-badge {
  animation: hero-badge-float 6s ease-in-out infinite;
  will-change: transform;
}
.hero-float-badge--1 {
  animation-delay: 0s;
}
.hero-float-badge--2 {
  animation-delay: 1s;
}
.hero-float-badge--3 {
  animation-delay: 2s;
}

@keyframes hero-badge-float {
  0%,
  100% {
    transform: translate3d(0, 0, 0);
  }
  50% {
    transform: translate3d(0, -8px, 0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-float-badge {
    animation: none;
  }
}
</style>

