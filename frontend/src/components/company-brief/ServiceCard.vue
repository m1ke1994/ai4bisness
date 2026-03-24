<template>
  <article class="rounded-[20px] border border-[#DCE2F1] bg-white p-4 shadow-[0_8px_24px_rgba(17,24,39,0.05)] sm:p-5">
    <div class="flex items-center justify-between gap-4">
      <h3 class="text-[16px] font-semibold tracking-[-0.02em] text-[#181C2E] sm:text-[18px]">
        Услуга {{ index + 1 }}
      </h3>

      <button
        type="button"
        class="inline-flex h-[34px] items-center justify-center rounded-[10px] border border-[#E6E9F6] px-3 text-[13px] font-medium text-[#4A5578] transition hover:border-[#D5DBEF] hover:bg-[#F8F9FF] disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="!canRemove || disabled"
        @click="$emit('remove')"
      >
        Удалить
      </button>
    </div>

    <div class="mt-4 grid grid-cols-1 gap-4">
      <BriefField
        :id="`service-name-${index}`"
        :model-value="service.name"
        label="Наименование услуги"
        helper="Как называется услуга, которую вы предлагаете клиентам."
        placeholder="Например: Настройка CRM"
        :error="errors.name || ''"
        :required="true"
        :disabled="disabled"
        autocomplete="organization-title"
        maxlength="255"
        @update:model-value="(value) => $emit('update', { field: 'name', value })"
        @blur="$emit('blur', { field: 'name' })"
      />

      <BriefField
        :id="`service-description-${index}`"
        :model-value="service.description"
        label="Описание услуги"
        helper="Кратко поясните, что получает клиент и в чем ценность этой услуги."
        placeholder="Что входит в услугу, какие задачи решает"
        :error="errors.description || ''"
        :required="true"
        as="textarea"
        :rows="4"
        :disabled="disabled"
        maxlength="2000"
        @update:model-value="(value) => $emit('update', { field: 'description', value })"
        @blur="$emit('blur', { field: 'description' })"
      />
    </div>

    <div class="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
      <BriefField
        :id="`service-price-from-${index}`"
        :model-value="service.priceFrom"
        label="Цена от"
        helper="Минимальная стоимость или стартовая цена."
        placeholder="Например: 15000"
        :error="errors.priceFrom || ''"
        :disabled="disabled"
        inputmode="decimal"
        maxlength="64"
        @update:model-value="(value) => $emit('update', { field: 'priceFrom', value })"
        @blur="$emit('blur', { field: 'priceFrom' })"
      />

      <BriefField
        :id="`service-price-to-${index}`"
        :model-value="service.priceTo"
        label="Цена до"
        helper="Максимальная стоимость, если услуга продается в диапазоне."
        placeholder="Например: 45000"
        :error="errors.priceTo || ''"
        :disabled="disabled"
        inputmode="decimal"
        maxlength="64"
        @update:model-value="(value) => $emit('update', { field: 'priceTo', value })"
        @blur="$emit('blur', { field: 'priceTo' })"
      />
    </div>
  </article>
</template>

<script setup>
import BriefField from '~/components/company-brief/BriefField.vue'

defineProps({
  service: {
    type: Object,
    required: true,
  },
  errors: {
    type: Object,
    default: () => ({}),
  },
  index: {
    type: Number,
    required: true,
  },
  canRemove: {
    type: Boolean,
    default: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update', 'remove', 'blur'])
</script>
