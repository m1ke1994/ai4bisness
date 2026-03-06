<template>
  <section
    id="contacts"
    class="relative overflow-hidden bg-[#01020a] py-10 sm:py-12 lg:py-16"
  >
    <img
      :src="contactsData.media.sectionBackground.src"
      alt=""
      aria-hidden="true"
      class="pointer-events-none absolute inset-0 h-full w-full object-cover"
      draggable="false"
    />

    <div
      aria-hidden="true"
      class="absolute inset-0 bg-[linear-gradient(180deg,rgba(4,5,18,0.72)_0%,rgba(7,9,28,0.58)_38%,rgba(7,9,28,0.84)_100%)]"
    ></div>

    <div
      aria-hidden="true"
      class="absolute inset-0 opacity-[0.18]"
      style="
        background-image: repeating-linear-gradient(
          125deg,
          rgba(194, 202, 255, 0.18) 0px,
          rgba(194, 202, 255, 0.18) 2px,
          transparent 2px,
          transparent 14px
        );
      "
    ></div>

    <div class="relative z-10 mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">
      <div
        class="relative min-h-[420px] overflow-hidden rounded-[36px] bg-[rgba(9,12,41,0.18)] xl:min-h-[560px]"
      >
        <div
          class="relative z-10 grid items-start gap-8 p-6 pb-0 sm:p-10 sm:pb-0 lg:grid-cols-1 xl:grid-cols-[minmax(0,1fr)_760px] xl:px-20 xl:pt-20"
        >

          <!-- ЛЕВАЯ ЧАСТЬ -->
          <div class="pt-2 xl:pt-14">
            <h2
              class="max-w-[820px] text-[34px] font-semibold leading-[0.96] tracking-[-0.035em] text-white sm:text-[48px] lg:text-[56px] xl:text-[68px]"
            >
              {{ contactsData.title }}

              <span
                class="block bg-[linear-gradient(90deg,#7A6EFF_0%,#9D96FF_100%)] bg-clip-text text-transparent"
              >
                {{ contactsData.subtitle }}
              </span>

              <span class="block">
                {{ contactsData.meta.headingLine3 }}
              </span>
            </h2>

          
          </div>

          <!-- ПРАВАЯ ФИОЛЕТОВАЯ КАРТОЧКА -->
          <div class="flex h-full items-end xl:justify-end">

            <div
              class="relative w-full max-w-[760px] overflow-hidden rounded-[32px] shadow-[0_30px_80px_rgba(34,24,89,0.38)]"
            >

              <img
                :src="contactsData.media.cardBackground.src"
                alt=""
                aria-hidden="true"
                class="absolute inset-0 h-full w-full object-cover"
              />

              <div
                class="absolute inset-0 bg-[linear-gradient(180deg,rgba(121,107,255,0.62)_0%,rgba(129,117,255,0.58)_45%,rgba(115,105,247,0.68)_100%)]"
              ></div>

              <div
                class="absolute inset-0 opacity-[0.10]"
                style="
                  background-image: repeating-linear-gradient(
                    130deg,
                    rgba(255,255,255,0.35) 0px,
                    rgba(255,255,255,0.35) 2px,
                    transparent 2px,
                    transparent 16px
                  );
                "
              ></div>

              <div class="relative z-10 px-8 py-10 lg:px-12 lg:py-12">

                <h3
                  class="text-[32px] font-semibold leading-[1.1] tracking-[-0.03em] text-white lg:text-[40px]"
                >
                  {{ contactsData.channelsTitle }}
                  <span class="block">{{ contactsData.channelsSubtitle }}</span>
                </h3>

                <!-- СЕТКА КАНАЛОВ -->
                <div
                  class="mt-10 grid grid-cols-3 gap-4 sm:grid-cols-4 lg:grid-cols-5"
                >

                  <a
                    v-for="item in socialMedia"
                    :key="item.id"
                    :href="item.href"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="group flex flex-col items-center justify-center gap-2 rounded-xl
                           bg-white/10 p-4 backdrop-blur-md transition
                           hover:bg-white/20"
                  >

                    <div
                      class="flex h-12 w-12 items-center justify-center rounded-lg"
                    >
                      <img
                        :src="item.icon"
                        :alt="item.name"
                        class="h-6 w-6 object-contain"
                      />
                    </div>

                    <span
                      class="text-xs text-white/80 group-hover:text-white"
                    >
                      {{ item.name }}
                    </span>

                  </a>

                </div>

              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { fetchContactsSection } from '~/data/api'
