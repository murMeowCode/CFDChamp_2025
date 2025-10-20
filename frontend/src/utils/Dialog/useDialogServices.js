// composables/useDialogServices.js
import DialogUpdateProfileEmailPhone from '@/components/DialogComponents/DialogUpdateProfileEmailPhone.vue'
import { useDialog } from 'primevue/usedialog'

export const useDialogServices = () => {
  const dialog = useDialog()

  function showUpdateEmailPhone() {
    dialog.open(DialogUpdateProfileEmailPhone,{
      props: {
        style: {
          width: "40vw",
          backgroundColor: "var(--color-bg)",
          border: "none",
          color: "var(--color-text)",
        },
        breakpoints: {
          "960px": "75vw",
          "640px": "80vw",
        },
        modal: true,
        draggable: false,
      },
    })
  }

  return {
    showUpdateEmailPhone,
  }
}
