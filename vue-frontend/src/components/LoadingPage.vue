<template>
  <v-sheet class="d-flex flex-row mt-16 mb-6 bg-surface-variant flex-nowrap justify-space-around">
    <v-sheet class="d-flex flex-column justify-center align-center">
      <v-sheet class="rotating-image square-container ma-2 pa-2 d-flex flex-column justify-center align-center align-self-center">
        <img src="../assets/sade.png" alt="Rotating Image" class="rotate">
      </v-sheet>
      <v-sheet class="ma-2 pa-2">Clothing</v-sheet>
    </v-sheet>
    <v-sheet class="d-flex flex-column justify-center align-center">
      <v-sheet class="rotating-image square-container ma-2 pa-2 d-flex flex-column justify-center align-center">
        <img src="../assets/sade.png" alt="Rotating Image" class="">
      </v-sheet>
      <v-sheet class="ma-2 pa-2">Music</v-sheet>
    </v-sheet>
    <v-sheet class="d-flex flex-column justify-center align-center">
      <v-sheet class="rotating-image square-container ma-2 pa-2 d-flex flex-column justify-center align-center">
        <img src="../assets/sade.png" alt="Rotating Image" class="">
      </v-sheet>
      <v-sheet class="ma-2 pa-2">Food</v-sheet>
    </v-sheet>
  </v-sheet>
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
    animation: rotate360 5s linear infinite; /* Adjust duration as needed */
  }

  .square-container {
    width: 100%; /* Adjust width as needed */
    max-width: 300px;
    position: relative;
    overflow: hidden;
  }

  .square-container img {
    width: 100%; /* Make the image fill the container horizontally */
    height: auto; /* Allow the height to adjust proportionally */
    display: block;
  }
  </style>
  