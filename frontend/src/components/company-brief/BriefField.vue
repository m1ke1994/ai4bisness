<template>
  <div class="space-y-2">
    <label
      :for="id"
      class="block text-[14px] font-medium leading-[1.3] tracking-[-0.01em] text-[#1B2138] sm:text-[15px]"
    >
      {{ label }}
      <span v-if="required" class="text-[#B42318]">*</span>
    </label>

    <component
      :is="componentType"
      :id="id"
      :value="modelValue"
      :type="inputType"
      :placeholder="placeholder"
      :rows="rows"
      :maxlength="maxlength"
      :autocomplete="autocomplete"
      :inputmode="inputmode"
      :disabled="disabled"
      class="w-full rounded-[14px] border bg-white px-4 py-3 text-[15px] leading-[1.35] tracking-[-0.01em] text-[#171C31] transition placeholder:text-[#8D95B2] focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:bg-[#F6F7FC]"
      :class="error ? 'border-[#E19BA5] focus:border-[#D7485E] focus:ring-[#D7485E]/20' : 'border-[#D7DEEE] focus:border-[#6F63FF] focus:ring-[#6F63FF]/20'"
      @input="handleInput"
      @change="handleInput"
      @blur="$emit('blur')"
    >
      <option
        v-if="isSelect && placeholder"
        disabled
        value=""
      >
        {{ placeholder }}
      </option>

      <option
        v-for="option in options"
        :key="option"
        :value="option"
      >
        {{ option }}
      </option>
    </component>

    <p
      class="text-[12px] leading-[1.4] text-[#667085] sm:text-[13px]"
      :class="error ? 'text-[#B42318]' : 'text-[#667085]'"
    >
      {{ error || helper }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    required: true,
  },
  helper: {
    type: String,
    required: true,
  },
  placeholder: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
  as: {
    type: String,
    default: 'input',
  },
  type: {
    type: String,
    default: 'text',
  },
  rows: {
    type: Number,
    default: 4,
  },
  options: {
    type: Array,
    default: () => [],
  },
  autocomplete: {
    type: String,
    default: 'off',
  },
  inputmode: {
    type: String,
    default: undefined,
  },
  maxlength: {
    type: [String, Number],
    default: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'blur'])

const isSelect = computed(() => props.as === 'select')
const componentType = computed(() => (props.as === 'textarea' ? 'textarea' : (isSelect.value ? 'select' : 'input')))
const inputType = computed(() => (props.as === 'input' ? props.type : undefined))

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>
