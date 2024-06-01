<script setup>
import TravelGlobe from './TravelGlobe.vue';
</script>

<template>
  <div class="content-container">
    <div class="recipe-header header-font">
      Travel
    </div>
    <div class="globe-container">
      <TravelGlobe :visitedCountries="visitedCountries"/>
    </div>
    <div class="recipe-header header-font">
      By Country Name (A-Z)
    </div>
    <div>
      <div v-for="country in visitedCountries.sort()" @click="redirect(`/travel/${country}`)">
        {{ country }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TravelGlobe',
  components: {
    TravelGlobe
  },
  data() {
    return {
      visitedCountries: ['Bali', 'France', 'Australia', 'Spain', 'Portugal', 'United Kingdom']
    };
  }
}
</script>

<style>
.globe-container {
  text-align: center;
  height: 100%;
}
</style>