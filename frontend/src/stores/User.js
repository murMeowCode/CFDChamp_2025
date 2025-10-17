import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUse = defineStore('us', () => {

    const FIO = ref('Иванов Иван Иваныч');
    const DateBirthday = ref('05.05.2000');
    const NickName = ref('IVAN');
    const PersonalPhoto = ref('TunTunTun.jpg');
    const Level = ref(10);

    const Profession = ref('Разработчик');
    const Quote = ref('Живи, люби, твори');
    const Email = ref('ivanov@example.com');
    const Phone = ref('+7 123 456 78 90');
    const BurthDay = ref('2000-05-05');
    const selectedOption = ref('option1');
    const Address = ref('г. Москва, Россия');
    const AboutMe = ref('Люблю программировать и учиться новому.');

    const contacts = ref([
  { type: 'email', value: Email.value },
  { type: 'tel', value: Phone.value }
]);

  return { FIO, DateBirthday, NickName, PersonalPhoto, Level, Profession, Quote, Email, Phone, BurthDay, selectedOption, Address, AboutMe, contacts }
})
