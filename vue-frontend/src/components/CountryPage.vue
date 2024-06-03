<script setup>
import NotFoundPage from "./404page.vue"
</script>

<template>
  <div v-if="found" class="content-container">
    <div class="recipe-header header-font">
      {{ country }}
    </div>
  </div>
  <div v-else>
    <NotFoundPage />
  </div>
</template>

<script>
export default {
  name: 'Country Page',
  components: {
    NotFoundPage
  },
  data() {
    return {
      countryData: undefined,
      found: true,
    }
  },
  computed: {
    country() {
      console.log(this.$route.params.country);
      return this.$route.params.country;
    }
  },
  mounted() {
    console.log(this.country)
  },
  methods: {
    async fetchCountry() {

    }
  }
}  
</script>