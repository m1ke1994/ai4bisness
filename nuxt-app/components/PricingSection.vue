<script setup>
import { siteData } from '~/data/siteData'

const CONTACT_FORM_OPEN_EVENT = siteData.events.contactFormOpen
const pricingData = siteData.pricing
const pricingPlans = pricingData.items

const openContactFormModal = () => {
  if (typeof window === 'undefined') return
  window.dispatchEvent(new Event(CONTACT_FORM_OPEN_EVENT))
}
</script>

<template>
  <section
    id="pricing"
    class="relative isolate bg-[#F3F4F7] py-10 sm:py-12 lg:py-16"
  >
    <div
      aria-hidden="true"
      class="pointer-events-none absolute inset-0"
      style="
        background:
          radial-gradient(36rem 20rem at 12% 8%, rgba(111, 99, 255, 0.10), transparent 72%),
          radial-gradient(34rem 18rem at 88% 12%, rgba(126, 182, 255, 0.10), transparent 72%),
          radial-gradient(42rem 18rem at 50% 100%, rgba(111, 99, 255, 0.05), transparent 78%);
      "
    />

    <div class="mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">
      <div class="px-2 text-center">
        <h2
          class="text-[34px] font-semibold leading-[1.06] tracking-[-0.03em] text-[#111218] sm:text-[44px] lg:text-[66px] lg:leading-[1.04]"
        >
          {{ pricingData.title }}
        </h2>
        <h3
          class="mt-2 text-[26px] font-semibold leading-[1.08] tracking-[-0.03em] text-[#9EA4B8] sm:text-[34px] lg:mt-3 lg:text-[52px] lg:leading-[1.05]"
        >
          {{ pricingData.subtitle }}
        </h3>
      </div>

      <div class="relative mt-8 grid grid-cols-1 gap-5 md:mt-12 md:grid-cols-2 lg:gap-6 xl:grid-cols-4">
        <article
          v-for="plan in pricingPlans"
          :key="plan.id"
          class="fade-item group relative flex h-full min-h-[560px] flex-col overflow-hidden rounded-[26px] border p-5 shadow-[0_14px_40px_rgba(17,24,39,0.06)] transition-all duration-500 hover:-translate-y-1 sm:min-h-[600px] sm:rounded-[28px] sm:p-6 lg:min-h-[620px]"
          :class="
            plan.meta.darkCard
              ? 'border-[#3A3D63] bg-[linear-gradient(180deg,#171A31_0%,#121524_100%)] shadow-[0_20px_60px_rgba(28,31,67,0.26)] hover:shadow-[0_28px_70px_rgba(28,31,67,0.34)]'
              : plan.meta.featured
                ? 'border-[#D9DDF2] bg-[linear-gradient(180deg,#FFFFFF_0%,#F6F7FE_100%)] shadow-[0_18px_50px_rgba(92,80,255,0.10)] hover:border-[#C8CFF0] hover:shadow-[0_28px_70px_rgba(92,80,255,0.16)]'
                : 'border-[#E6E8F3] bg-[linear-gradient(180deg,#FFFFFF_0%,#F7F8FC_100%)] hover:border-[#DDE1EF] hover:shadow-[0_24px_60px_rgba(17,24,39,0.10)]'
          "
        >
          <div
            aria-hidden="true"
            class="pointer-events-none absolute inset-x-0 top-0 h-32 opacity-90 transition duration-500 group-hover:opacity-100"
            :class="
              plan.meta.darkCard
                ? 'bg-[radial-gradient(circle_at_20%_10%,rgba(129,117,255,0.28),transparent_70%)]'
                : plan.meta.featured
                  ? 'bg-[radial-gradient(circle_at_20%_10%,rgba(111,99,255,0.18),transparent_72%)]'
                  : 'bg-[radial-gradient(circle_at_20%_10%,rgba(111,99,255,0.10),transparent_72%)]'
            "
          />

          <div class="relative z-10 flex h-full flex-col">
            <div>
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h4
                    class="text-[20px] font-semibold tracking-[-0.02em] sm:text-[22px]"
                    :class="plan.meta.darkCard ? 'text-white' : 'text-[#111218]'"
                  >
                    {{ plan.title }}
                  </h4>

                  <div
                    class="mt-3 inline-flex items-center rounded-full border px-3 py-1.5 text-[11px] font-medium tracking-[-0.01em]"
                    :class="
                      plan.meta.darkCard
                        ? 'border-white/12 bg-white/5 text-white'
                        : 'border-[#E0E5F5] bg-white/90 text-[#414868] shadow-[0_8px_20px_rgba(18,26,52,0.04)]'
                    "
                  >
                    {{ plan.subtitle }}
                  </div>
                </div>

                <span
                  v-if="plan.accentBadge"
                  class="shrink-0 rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.06em]"
                  :class="
                    plan.meta.darkCard
                      ? 'border-[#7F79FF]/35 bg-[rgba(111,99,255,0.14)] text-white'
                      : 'border-[#CFC8FF] bg-[rgba(111,99,255,0.08)] text-[#5B50CF]'
                  "
                >
                  {{ plan.accentBadge }}
                </span>
              </div>

              <p
                v-if="plan.inheritLine"
                class="mt-4 text-[13px] font-medium tracking-[-0.01em]"
                :class="plan.meta.darkCard ? 'text-white' : 'text-[#6F7692]'"
              >
                {{ plan.inheritLine }}
              </p>

              <div
                class="mt-4 h-px w-full bg-gradient-to-r from-transparent via-white/60 to-transparent"
                :class="plan.meta.darkCard ? 'opacity-15' : 'opacity-100'"
              />

              <ul class="mt-4 space-y-2.5">
                <li
                v-for="feature in plan.features"
                :key="feature.id"
                class="flex items-start gap-2.5 text-[13px] leading-[1.45] tracking-[-0.01em] sm:text-[14px]"
                :class="plan.meta.darkCard ? 'text-white' : 'text-[#2E334A]'"
              >
                  <span
                    aria-hidden="true"
                    class="mt-0.5 inline-flex h-4 w-4 shrink-0 items-center justify-center rounded-full border"
                    :class="
                      plan.meta.darkCard
                        ? 'border-white/15 bg-white/5 text-white'
                        : 'border-[#D9DDF0] bg-white text-[#6A5EFD]'
                    "
                  >
                    <svg viewBox="0 0 16 16" class="h-3 w-3" fill="none">
                      <path
                        d="M4 8.2l2.1 2.1L12 4.7"
                        stroke="currentColor"
                        stroke-width="1.6"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  </span>
                  <span>{{ feature.text }}</span>
                </li>
              </ul>
            </div>

            <div class="mt-auto pt-5">
              <div
                class="rounded-[16px] border px-3.5 py-3 text-[12px] leading-[1.35] tracking-[-0.01em] sm:text-[13px]"
                :class="
                  plan.meta.darkCard
                    ? 'border-white/10 bg-white/5 text-white'
                    : 'border-[#E4E8F4] bg-white/80 text-[#59607D]'
                "
              >
                <span class="font-semibold" :class="plan.meta.darkCard ? 'text-white' : 'text-[#2E334A]'">{{ pricingData.meta.channelsLabel }}</span>
                {{ ' ' }}{{ plan.channels }}
              </div>

              <button
                type="button"
                class="mt-4 inline-flex h-[48px] w-full items-center justify-center rounded-[16px] border text-[14px] font-medium tracking-[-0.01em] transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-0 sm:h-[52px] sm:text-[15px]"
                :class="
                  plan.meta.darkCard
                    ? 'border-[#8F87FF]/35 bg-[linear-gradient(90deg,rgba(111,99,255,0.24)_0%,rgba(139,127,255,0.14)_100%)] text-white shadow-[0_14px_36px_rgba(92,80,255,0.20)] hover:border-[#A69FFF]/40 hover:bg-[linear-gradient(90deg,rgba(111,99,255,0.30)_0%,rgba(139,127,255,0.18)_100%)] focus-visible:ring-white/45'
                    : plan.meta.featured
                      ? 'border-[#D4D9F4] bg-[linear-gradient(90deg,rgba(111,99,255,0.10)_0%,rgba(139,127,255,0.06)_100%)] text-[#2A2F45] shadow-[0_12px_28px_rgba(92,80,255,0.10)] hover:border-[#C5CCEF] hover:bg-[linear-gradient(90deg,rgba(111,99,255,0.14)_0%,rgba(139,127,255,0.08)_100%)] focus-visible:ring-[#6F63FF]/35'
                      : 'border-[#E1E5F3] bg-white text-[#2A2F45] shadow-[0_10px_24px_rgba(18,26,52,0.05)] hover:border-[#D0D7EE] hover:bg-[#FBFBFE] focus-visible:ring-[#6F63FF]/30'
                "
                :aria-label="`${plan.cta.label}: ${plan.title}`"
                @click="openContactFormModal"
              >
                {{ plan.cta.label }}
              </button>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>


