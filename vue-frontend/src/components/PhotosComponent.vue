<script setup lang="">
  import { filename } from 'pathe/utils'
  const glob = import.meta.glob('@/assets/monthly_photos/*.JPG', { eager: true })
  const images = Object.fromEntries(
    Object.entries(glob).map(([key, value]) => [filename(key), value.default])
  )
</script>

<template>
  <div>
    <v-container>
      <v-row>
        <v-col v-for="(image, index) in imagesFormatted" :key="image" class="monthly-container" cols="12" sm="6" md="4" lg="3">
          <img :src="images[`${image}`]" alt="Image" class="cropped-image" />
          <p><strong>{{ `${this.months[index].toUpperCase()}:` }}</strong> {{ this.captions[index] }}</p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="">
export default {
  props: ['year', 'months', 'captions'], // Corrected props definition
  computed: {
    imagesFormatted() {
      // Access props with 'this' keyword
      return this.months.map(month => {
        return `${month}${this.year}`
      });
    }
  }
}
</script>

<style>
  .cropped-image {
    width: 100%;
    height: 85%;
    object-fit: cover; /* Apply cropping to maintain aspect ratio */
  }
  .monthly-container {
    text-align: center;
  }
</style>

