<template>
    <b-alert variant="success"
             :show="dismissCountDown"
             @dismissed="dismissCountDown=0"
             @dismiss-count-down="countDownChanged"><slot></slot>

      <b-progress
        variant="success"
        class="mt-2"
        :max="dismissSecs"
        :value="dismissCountDown"
        height="4px">

      </b-progress>
    </b-alert>
</template>

<script>
export default Vue.component('Alert-box', {

  name: 'Alert-box',
  data() {
    return {
      dismissSecs: 10,
      dismissCountDown: 10,
      text: "",
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert(message) {
      this.message = message;
      this.dismissCountDown = this.dismissSecs;
    },
  },
});
</script>
