<template>
    <div class="rotating-image">
      <img src="../assets/sade.png" alt="Rotating Image" class="rotate">
    </div>
  </template>
  
  <script>
  export default {
    name: 'RotatingImage'
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
  </style>
  