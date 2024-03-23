// globalMixin.js

export default {
  methods: {
    redirect(endpoint) {
      // Your global method logic here
      this.$router.push(endpoint)
    }
  }
}