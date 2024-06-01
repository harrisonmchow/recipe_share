<template>
    <div class="d-flex flex-wrap justify-space-between container">
      <v-sheet class="ma-2 pa-2">
        <div class="square-container cursor-pointer" @click="redirect('/travel')">
          <img src="../assets/earth.png" alt="Travel" class="circular-image">
          <div style="text-align: center; padding: 5px">Travel</div>
        </div>
      </v-sheet>
      <v-sheet class="ma-2 pa-2">
        <div class="square-container cursor-pointer" @click="redirect('/music')">
          <img src="../assets/sade.png" alt="Music" class="rotate circular-image">
          <div style="text-align: center; padding: 5px">Music</div>
        </div>
      </v-sheet>
      <v-sheet class="ma-2 pa-2">
        <div class="square-container cursor-pointer" @click="redirect('/recipes')">
          <img src="../assets/pan.png" alt="Recipes" class="circular-image">
          <div style="text-align: center; padding: 5px;">Recipes</div>
        </div>
      </v-sheet>
    </div>
</template>

<script>
export default {
  name: 'LoadingPage'
}
</script>

<style>
/* Define the animation */
@keyframes rotate360 {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* Apply the animation to the image */
.rotate {
  animation: rotate360 5s linear infinite;
  /* Adjust duration as needed */
}

.square-container {
  width: 100%;
  /* Adjust width as needed */
  max-width: 220px;
  position: relative;
  overflow: hidden;
}

.square-container img {
  width: 100%;
  /* Make the image fill the container horizontally */
  height: auto;
  /* Allow the height to adjust proportionally */
  display: block;
}

.circular-image {
  border-radius: 222px;
  background: url(<path-to-image>) lightgray 50% / cover no-repeat;
}
</style>