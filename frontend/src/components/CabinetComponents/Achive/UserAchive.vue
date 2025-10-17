<template>
    <div class="UserAchivesMainPanel">
        <div class="Photo">
            <img :src="ph2" alt=""></img>
        </div>
        <div class="AchiveText">
            {{ Achive.text }}
        </div>
        <div class="AchiveProcent">
            {{ Achive.procent }} %
        </div>
    </div>
</template>

<script setup>

import { ref, defineProps } from 'vue';
import ph2 from '@/components/CabinetComponents/img/TunTunTun.jpg'
const props = defineProps({
    Achive: Object,
})


</script>

<style scoped>
.UserAchivesMainPanel {

  display: flex;
  align-items: center;
  border-style: solid;
  border-radius: 25px;
  border-width: 5px;
  margin-bottom: 10px;
  height: 70px;
  padding: 0 15px;
  box-sizing: border-box;
  gap: 15px;
  background: #f9fafb;
}

.Photo img {
  border-radius: 50%;
  width: 50px;
  height: 50px;
  object-fit: cover;
}

/* Контейнер для текста — занимает оставшееся пространство и центрируется */
.AchiveText {
  flex: 1;
  text-align: center;
    font-size: 10pt;
  font-weight: 600;
  color: #2c3e50;
  user-select: none;
}

/* Контейнер процентов — фиксированного размера */
.AchiveProcent {
  min-width: 55px;
  height: 55px;
  line-height: 50px;
  background-color: #42b983;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  border-radius: 50%;
  text-align: center;
  user-select: none;
  box-shadow: 0 2px 8px rgba(66, 185, 131, 0.5);
}
</style>
