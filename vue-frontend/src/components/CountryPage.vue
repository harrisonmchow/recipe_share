<script setup>
import NotFoundPage from "./404page.vue"
import axios from "axios";
import globalMixin from '../globalMixin.js';
</script>

<template>
  <div v-if="found" class="content-container">
    <div class="recipe-header header-font">
      {{ country }}
    </div>
    <div class="country-description">
      {{ countryData.description }}
    </div>
    <div v-if="hasToken === true" style="text-align: center; margin-top: 5px;">
      <v-btn color="success" @click="console.log('New guide');">
        Add a new guide
      </v-btn>
    </div>
    <v-container v-for="guide, index in countryData.guides" class="guide-container" :key="`guide-${index}`">
      <v-row class="d-flex align-center">
        <v-col cols="12" md="8" class="d-flex align-center justify-center">
          <div>
            <div class="city-header">
              {{ guide.state ? `${guide.city} (${guide.state})` : guide.city }}
            </div>
            <div class="city-description">
              {{ guide.description }}
            </div>
            <div class="city-subheading">
              Accomodation
            </div>
            <div>
              We stayed at <a :href="guide.accomodation.link" target="_blank" rel="noopener noreferrer">{{
    guide.accomodation.name }} for {{ guide.length }} nights</a>.
              It cost a total of ~{{ Math.round(guide.accomodation.price) }} AUD (~{{
    Math.round(guide.accomodation.price /
      guide.length) }} per night)
            </div>
            <div>
              Notes about our accomodation. How do we rate the stay out of 5.
            </div>
            <div class="city-subheading">
              Activities
            </div>
            <div v-for="activity in guide.activities">
              {{ activity }}
              <div class="city-notes">
                - Some notes on the activity
              </div>
            </div>
            <div class="city-subheading">
              Food and Drink
            </div>
            <div v-for="place in guide.food">
              {{ place }}
              <div class="city-notes">
                - Some notes on the place
              </div>
            </div>
            <div class="city-subheading">
              Final notes
            </div>
            <div>
              {{ guide.finalNotes }}
            </div>
          </div>
        </v-col>
        <v-col cols="12" md="4" class="d-flex align-center justify-center">
          <v-carousel hide-delimiters show-arrows="hover">
            <v-carousel-item v-for="(item, i) in guide.photos" :key="i" :src="item" cover class="image"></v-carousel-item>
          </v-carousel>
        </v-col>
      </v-row>
    </v-container>
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
  mixins: [globalMixin],
  data() {
    return {
      countryData: undefined,
      found: false,
      hasToken: false,
    }
  },
  computed: {
    country() {
      return this.$route.params.country;
    }
  },
  mounted() {
    this.fetchCountry();
    this.checkForToken();
  },
  methods: {
    async fetchCountry() {
      try {
        const backendUrl = import.meta.env.VITE_DB_HOST;
        const response = await axios.get(`${backendUrl}/travel?country=${this.country}`);
        this.countryData = response.data.data;
        console.log(response.data.data);
        this.found = true;
      } catch (err) {
        console.log(err);
      }
    }
  }
}  
</script>

<style>
.country-description {
  font-size: 17pt;
  text-align: center;
  font-style: italic;
  padding-bottom: 25px;
}

.city-header {
  font-size: 22pt;
  padding: 10px 0px;
  font-weight: bold;
}

.city-description {
  font-size: 12pt;
}

.guide-container {
  margin: 0px 4%;
  text-align: left;
}

.city-subheading {
  font-size: 15pt;
  padding: 10px 0px;
  font-weight: bold;
}

.city-notes {
  font-size: 9pt;
  margin-left: 5px;
}

.image {
  width: 100%;
  height: auto;
}
</style>