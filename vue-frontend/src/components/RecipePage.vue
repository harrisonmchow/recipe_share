<script setup>
import axios from 'axios';
import NotFoundPage from "./404page.vue"
</script>

<template>
  <div v-if="found && recipeData">
    <div class="content-container">
      <div class="recipe-header header-font">
        {{ recipeData.title }}
      </div>
      <v-container class="">
        <v-row no-gutters>
          <v-col cols="12" sm="4">
            <v-sheet class="ma-2">
              <div class="recipe-info">
                <div>Cuisine: {{ recipeData.cuisine.charAt(0).toUpperCase() + recipeData.cuisine.slice(1) }}</div>
                <div>Total Time: {{ formatTime(recipeData.time) }} <v-icon icon="mdi-timer-outline"
                    size="small"></v-icon></div>
                <div>Difficulty: {{ recipeData.difficulty }}
                  <v-icon v-for="n in difficultyIcons(recipeData.difficulty)" :key="`icon_${n}`" icon="mdi-chef-hat"
                    size="small"></v-icon>
                </div>
              </div>
              <div class="recipe-description">
                {{ recipeData.description }}
              </div>
              <div class="ingredients">
                <div class="ingredients-header">
                  You'll need the following:
                </div>
                <ul class="item">
                  <li v-for="ingredient in recipeData.ingredients" :key="ingredient">{{ ingredient }}</li>
                </ul>
              </div>
            </v-sheet>
          </v-col>
          <v-divider vertical class="border-opacity-25"></v-divider>
          <v-col cols="12" sm="8">
            <v-sheet class="ma-2 instructions-container">
              <div class="instructions-header">
                Instructions (Click here for the video
                  <v-icon icon="mdi-open-in-new" size="small" @click="openLink(recipeData.link)"></v-icon>)
              </div>
              <ol class="styled-list">
                <li v-for="instruction, index in recipeData.instructions" :key="`instru_${index}`">{{ instruction }}
                </li>
              </ol>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
  <div v-else>
    <NotFoundPage />
  </div>
</template>

<script>
export default {
  name: 'Recipe Page',
  components: {
    NotFoundPage
  },
  data() {
    return {
      recipeData: undefined,
      found: true,
      icons: 0,
    }
  },
  mounted() {
    const id = this.$route.query.id;
    console.log("ID:", id);
    this.fetchRecipe(id);
  },
  methods: {
    async fetchRecipe(id) {
      try {
        const backendUrl = import.meta.env.VITE_DB_HOST;
        const response = await axios.get(`${backendUrl}/recipes?id=${id}`);
        this.recipeData = response.data;
      } catch (err) {
        console.log(err)
        this.found = false;
      }
    },
    formatTime(minutes) {
      const hours = Math.floor(minutes / 60);
      if (hours === 0) {
        return `${minutes} min`;
      }
      const remainingMinutes = minutes % 60;
      return `${hours} hr ${remainingMinutes} min`;
    },
    difficultyIcons(difficulty) {
      if (difficulty === 'Beginner') {
        return 1;
      } else if (difficulty === 'Intermediate') {
        return 2;
      } else if (difficulty === 'Chef') {
        return 3;
      }
      return 0;
    },
    openLink(url) {
      window.open(url, '_blank');
    }
  },
};
</script>

<style>
.recipe-header {
  font-size: 40pt;
  text-align: center;
  color: rgb(0, 0, 0);
  padding-top: 25px;
  padding-bottom: 10px;
}

.recipe-description {
  font-size: 12pt;
  margin: 10px 0px;
  font-style: italic;
}

.recipe-info {
  font-size: 12pt;
  font-weight: bold;
  margin: 10px 0px;
}

.ingredients {
  font-size: 12pt;
  /* padding-bottom: 5pt; */
  margin: 20px 0px;
}

.ingredients-header {
  font-weight: bold;
}

.instructions-container {
  padding-left: 5%;
}

.instructions-header {
  /* font-weight: bold; */
  font-size: 15pt;
  margin-bottom: 10px;
}

ol {
  list-style: none;
}

styled-list {
  counter-reset: list-counter;
  padding-left: 0;
}

.styled-list li {
  counter-increment: list-counter;
  position: relative;
  padding-left: 2.5em;
  /* margin-bottom: 0.5em; */
  margin: 10px 0px
    /* Font for list items */
}

.styled-list li::before {
  content: counter(list-counter) ".";
  position: absolute;
  left: 0;
  bottom: -3px;
  /* font-family: 'Courier New', Courier, monospace; */
  font-family: 'Rubik Mono One', monospace;
  /* Font for numbers */
  font-size: 1.2em;
}
</style>