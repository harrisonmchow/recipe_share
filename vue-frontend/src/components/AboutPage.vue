<script setup>
import YearDivider from './YearDivider.vue'
import PhotosComponent from './PhotosComponent.vue'
</script>

<template>
    <div class="image-container">
      <div class="about-header header-font">
        About
      </div>
    </div>
    <div class="text-container">
      <p>
        This website is dedicated to my pookie, and one of the coolest people I know. You are an absolute blessing to everyone in your life, and words cannot express how grateful I am to share this earth with you. I want the world to see how awesome and talented you are, and everyone should take a page out of your book on how to be such a magical human being.
      </p>
      <br/>
      <p>
        Below are some of my favourite memories since we've started dating. Let's take a trip down memory lane.
      </p>
    </div>
    <YearDivider year="2022"/>
    <PhotosComponent year="2022" :months="dict2022.months" :captions="dict2022.captions"/>
    <YearDivider year="2023"/>
    <PhotosComponent year="2023" :months="dict2023.months" :captions="dict2023.captions"/>
    <YearDivider year="2024"/>
    <PhotosComponent year="2024" :months="dict2024.months" :captions="dict2024.captions"/>
</template>
  
<script>
  export default {
    name: 'AboutPage',
    components: {
      PhotosComponent,
      YearDivider
    },
    data() {
      return {
        years: [
          '2022', '2023', '2024'
        ],
        dict2022: {
          months: [
            'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec'
          ],
          captions: [
            'test'
          ]
        },
        dict2023: {
          months: [
            'jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec'
          ],
        },
        dict2024: {
          months: [
            'jan', 'feb', 'march'
          ],
        }
      };
    },
  }
</script>
  
<style>
  .image-container {
    margin-top: 4%;
    min-height: 400px;
    max-height: 500px;
    width: 100vw;
    background-image: url('../assets/about_header_photo.JPG');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    display: grid;
    place-items: center;
  }

  .about-header {
    font-size: 50pt;
    text-align: center;
    color: rgb(255, 255, 255);
  }

  .text-container {
    /* background-color: blue; */
    padding: 25px 0px;
    margin: 0px 5%;
  }
</style>
  