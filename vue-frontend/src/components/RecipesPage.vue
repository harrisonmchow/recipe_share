<script setup>
  import { ref } from 'vue'

  const variants = ['elevated', 'flat', 'elevated', 'elevated', 'elevated']
  const color = ref('indigo')

  const filters = ['difficulty', 'cuisine', 'our favourites']
</script>

<template>
  <div class="content-container">
    <div class="recipes-header header-font">
      Recipes
    </div>
    <div class="subtext">
      Coming from recipe books, Tiktok, or simply improvisations, here are some of our favourite recipes we've cooked up for ourselves. Browse by cuisine, difficulty, or simply by our favourites. 
      <br/>
      Enjoy!
    </div>
    <v-container class="recipe-card-container">
      <v-row align="center" justify="start">
      <v-col
        v-for="(variant, i) in variants"
        :key="i"
        cols="4"
      >
        <v-card
          :color="color"
          :variant="variant"
          class="mx-auto"
        >
          <v-card-item>
            <div>
              <div class="text-overline mb-1">
                {{ variant }}
              </div>
              <div class="text-h6 mb-1">
                Headline
              </div>
              <div class="text-caption">Greyhound divisely hello coldly fonwderfully</div>
            </div>
          </v-card-item>

          <v-card-actions>
            <v-btn>
              Button
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'RecipePage'
}
</script>

<style>
  .recipes-header {
    font-size: 40pt;
    text-align: center;
    color: rgb(0, 0, 0);
    padding: 25px 0px
  }
  .subtext {
    font-size: 20pt;
    text-align: center;
    margin: 0 20%;
  }
  .recipe-card-container {
    /* background-color: blue; */
    margin-top: 40px;
  }
</style>