<template>
  <Notivue v-slot="item">
    <Notification
      v-if="item && item.type"
      :item="item"
      :theme="item.type"
      class="custom-notification"
    >
      <div class="notification-content">
        <div class="notification-icon">
          <i v-if="item.type === 'success'" class="pi pi-check-circle"></i>
          <i v-else-if="item.type === 'error'" class="pi pi-times-circle"></i>
          <i v-else-if="item.type === 'warning'" class="pi pi-exclamation-triangle"></i>
          <i v-else-if="item.type === 'info'" class="pi pi-info-circle"></i>
          <i v-else-if="item.type === 'promise'" class="pi pi-spinner pi-spin"></i>
        </div>
        <div class="notification-text">
          <div class="notification-title">{{ item.title || '' }}</div>
          <div class="notification-message">{{ item.message || '' }}</div>
        </div>
      </div>
    </Notification>
  </Notivue>
</template>

<script setup>
import { Notivue, Notification } from 'notivue'
</script>

<style scoped></style>
