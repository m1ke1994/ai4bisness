<template>
  <section class="relative isolate bg-[#F3F4F7] py-10 sm:py-12 lg:py-16">
    <div
      aria-hidden="true"
      class="pointer-events-none absolute inset-0"
      style="
        background:
          radial-gradient(34rem 18rem at 10% 10%, rgba(111, 99, 255, 0.09), transparent 72%),
          radial-gradient(34rem 18rem at 90% 14%, rgba(126, 182, 255, 0.09), transparent 72%),
          radial-gradient(38rem 20rem at 50% 100%, rgba(111, 99, 255, 0.05), transparent 78%);
      "
    />

    <div class="relative z-10 mx-auto w-full max-w-[1120px] px-4 sm:px-6 lg:px-10">
      <div class="overflow-hidden rounded-[30px] border border-[#E1E6F4] bg-white p-6 shadow-[0_20px_60px_rgba(17,24,39,0.08)] sm:p-8 lg:p-10">
        <h1 class="text-[34px] font-semibold leading-[1.04] tracking-[-0.03em] text-[#111218] sm:text-[44px] lg:text-[52px]">
          Анкета для компаний
        </h1>

        <p class="mt-4 max-w-[900px] text-[15px] leading-[1.6] text-[#4A5270] sm:text-[16px]">
          Эта анкета нужна, чтобы мы точнее настроили ИИ-ассистента под ваш бизнес: сценарии общения, автоматизацию, интеграции и рабочую логику.
          Чем подробнее заполнены поля, тем качественнее будет итоговая настройка.
        </p>

        <div
          v-if="submitSuccessMessage"
          class="mt-6 rounded-[16px] border border-[#CFE5C7] bg-[#F2FBEE] px-4 py-3 text-[14px] text-[#2E6B2E] sm:text-[15px]"
        >
          {{ submitSuccessMessage }}
        </div>

        <div
          v-if="submitErrorMessage"
          class="mt-4 rounded-[16px] border border-[#F3C8CD] bg-[#FEF3F4] px-4 py-3 text-[14px] text-[#B42318] sm:text-[15px]"
        >
          {{ submitErrorMessage }}
        </div>

        <form class="mt-8 space-y-8" novalidate @submit.prevent="handleSubmit">
          <section class="rounded-[24px] border border-[#E4E8F3] bg-[#F8F9FD] p-5 sm:p-6">
            <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-[#1A2035] sm:text-[28px]">Основные</h2>

            <div class="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-5">
              <div
                v-for="field in basicFields"
                :key="field.key"
                :class="field.full ? 'sm:col-span-2' : ''"
              >
                <BriefField
                  :id="field.key"
                  v-model="form[field.key]"
                  :label="field.label"
                  :helper="field.helper"
                  :placeholder="field.placeholder"
                  :error="errors[field.key]"
                  :required="Boolean(field.required)"
                  :disabled="isSubmitting"
                  :as="field.as || 'input'"
                  :type="field.type || 'text'"
                  :rows="field.rows || 4"
                  :options="field.options || []"
                  :autocomplete="field.autocomplete || 'off'"
                  :maxlength="field.maxlength || null"
                  @blur="revalidateIfNeeded"
                />
              </div>
            </div>
          </section>

          <section class="rounded-[24px] border border-[#E4E8F3] bg-[#F8F9FD] p-5 sm:p-6">
            <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-[#1A2035] sm:text-[28px]">Контакты</h2>

            <div class="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-5">
              <div
                v-for="field in contactFields"
                :key="field.key"
                :class="field.full ? 'sm:col-span-2' : ''"
              >
                <BriefField
                  :id="field.key"
                  v-model="form[field.key]"
                  :label="field.label"
                  :helper="field.helper"
                  :placeholder="field.placeholder"
                  :error="errors[field.key]"
                  :required="Boolean(field.required)"
                  :disabled="isSubmitting"
                  :type="field.type || 'text'"
                  :autocomplete="field.autocomplete || 'off'"
                  :maxlength="field.maxlength || null"
                  @blur="revalidateIfNeeded"
                />
              </div>
            </div>
          </section>

          <section class="rounded-[24px] border border-[#E4E8F3] bg-[#F8F9FD] p-5 sm:p-6">
            <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-[#1A2035] sm:text-[28px]">Услуги</h2>
            <p class="mt-3 text-[14px] leading-[1.55] text-[#536082] sm:text-[15px]">
              Если у вас несколько услуг, добавьте каждую отдельно, чтобы мы точнее настроили сценарии продаж и консультаций.
            </p>

            <div class="mt-5 space-y-4">
              <ServiceCard
                v-for="(service, index) in form.services"
                :key="`service-${index}`"
                :service="service"
                :errors="errors.services[index] || createEmptyServiceErrors()"
                :index="index"
                :can-remove="form.services.length > 1"
                :disabled="isSubmitting"
                @update="(payload) => handleServiceUpdate(index, payload)"
                @remove="removeService(index)"
                @blur="revalidateIfNeeded"
              />
            </div>

            <button
              type="button"
              class="mt-5 inline-flex h-[44px] items-center justify-center rounded-[14px] border border-[#D4DAEE] bg-white px-5 text-[14px] font-medium text-[#2D3551] shadow-[0_8px_24px_rgba(17,24,39,0.04)] transition hover:border-[#C4CCEB] hover:bg-[#FDFDFF] disabled:cursor-not-allowed disabled:opacity-70"
              :disabled="isSubmitting"
              @click="addService"
            >
              Добавить услугу
            </button>
          </section>

          <section class="rounded-[24px] border border-[#E4E8F3] bg-[#F8F9FD] p-5 sm:p-6">
            <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-[#1A2035] sm:text-[28px]">Ассистенты</h2>
            <p class="mt-3 text-[14px] leading-[1.55] text-[#536082] sm:text-[15px]">
              Выберите каналы, где ИИ-ассистент будет общаться с клиентами или обрабатывать обращения.
            </p>

            <div
              v-if="errors.assistantChannels"
              class="mt-4 rounded-[12px] border border-[#F3C8CD] bg-[#FEF3F4] px-3 py-2 text-[13px] text-[#B42318]"
            >
              {{ errors.assistantChannels }}
            </div>

            <div class="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <label
                v-for="channel in ASSISTANT_CHANNELS"
                :key="channel.id"
                class="group relative flex cursor-pointer gap-3 rounded-[14px] border bg-white p-4 transition"
                :class="isSelected(form.assistantChannels, channel.label) ? 'border-[#6F63FF] shadow-[0_12px_30px_rgba(111,99,255,0.14)]' : 'border-[#DDE3F2] hover:border-[#C8D1EB]'"
              >
                <input
                  :checked="isSelected(form.assistantChannels, channel.label)"
                  type="checkbox"
                  class="mt-0.5 h-4 w-4 shrink-0 rounded border-[#C5CEE6] text-[#6F63FF] focus:ring-[#6F63FF]/30"
                  :disabled="isSubmitting"
                  @change="toggleChoice('assistantChannels', channel.label)"
                />

                <span class="min-w-0">
                  <span class="block text-[14px] font-semibold leading-[1.3] text-[#1B2138]">{{ channel.label }}</span>
                  <span class="mt-1 block text-[12px] leading-[1.45] text-[#65708F]">{{ channel.description }}</span>
                </span>
              </label>
            </div>
          </section>

          <section class="rounded-[24px] border border-[#E4E8F3] bg-[#F8F9FD] p-5 sm:p-6">
            <h2 class="text-[24px] font-semibold tracking-[-0.02em] text-[#1A2035] sm:text-[28px]">Интеграции</h2>
            <p class="mt-3 text-[14px] leading-[1.55] text-[#536082] sm:text-[15px]">
              Выберите CRM, системы бронирования и сервисы, с которыми нужно связать ИИ-ассистента.
            </p>

            <div class="mt-5 rounded-[18px] border border-[#DFE5F3] bg-white p-4 sm:p-5">
              <h3 class="text-[17px] font-semibold text-[#1A2035]">CRM и системы</h3>
              <div class="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                <label
                  v-for="integration in crmIntegrationOptions"
                  :key="integration.label"
                  class="flex cursor-pointer items-start gap-3 rounded-[12px] border border-[#E2E7F4] bg-[#FAFBFF] px-3 py-2.5 transition hover:border-[#CFD7EE]"
                >
                  <input
                    :checked="isSelected(form.crmIntegrations, integration.label)"
                    type="checkbox"
                    class="mt-0.5 h-4 w-4 shrink-0 rounded border-[#C5CEE6] text-[#6F63FF] focus:ring-[#6F63FF]/30"
                    :disabled="isSubmitting"
                    @change="toggleChoice('crmIntegrations', integration.label)"
                  />
                  <span class="min-w-0">
                    <span class="block text-[13px] leading-[1.45] text-[#2F3754]">{{ integration.label }}</span>
                    <span class="mt-0.5 block text-[12px] leading-[1.35] text-[#677392]">{{ integration.description }}</span>
                  </span>
                </label>
              </div>
            </div>

            <div class="mt-4 rounded-[18px] border border-[#DFE5F3] bg-white p-4 sm:p-5">
              <h3 class="text-[17px] font-semibold text-[#1A2035]">Бронирование</h3>
              <div class="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                <label
                  v-for="integration in bookingIntegrationOptions"
                  :key="integration.label"
                  class="flex cursor-pointer items-start gap-3 rounded-[12px] border border-[#E2E7F4] bg-[#FAFBFF] px-3 py-2.5 transition hover:border-[#CFD7EE]"
                >
                  <input
                    :checked="isSelected(form.bookingIntegrations, integration.label)"
                    type="checkbox"
                    class="mt-0.5 h-4 w-4 shrink-0 rounded border-[#C5CEE6] text-[#6F63FF] focus:ring-[#6F63FF]/30"
                    :disabled="isSubmitting"
                    @change="toggleChoice('bookingIntegrations', integration.label)"
                  />
                  <span class="min-w-0">
                    <span class="block text-[13px] leading-[1.45] text-[#2F3754]">{{ integration.label }}</span>
                    <span class="mt-0.5 block text-[12px] leading-[1.35] text-[#677392]">{{ integration.description }}</span>
                  </span>
                </label>
              </div>
            </div>
          </section>

          <section class="rounded-[24px] border border-[#DBE1F0] bg-[linear-gradient(180deg,#FFFFFF_0%,#F7F9FF_100%)] p-5 sm:p-6">
            <p class="text-[14px] leading-[1.6] text-[#4D587A] sm:text-[15px]">
              Чем полнее заполнена анкета, тем точнее получится настройка ИИ-ассистента, интеграций и рабочих сценариев.
            </p>

            <button
              type="submit"
              class="mt-4 inline-flex h-[50px] w-full items-center justify-center rounded-[16px] border border-[#D4D9F4] bg-[linear-gradient(90deg,rgba(111,99,255,0.11)_0%,rgba(139,127,255,0.08)_100%)] text-[15px] font-semibold tracking-[-0.01em] text-[#2A2F45] shadow-[0_12px_28px_rgba(92,80,255,0.10)] transition hover:border-[#C5CCEF] hover:bg-[linear-gradient(90deg,rgba(111,99,255,0.15)_0%,rgba(139,127,255,0.11)_100%)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6F63FF]/35 disabled:cursor-not-allowed disabled:opacity-70"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Отправляем...' : 'Отправить' }}
            </button>
          </section>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

import BriefField from '~/components/company-brief/BriefField.vue'
import ServiceCard from '~/components/company-brief/ServiceCard.vue'
import { submitCompanyBrief } from '~/data/api'
import { ASSISTANT_CHANNELS, BOOKING_INTEGRATIONS, CRM_INTEGRATIONS, INDUSTRY_OPTIONS } from '~/data/companyBriefConfig'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const PHONE_PATTERN = /^[0-9+\-\s()]{6,30}$/
const PRICE_PATTERN = /^\d+(?:[.,]\d{1,2})?$/

const createEmptyService = () => ({ name: '', description: '', priceFrom: '', priceTo: '' })
const createEmptyServiceErrors = () => ({ name: '', description: '', priceFrom: '', priceTo: '' })

const basicFields = [
  { key: 'companyName', label: 'Название компании', helper: 'Как официально называется ваш бизнес или бренд.', placeholder: 'Например: ООО «Альфа Трейд»', required: true, autocomplete: 'organization', maxlength: 255 },
  { key: 'industry', label: 'Отрасль', helper: 'Выберите основное направление бизнеса.', placeholder: 'Выберите отрасль', required: true, as: 'select', options: INDUSTRY_OPTIONS },
  { key: 'subindustry', label: 'Подотрасль', helper: 'Уточните нишу или специализацию внутри отрасли.', placeholder: 'Например: детская стоматология', maxlength: 255 },
  { key: 'teamMembers', label: 'Члены команды', helper: 'Перечислите роли сотрудников, с кем будет взаимодействовать ассистент.', placeholder: 'Например: менеджер по продажам, администратор, поддержка', required: true, as: 'textarea', rows: 4, full: true, maxlength: 2000 },
  { key: 'shortDescription', label: 'Краткое описание', helper: 'Коротко расскажите о компании в 1–3 предложениях.', placeholder: 'Кто вы и чем помогаете клиентам', required: true, as: 'textarea', rows: 4, full: true, maxlength: 1200 },
  { key: 'fullDescription', label: 'Полное описание', helper: 'Опишите процессы, особенности, преимущества, аудиторию и географию.', placeholder: 'Чем подробнее описание, тем точнее сценарии ИИ-ассистента.', required: true, as: 'textarea', rows: 7, full: true, maxlength: 6000 },
]

const contactFields = [
  { key: 'primaryPhone', label: 'Основной номер телефона', helper: 'Номер для основных обращений клиентов.', placeholder: '+7 (999) 123-45-67', required: true, autocomplete: 'tel', maxlength: 64 },
  { key: 'secondaryPhone', label: 'Дополнительный номер телефона', helper: 'Резервный номер или номер другого отдела.', placeholder: '+7 (999) 765-43-21', autocomplete: 'tel-national', maxlength: 64 },
  { key: 'primaryEmail', label: 'Основной e-mail', helper: 'Главная почта компании для связи.', placeholder: 'hello@company.ru', required: true, type: 'email', autocomplete: 'email', maxlength: 254 },
  { key: 'supportEmail', label: 'E-mail поддержки', helper: 'Почта для обращений по действующим услугам.', placeholder: 'support@company.ru', type: 'email', autocomplete: 'email', maxlength: 254 },
  { key: 'salesEmail', label: 'E-mail продаж', helper: 'Почта для новых заявок и обращений.', placeholder: 'sales@company.ru', type: 'email', autocomplete: 'email', maxlength: 254 },
  { key: 'websiteUrl', label: 'URL веб-сайта', helper: 'Ссылка на основной сайт компании.', placeholder: 'https://company.ru', autocomplete: 'url', maxlength: 500 },
  { key: 'address', label: 'Адрес', helper: 'Юридический или фактический адрес компании.', placeholder: 'Улица, дом, офис', required: true, autocomplete: 'street-address', full: true, maxlength: 255 },
  { key: 'city', label: 'Город', helper: 'Основной город работы.', placeholder: 'Москва', required: true, autocomplete: 'address-level2', maxlength: 120 },
  { key: 'country', label: 'Страна', helper: 'Страна, в которой работает компания.', placeholder: 'Россия', required: true, autocomplete: 'country-name', maxlength: 120 },
  { key: 'timezoneName', label: 'Часовой пояс', helper: 'Нужен для корректной работы расписаний, ответов и интеграций.', placeholder: 'Например: Europe/Moscow', required: true, maxlength: 120 },
]

const crmIntegrationOptions = CRM_INTEGRATIONS.map((label) => ({
  label,
  description: 'Подключение CRM для передачи лидов, этапов и клиентских данных.',
}))

const bookingIntegrationOptions = BOOKING_INTEGRATIONS.map((label) => ({
  label,
  description: 'Синхронизация записей, расписаний и бронирований.',
}))

const form = reactive({
  companyName: '',
  industry: '',
  subindustry: '',
  teamMembers: '',
  shortDescription: '',
  fullDescription: '',
  primaryPhone: '',
  secondaryPhone: '',
  primaryEmail: '',
  supportEmail: '',
  salesEmail: '',
  address: '',
  city: '',
  country: '',
  websiteUrl: '',
  timezoneName: '',
  services: [createEmptyService()],
  assistantChannels: [],
  crmIntegrations: [],
  bookingIntegrations: [],
})

const errors = reactive({
  companyName: '',
  industry: '',
  subindustry: '',
  teamMembers: '',
  shortDescription: '',
  fullDescription: '',
  primaryPhone: '',
  secondaryPhone: '',
  primaryEmail: '',
  supportEmail: '',
  salesEmail: '',
  address: '',
  city: '',
  country: '',
  websiteUrl: '',
  timezoneName: '',
  assistantChannels: '',
  services: [createEmptyServiceErrors()],
})

const isSubmitting = ref(false)
const isSubmitAttempted = ref(false)
const submitSuccessMessage = ref('')
const submitErrorMessage = ref('')

const trimValue = (value) => String(value || '').trim()

const clearErrors = () => {
  Object.keys(errors).forEach((key) => {
    errors[key] = key === 'services' ? form.services.map(() => createEmptyServiceErrors()) : ''
  })
}

const isValidEmail = (value) => EMAIL_PATTERN.test(trimValue(value))
const isValidPhone = (value) => PHONE_PATTERN.test(trimValue(value))

const isValidUrl = (value) => {
  const normalized = trimValue(value)
  if (!normalized) return true

  try {
    const parsed = new URL(normalized)
    return parsed.protocol === 'http:' || parsed.protocol === 'https:'
  } catch {
    return false
  }
}

const parsePrice = (value) => {
  const normalized = trimValue(value).replace(/\s+/g, '').replace(',', '.')
  if (!normalized) return null
  if (!PRICE_PATTERN.test(normalized)) return Number.NaN
  return Number(normalized)
}

const validateForm = () => {
  clearErrors()

  basicFields.forEach((field) => {
    if (field.required && !trimValue(form[field.key])) {
      errors[field.key] = 'Это поле обязательно для заполнения.'
    }
  })

  contactFields.forEach((field) => {
    if (field.required && !trimValue(form[field.key])) {
      errors[field.key] = 'Это поле обязательно для заполнения.'
    }
  })

  if (trimValue(form.primaryPhone) && !isValidPhone(form.primaryPhone)) {
    errors.primaryPhone = 'Введите телефон в формате +7 (999) 123-45-67.'
  }

  if (trimValue(form.secondaryPhone) && !isValidPhone(form.secondaryPhone)) {
    errors.secondaryPhone = 'Введите корректный дополнительный номер.'
  }

  if (trimValue(form.primaryEmail) && !isValidEmail(form.primaryEmail)) {
    errors.primaryEmail = 'Введите корректный e-mail.'
  }

  if (trimValue(form.supportEmail) && !isValidEmail(form.supportEmail)) {
    errors.supportEmail = 'Введите корректный e-mail поддержки.'
  }

  if (trimValue(form.salesEmail) && !isValidEmail(form.salesEmail)) {
    errors.salesEmail = 'Введите корректный e-mail продаж.'
  }

  if (trimValue(form.websiteUrl) && !isValidUrl(form.websiteUrl)) {
    errors.websiteUrl = 'Введите корректный URL (например, https://company.ru).'
  }

  errors.services = form.services.map(() => createEmptyServiceErrors())
  form.services.forEach((service, index) => {
    if (!trimValue(service.name)) errors.services[index].name = 'Укажите наименование услуги.'
    if (!trimValue(service.description)) errors.services[index].description = 'Добавьте описание услуги.'

    const priceFrom = parsePrice(service.priceFrom)
    const priceTo = parsePrice(service.priceTo)

    if (trimValue(service.priceFrom) && Number.isNaN(priceFrom)) {
      errors.services[index].priceFrom = 'Укажите корректную цену.'
    }

    if (trimValue(service.priceTo) && Number.isNaN(priceTo)) {
      errors.services[index].priceTo = 'Укажите корректную цену.'
    }

    if (!Number.isNaN(priceFrom) && !Number.isNaN(priceTo) && priceFrom !== null && priceTo !== null && priceFrom > priceTo) {
      errors.services[index].priceTo = 'Цена "до" должна быть больше или равна цене "от".'
    }
  })

  if (!form.assistantChannels.length) {
    errors.assistantChannels = 'Выберите хотя бы один канал ассистента.'
  }

  const hasFlatErrors = Object.keys(errors).some((key) => key !== 'services' && Boolean(errors[key]))
  const hasServiceErrors = errors.services.some((serviceErrors) => Object.values(serviceErrors).some(Boolean))

  return !hasFlatErrors && !hasServiceErrors
}

const buildPayload = () => ({
  company_name: trimValue(form.companyName),
  industry: trimValue(form.industry),
  subindustry: trimValue(form.subindustry),
  team_members: trimValue(form.teamMembers),
  short_description: trimValue(form.shortDescription),
  full_description: trimValue(form.fullDescription),
  primary_phone: trimValue(form.primaryPhone),
  secondary_phone: trimValue(form.secondaryPhone),
  primary_email: trimValue(form.primaryEmail),
  support_email: trimValue(form.supportEmail),
  sales_email: trimValue(form.salesEmail),
  address: trimValue(form.address),
  city: trimValue(form.city),
  country: trimValue(form.country),
  website_url: trimValue(form.websiteUrl),
  timezone_name: trimValue(form.timezoneName),
  services: form.services.map((service) => ({
    name: trimValue(service.name),
    description: trimValue(service.description),
    price_from: trimValue(service.priceFrom).replace(',', '.'),
    price_to: trimValue(service.priceTo).replace(',', '.'),
  })),
  assistant_channels: [...form.assistantChannels],
  crm_integrations: [...form.crmIntegrations],
  booking_integrations: [...form.bookingIntegrations],
})

const findFirstErrorText = (value) => {
  if (!value) return ''
  if (Array.isArray(value)) return findFirstErrorText(value.find(Boolean))
  if (typeof value === 'object') {
    for (const item of Object.values(value)) {
      const text = findFirstErrorText(item)
      if (text) return text
    }
  }
  return typeof value === 'string' ? value : ''
}

const applyBackendErrors = (backendErrors) => {
  if (!backendErrors || typeof backendErrors !== 'object') return

  const fieldMap = {
    company_name: 'companyName',
    industry: 'industry',
    subindustry: 'subindustry',
    team_members: 'teamMembers',
    short_description: 'shortDescription',
    full_description: 'fullDescription',
    primary_phone: 'primaryPhone',
    secondary_phone: 'secondaryPhone',
    primary_email: 'primaryEmail',
    support_email: 'supportEmail',
    sales_email: 'salesEmail',
    address: 'address',
    city: 'city',
    country: 'country',
    website_url: 'websiteUrl',
    timezone_name: 'timezoneName',
    assistant_channels: 'assistantChannels',
  }

  Object.entries(fieldMap).forEach(([backendKey, localKey]) => {
    const text = findFirstErrorText(backendErrors[backendKey])
    if (text) errors[localKey] = text
  })

  if (Array.isArray(backendErrors.services)) {
    errors.services = form.services.map(() => createEmptyServiceErrors())
    backendErrors.services.forEach((serviceErrors, index) => {
      if (!serviceErrors || !errors.services[index]) return
      errors.services[index].name = findFirstErrorText(serviceErrors.name)
      errors.services[index].description = findFirstErrorText(serviceErrors.description)
      errors.services[index].priceFrom = findFirstErrorText(serviceErrors.price_from)
      errors.services[index].priceTo = findFirstErrorText(serviceErrors.price_to)
    })
  }
}

const resetForm = () => {
  Object.keys(form).forEach((key) => {
    if (Array.isArray(form[key])) {
      form[key] = key === 'services' ? [createEmptyService()] : []
    } else {
      form[key] = ''
    }
  })
  clearErrors()
}

const handleSubmit = async () => {
  isSubmitAttempted.value = true
  submitSuccessMessage.value = ''
  submitErrorMessage.value = ''

  if (!validateForm()) {
    submitErrorMessage.value = 'Проверьте обязательные поля и исправьте ошибки формы.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await submitCompanyBrief(buildPayload())
    submitSuccessMessage.value = response?.message || 'Анкета успешно отправлена. Спасибо!'
    resetForm()
    isSubmitAttempted.value = false

    if (typeof window !== 'undefined') {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  } catch (error) {
    applyBackendErrors(error?.payload?.errors)
    submitErrorMessage.value =
      error?.payload?.message || 'Не удалось отправить анкету. Попробуйте еще раз.'
  } finally {
    isSubmitting.value = false
  }
}

const addService = () => {
  form.services.push(createEmptyService())
  errors.services.push(createEmptyServiceErrors())
}

const removeService = (index) => {
  if (form.services.length === 1) {
    form.services[0] = createEmptyService()
    errors.services = [createEmptyServiceErrors()]
    return
  }

  form.services.splice(index, 1)
  errors.services.splice(index, 1)
  revalidateIfNeeded()
}

const handleServiceUpdate = (index, payload) => {
  if (!form.services[index]) return
  form.services[index][payload.field] = payload.value
  revalidateIfNeeded()
}

const isSelected = (collection, value) => collection.includes(value)

const toggleChoice = (field, value) => {
  const collection = form[field]
  const index = collection.indexOf(value)
  if (index >= 0) collection.splice(index, 1)
  else collection.push(value)
  revalidateIfNeeded()
}

const revalidateIfNeeded = () => {
  if (isSubmitAttempted.value) validateForm()
}

const setMeta = (name, content) => {
  if (!content || typeof document === 'undefined') return

  let element = document.head.querySelector(`meta[name="${name}"]`)
  if (!element) {
    element = document.createElement('meta')
    element.setAttribute('name', name)
    document.head.appendChild(element)
  }

  element.setAttribute('content', content)
}

onMounted(() => {
  document.title = 'Анкета для компаний | AI4Business'
  setMeta('description', 'Анкета для компаний AI4Business: заполните данные о бизнесе, услугах, каналах и интеграциях для точной настройки ИИ-ассистента.')
})
</script>