import { siteData } from '~/data/siteData'

const fallbackContactsData = siteData.contacts

const fallbackSocialMedia = [
  { id: 'telegram', name: 'Telegram', icon: '/images/icons/telegram.svg', href: 'https://example.com' },
  { id: 'avito', name: 'Avito', icon: '/images/icons/avito.svg', href: 'https://example.com' },
  { id: 'instagram', name: 'Instagram', icon: '/images/icons/instagram.svg', href: 'https://example.com' },
  { id: 'facebook', name: 'Facebook', icon: '/images/icons/facebook.svg', href: 'https://example.com' },
  { id: 'whatsapp', name: 'WhatsApp', icon: '/images/icons/whatsapp.svg', href: 'https://example.com' },
  { id: 'youtube', name: 'YouTube', icon: '/images/icons/youtube.svg', href: 'https://example.com' },
  { id: 'tiktok', name: 'TikTok', icon: '/images/icons/tiktok.svg', href: 'https://example.com' },
  { id: 'mail', name: 'Mail', icon: '/images/icons/mail.svg', href: 'https://example.com' },
  { id: 'vk', name: 'ВКонтакте', icon: '/images/icons/vk.svg', href: 'https://example.com' },
  { id: 'max', name: 'Max', icon: '/images/icons/Max.svg', href: 'https://example.com' },
]

const { data: contactsSection } = useAsyncData('contacts-section', fetchContactsSection, {
  server: false,
  default: () => null,
})

const contactsData = computed(() => {
  const fallbackChannelsTitle = fallbackContactsData?.meta?.card?.titleLine1 || 'Выберите удобный'
  const fallbackChannelsSubtitle = fallbackContactsData?.meta?.card?.titleLine2 || 'канал связи'

  if (!contactsSection.value) {
    return {
      ...fallbackContactsData,
      channelsTitle: fallbackChannelsTitle,
      channelsSubtitle: fallbackChannelsSubtitle,
    }
  }

  return {
    ...fallbackContactsData,
    title: contactsSection.value.title || fallbackContactsData.title,
    subtitle: contactsSection.value.subtitle || fallbackContactsData.subtitle,
    description: contactsSection.value.description || fallbackContactsData.description,
    meta: {
      ...fallbackContactsData.meta,
      headingLine3: contactsSection.value.meta.headingLine3 || fallbackContactsData.meta.headingLine3,
    },
    media: {
      ...fallbackContactsData.media,
      sectionBackground: {
        ...fallbackContactsData.media.sectionBackground,
        src: contactsSection.value.media.sectionBackground.src || fallbackContactsData.media.sectionBackground.src,
      },
      cardBackground: {
        ...fallbackContactsData.media.cardBackground,
        src: contactsSection.value.media.cardBackground.src || fallbackContactsData.media.cardBackground.src,
      },
    },
    channelsTitle: contactsSection.value.channelsTitle || fallbackChannelsTitle,
    channelsSubtitle: contactsSection.value.channelsSubtitle || fallbackChannelsSubtitle,
  }
})

const socialMedia = computed(() => {
  if (!contactsSection.value || !contactsSection.value.items.length) {
    return fallbackSocialMedia
  }

  return contactsSection.value.items.map((item) => ({
    id: item.id,
    name: item.name,
    icon: item.icon,
    href: item.href,
  }))
})
</script>
